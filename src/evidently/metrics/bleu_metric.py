from nltk.translate.bleu_score import sentence_bleu

class BleuMetric:
    def __init__(self):
        pass

    def evaluate(self, reference, candidate):
        """
        reference: list of reference sentences
        candidate: candidate sentence
        """
        score = sentence_bleu([reference.split()], candidate.split())
        return score
