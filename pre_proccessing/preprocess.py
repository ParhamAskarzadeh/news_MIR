from hazm import Lemmatizer, word_tokenize, stopwords_list
from pre_proccessing.normalizer import SelfNormalizer


class DocumentPreProcessing:
    def __init__(self):
        self.stop_words = stopwords_list()
        self.normalizer = SelfNormalizer()
        self.lemmatizer = Lemmatizer()
        self.word_tokenize = word_tokenize()

    def preprocess_text(self, document):
        document = self.normalizer.complete_normalize(document)

        tokens = self.word_tokenize(document)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [word for word in tokens if len(word) > 2]

        preprocessed_text = ' '.join(tokens)

        return preprocessed_text
