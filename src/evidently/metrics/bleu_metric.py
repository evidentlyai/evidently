# src/evidently/metrics/bleu_metric.py
"""
BLEU Metric for evaluating candidate sentences against reference sentences.
Beginner-friendly contribution for Hacktoberfest.
"""

from nltk.translate.bleu_score import sentence_bleu

class BleuMetric:
    def __init__(self):
        """Initialize the BLEU metric class."""
        pass

    def evaluate(self, reference, candidate):
        """
        Evaluate the BLEU score.

        Parameters:
        reference (str): The reference sentence.
        candidate (str): The candidate sentence to evaluate.

        Returns:
        float: BLEU score between 0 and 1.
        """
        # Convert sentences to lists of words
        reference_words = reference.split()
        candidate_words = candidate.split()

        # Compute BLEU score
        score = sentence_bleu([reference_words], candidate_words)

        return score


# Example usage (for maintainers/tests)
if __name__ == "__main__":
    reference_sentence = "The cat is on the mat"
    candidate_sentence = "The cat is on the mat"
    
    bleu = BleuMetric()
    print("BLEU Score:", bleu.evaluate(reference_sentence, candidate_sentence))
