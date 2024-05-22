import logging
from flair.data import Sentence, Token
from flair.models import SequenceTagger
from cassis import load_cas_from_xmi, load_typesystem, Cas, TypeSystem, merge_typesystems
from ariadne.server import Server
from ariadne.classifier import Classifier
from ariadne.util import setup_logging
from ariadne.contrib.inception_util import create_prediction, TOKEN_TYPE, IS_PREDICTION
from ariadne.contrib.inception_util import SENTENCE_TYPE

PREDICTED_TYPE = "webanno.custom.AjMCNamedEntity"
PREDICTED_FEATURE = "value"
USER = "mromanello"
PROJECT_ID = "test_project"
PATH_HMBERT_AJMC_MULTILINGUAL_MODEL = "./models/bert-base-historic-multilingual-cased-bs4-wsFalse-e10-lr5e-05-layers-1-crfFalse-1/best-model.pt"

setup_logging(level=logging.DEBUG)


class ClassicsNERClassifier(Classifier):
    
    def __init__(self, language : str, tagset : str):
        if tagset == 'fine':
            self._model = SequenceTagger.load(PATH_HMBERT_AJMC_MULTILINGUAL_MODEL)
        elif tagset == 'coarse':
            self._model = SequenceTagger.load(f"hmteams/flair-hipe-2022-ajmc-{language}")

    def predict(self, cas: Cas, layer: str, feature: str, project_id: str, document_id: str, user_id: str):
        tokens_cas = list(cas.select(TOKEN_TYPE))
        sentences = cas.select(SENTENCE_TYPE)
        text = []
        idx = 0
        for sentence in sentences:
            tokens = [
                Token(t.get_covered_text())
                for t in cas.select_covered(TOKEN_TYPE, sentence)
            ]
            for token in tokens:
                token.index = idx
                idx += 1
            s = Sentence(tokens)
            text.append(s)
        
        self._model.predict(text)

        for sentence in text:
            for ent in sentence.get_spans('ner'):
                start_idx = ent.tokens[0].index
                end_idx = start_idx + len(ent.tokens) - 1
                begin = tokens_cas[start_idx].begin
                end = tokens_cas[end_idx].end
                prediction = create_prediction(cas, layer, feature, begin, end, ent.tag)
                #prediction.set(f'{feature}_score', ent.score)
                cas.add(prediction)

def build_typesystem() -> TypeSystem:
    typesystem = TypeSystem()
    SentenceType = typesystem.create_type(SENTENCE_TYPE)
    PredictedType = typesystem.create_type(PREDICTED_TYPE)
    typesystem.create_feature(PredictedType, PREDICTED_FEATURE, "uima.cas.String")
    typesystem.create_feature(PredictedType, IS_PREDICTION, "uima.cas.Boolean")
    return typesystem

def load_test_document() -> Cas:
    with open("data/AjMC_TypeSystem.xml", "rb") as f:
        typesystem = merge_typesystems(load_typesystem(f), build_typesystem())

    with open("data/lestragdiesdeso00tourgoog_0065.xmi", "rb") as f:
        cas = load_cas_from_xmi(f, typesystem=typesystem)

    return cas

server = Server()
#server.add_classifier("ner_coarse_fr", ClassicsNERClassifier("fr", "coarse"))
#server.add_classifier("ner_coarse_de", ClassicsNERClassifier("de", "coarse"))
#server.add_classifier("ner_coarse_en", ClassicsNERClassifier("en", "coarse"))
server.add_classifier("ner_fine_multiling", ClassicsNERClassifier(None, "fine"))
app = server._app

if __name__ == '__main__':
    server.start(debug=True)