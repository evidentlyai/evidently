import re
from typing import TYPE_CHECKING
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd

from evidently.core.datasets import AnyDescriptorTest
from evidently.core.datasets import Dataset
from evidently.core.datasets import DatasetColumn
from evidently.core.datasets import Descriptor
from evidently.legacy.core import ColumnType
from evidently.legacy.options.base import Options

if TYPE_CHECKING:
    from nltk.stem.wordnet import WordNetLemmatizer


class TextMatchOptions:
    """Configuration options for text matching operations."""

    def __init__(
        self,
        case_sensitive: bool = True,
        lemmatize: bool = False,
        word_boundaries: bool = False,
    ):
        self.case_sensitive = case_sensitive
        self.lemmatize = lemmatize
        self.word_boundaries = word_boundaries


class TextMatchProcessor:
    """Centralized processing logic for all text matching operations."""

    _lem: Optional["WordNetLemmatizer"] = None

    def __init__(self, options: TextMatchOptions):
        self.options = options

    @property
    def lem(self):
        if self._lem is None:
            try:
                import nltk
                from nltk.stem.wordnet import WordNetLemmatizer

                nltk.download("wordnet", quiet=True)
                self._lem = WordNetLemmatizer()
            except ImportError:
                raise ImportError("NLTK is required for lemmatization. Install with: pip install nltk")
        return self._lem

    def process_text(self, text: str) -> str:
        """Unified text preprocessing pipeline."""
        if text is None or (isinstance(text, float) and np.isnan(text)):
            return ""

        if not isinstance(text, str):
            text = str(text)

        if self.options.word_boundaries:
            # Extract words using regex, removing non-alphanumeric characters
            text = " ".join(re.findall(r"\b\w+\b", text))

        if self.options.lemmatize:
            text = self._lemmatize_text(text)

        return text

    def _lemmatize_text(self, text: str) -> str:
        """Apply lemmatization to text."""
        words = text.split()
        lemmatized_words = [self.lem.lemmatize(word.lower()) for word in words]
        return " ".join(lemmatized_words)

    def all_match(self, text: str, items: List[str]) -> bool:
        """Check if text contains all of the specified items."""
        processed_text = self.process_text(text)

        if self.options.case_sensitive:
            return all(item in processed_text for item in items)
        else:
            processed_text_lower = processed_text.lower()
            return all(item.lower() in processed_text_lower for item in items)

    def any_match(self, text: str, items: List[str]) -> bool:
        """Check if text contains any of the specified items."""
        processed_text = self.process_text(text)

        if self.options.case_sensitive:
            return any(item in processed_text for item in items)
        else:
            processed_text_lower = processed_text.lower()
            return any(item.lower() in processed_text_lower for item in items)

    def regex_match(self, text: str, pattern: str) -> bool:
        """Check if text matches a regex pattern."""
        processed_text = self.process_text(text)

        flags = 0 if self.options.case_sensitive else re.IGNORECASE
        return bool(re.search(pattern, processed_text, flags))

    def exact_match(self, text: str, items: List[str]) -> bool:
        """Check if text exactly matches any of the specified items."""
        processed_text = self.process_text(text)

        if self.options.case_sensitive:
            return processed_text in items
        else:
            return processed_text.lower() in [item.lower() for item in items]


class TextMatch(Descriptor):
    """
    Unified text matching descriptor that handles all word/text matching scenarios.

    This descriptor replaces multiple legacy text matching features with a single,
    intuitive API that supports various matching strategies.

    Examples:
        # Simple contains matching
        TextMatch(text_column="description", match_items=["urgent", "important"])

        # Column-to-column matching
        TextMatch(text_column="description", match_items="keywords_column")

        # Exclusions with lemmatization
        TextMatch(
            text_column="description",
            match_items=["spam", "test"],
            match_type="not_contains",
            lemmatize=True
        )

        # Regex matching
        TextMatch(text_column="description", match_items=r"\b\d{3}-\d{3}-\d{4}\b", match_type="regex")
    """

    column_name: str
    match_items: Union[str, List[str]]
    match_type: Literal["contains", "not_contains", "exact", "regex"] = "contains"
    match_mode: Literal["any", "all"] = "any"

    # Processing options with smart defaults
    case_sensitive: bool = True
    lemmatize: bool = False
    word_boundaries: bool = False

    def __init__(
        self,
        column_name: str,
        match_items: Union[str, List[str]],
        match_type: Literal["contains", "not_contains", "exact", "regex"] = "contains",
        match_mode: Literal["any", "all"] = "any",
        case_sensitive: bool = True,
        lemmatize: bool = False,
        word_boundaries: bool = False,
        alias: Optional[str] = None,
        tests: Optional[List[AnyDescriptorTest]] = None,
    ):
        self.column_name = column_name
        self.match_items = match_items
        self.match_type = match_type
        self.match_mode = match_mode
        self.case_sensitive = case_sensitive
        self.lemmatize = lemmatize
        self.word_boundaries = word_boundaries

        # Smart defaults
        if lemmatize and not word_boundaries:
            self.word_boundaries = True

        super().__init__(alias=alias or _generate_alias(match_items, match_mode, column_name, match_type), tests=tests)

    def generate_data(self, dataset: "Dataset", options: Options) -> DatasetColumn:
        """Generate the text matching feature data."""
        df = dataset.as_dataframe()

        processor = TextMatchProcessor(
            options=TextMatchOptions(
                case_sensitive=self.case_sensitive,
                lemmatize=self.lemmatize,
                word_boundaries=self.word_boundaries,
            )
        )

        if isinstance(self.match_items, str):
            # Column-to-column matching
            if self.match_items not in df.columns:
                raise ValueError(f"Column '{self.match_items}' not found in dataset")
            result = self._column_matching(df[self.column_name], df[self.match_items], processor)
        else:
            # List matching
            result = self._list_matching(df[self.column_name], self.match_items, processor)

        return DatasetColumn(type=ColumnType.Categorical, data=result)

    def _apply_matching(self, text: str, items: List[str], processor: TextMatchProcessor) -> bool:
        """Apply the core matching logic for a single text-item pair."""
        if self.match_type == "contains":
            if self.match_mode == "any":
                return processor.any_match(text, items)
            # all
            return processor.all_match(text, items)
        if self.match_type == "not_contains":
            if self.match_mode == "any":
                return not processor.all_match(text, items)
            # all
            return not processor.any_match(text, items)
        if self.match_type == "exact":
            return processor.exact_match(text, items)
        if self.match_type == "regex":
            if len(items) != 1:
                raise ValueError("Regex matching requires exactly one pattern")
            return processor.regex_match(text, items[0])
        raise ValueError(f"Unknown match_type: {self.match_type}")

    def _column_matching(
        self, text_series: pd.Series, items_series: pd.Series, processor: TextMatchProcessor
    ) -> pd.Series:
        """Apply matching when comparing two columns."""

        def match_row(text, items):
            if not isinstance(items, (list, tuple)):
                items = [items] if pd.notna(items) else []
            return self._apply_matching(text, items, processor)

        return text_series.combine(items_series, match_row)

    def _list_matching(self, text_series: pd.Series, items: List[str], processor: TextMatchProcessor) -> pd.Series:
        """Apply matching when using a fixed list of items."""

        def match_text(text):
            return self._apply_matching(text, items, processor)

        return text_series.apply(match_text)

    def list_input_columns(self) -> List[str]:
        """List the input columns required for this descriptor."""
        columns = [self.column_name]
        if isinstance(self.match_items, str):
            columns.append(self.match_items)
        return columns


def _generate_alias(match_items, match_mode, column_name, match_type) -> str:
    """Generate a descriptive alias for the feature."""
    items_str = str(match_items) if isinstance(match_items, str) else f"{len(match_items)}_items"
    mode_str = f"_{match_mode}" if match_mode != "any" else ""

    return f"{column_name}_{items_str}_{match_type}{mode_str}"


# Convenience functions matching legacy feature names
def Contains(
    column_name: str,
    items: List[str],
    case_sensitive: bool = True,
    mode: Literal["any", "all"] = "any",
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy Contains feature."""
    return TextMatch(
        column_name=column_name,
        match_items=items,
        match_type="contains",
        match_mode=mode,
        case_sensitive=case_sensitive,
        alias=alias,
        tests=tests,
    )


def DoesNotContain(
    column_name: str,
    items: List[str],
    case_sensitive: bool = True,
    mode: Literal["any", "all"] = "any",
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy DoesNotContain feature."""
    # legacy has inverted logic
    mode = "all" if mode == "any" else "any"
    return TextMatch(
        column_name=column_name,
        match_items=items,
        match_type="not_contains",
        match_mode=mode,
        case_sensitive=case_sensitive,
        alias=alias,
        tests=tests,
    )


def ItemMatch(
    columns: List[str],
    case_sensitive: bool = True,
    mode: Literal["any", "all"] = "any",
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy ItemMatch feature."""
    if len(columns) != 2:
        raise ValueError("ItemMatch requires exactly 2 columns")
    return TextMatch(
        column_name=columns[0],
        match_items=columns[1],
        match_type="contains",
        match_mode=mode,
        case_sensitive=case_sensitive,
        alias=alias,
        tests=tests,
    )


def ItemNoMatch(
    columns: List[str],
    case_sensitive: bool = True,
    mode: Literal["any", "all"] = "any",
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy ItemNoMatch feature."""
    # legacy has inverted logic
    mode = "all" if mode == "any" else "any"
    if len(columns) != 2:
        raise ValueError("ItemNoMatch requires exactly 2 columns")
    return TextMatch(
        column_name=columns[0],
        match_items=columns[1],
        match_type="not_contains",
        match_mode=mode,
        case_sensitive=case_sensitive,
        alias=alias,
        tests=tests,
    )


def WordsPresence(
    column_name: str,
    words_list: List[str],
    mode: Literal["includes_any", "includes_all", "excludes_any", "excludes_all"] = "includes_any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy WordsPresence feature."""
    match_type: Literal["contains", "not_contains"] = "contains" if mode.startswith("includes") else "not_contains"
    match_mode: Literal["any", "all"] = "any" if mode.endswith("any") else "all"

    return TextMatch(
        column_name=column_name,
        match_items=words_list,
        match_type=match_type,
        match_mode=match_mode,
        lemmatize=lemmatize,
        case_sensitive=False,
        word_boundaries=True,  # WordsPresence uses word boundaries
        alias=alias,
        tests=tests,
    )


def IncludesWords(
    column_name: str,
    words_list: List[str],
    mode: Literal["any", "all"] = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy IncludesWords feature."""
    return TextMatch(
        column_name=column_name,
        match_items=words_list,
        match_type="contains",
        match_mode=mode,
        lemmatize=lemmatize,
        word_boundaries=True,
        case_sensitive=False,
        alias=alias,
        tests=tests,
    )


def ExcludesWords(
    column_name: str,
    words_list: List[str],
    mode: Literal["any", "all"] = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy ExcludesWords feature."""
    return TextMatch(
        column_name=column_name,
        match_items=words_list,
        match_type="not_contains",
        match_mode=mode,
        lemmatize=lemmatize,
        word_boundaries=True,
        case_sensitive=False,
        alias=alias,
        tests=tests,
    )


def WordMatch(
    columns: List[str],
    mode: Literal["any", "all"] = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy WordMatch feature."""
    if len(columns) != 2:
        raise ValueError("WordMatch requires exactly 2 columns")
    return TextMatch(
        column_name=columns[0],
        match_items=columns[1],
        match_type="contains",
        match_mode=mode,
        lemmatize=lemmatize,
        word_boundaries=True,
        case_sensitive=False,
        alias=alias,
        tests=tests,
    )


def WordNoMatch(
    columns: List[str],
    mode: Literal["any", "all"] = "any",
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy WordNoMatch feature."""
    if len(columns) != 2:
        raise ValueError("WordNoMatch requires exactly 2 columns")
    return TextMatch(
        column_name=columns[0],
        match_items=columns[1],
        match_type="not_contains",
        match_mode=mode,
        lemmatize=lemmatize,
        word_boundaries=True,
        case_sensitive=False,
        alias=alias,
        tests=tests,
    )


def TriggerWordsPresent(
    column_name: str,
    words_list: List[str],
    lemmatize: bool = True,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy TriggerWordsPresent feature."""
    return TextMatch(
        column_name=column_name,
        match_items=words_list,
        match_type="contains",
        match_mode="any",
        lemmatize=lemmatize,
        word_boundaries=True,
        case_sensitive=False,
        alias=alias,
        tests=tests,
    )


def RegExp(
    column_name: str,
    reg_exp: str,
    alias: Optional[str] = None,
    tests: Optional[List[AnyDescriptorTest]] = None,
) -> TextMatch:
    """Convenience function matching legacy RegExp feature."""
    return TextMatch(
        column_name=column_name,
        match_items=[reg_exp],
        match_type="regex",
        case_sensitive=True,
        alias=alias,
        tests=tests,
    )
