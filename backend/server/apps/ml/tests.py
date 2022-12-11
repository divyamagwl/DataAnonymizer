from django.test import TestCase

import inspect

from apps.ml.registry import MLRegistry
from apps.ml.ner.dslim_bert_ner import DslimBertNER
from apps.ml.ner.roberta_large_ner_english import RobertaLargeNEREnglish
from apps.ml.ner.allen_nlp_ner import AllenNlpNER
from apps.ml.ner.spacy_ner import SpacyNER
from apps.ml.anonymization.w2v_allen_nlp_ner import W2VAllenNlpNER
from apps.ml.anonymization.spacy_ner_anony import SpacyNERAnony

class MLTests(TestCase):
    def test_dslim_algorithm(self):
        input_data = "My name is Wolfgang and I live in Berlin"
        my_alg = DslimBertNER()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_roberta_algorithm(self):
        input_data = "My name is Wolfgang and I live in Berlin"
        my_alg = RobertaLargeNEREnglish()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_allen_nlp_algorithm(self):
        input_data = "Albert Einstein was born in Germany and lived in England."
        my_alg = AllenNlpNER()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_spacy_ner_algorithm(self):
        input_data = "Albert Einstein was born in Germany and lived in England."
        my_alg = SpacyNER()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_w2v_allen_nlp_fetch_tags(self):
        my_alg = W2VAllenNlpNER()
        response = my_alg.fetch_tags()
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_w2v_allen_nlp_algorithm(self):
        input_data = "Albert Einstein was born in Germany and lived in England."
        tag = "LOC"
        my_alg = W2VAllenNlpNER()
        response = my_alg.compute_prediction(input_data, tag)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_spacy_ner_anony_algorithm(self):
        input_data = "Albert Einstein was born in Germany and lived in England."
        tag = "PERSON"
        my_alg = SpacyNERAnony()
        response = my_alg.compute_prediction(input_data, tag)
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_spacy_ner_anony_fetch_tags(self):
        my_alg = SpacyNERAnony()
        response = my_alg.fetch_tags()
        self.assertEqual('OK', response['status'])
        # print(response)

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "ner"
        algorithm_object = DslimBertNER()
        algorithm_name = "DSLIM BERT"
        algorithm_version = "0.0.1"
        algorithm_creator = "David S. Lim"
        algorithm_description = "bert-base-NER is a fine-tuned BERT model that is ready to use for Named Entity Recognition and achieves state-of-the-art performance for the NER task."
        algorithm_code = inspect.getsource(DslimBertNER)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                    algorithm_version, algorithm_creator,
                    algorithm_description, algorithm_code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
