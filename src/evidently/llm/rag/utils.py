from pathlib import Path
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from pypdf._utils import StrByteType


def read_text_pdf(file: Union["StrByteType", Path]) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise ImportError("Please install pypdf to extract context from .pdf files") from e
    reader = PdfReader(file)
    texts = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        texts.append(page.extract_text())
    return "".join(texts)


def read_text(filename: str) -> str:
    file_path = Path(filename)
    if file_path.suffix.lower() == ".pdf":
        read_text(read_text_pdf(filename))
    return Path(filename).read_text()
