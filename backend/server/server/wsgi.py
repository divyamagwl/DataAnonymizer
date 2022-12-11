"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

application = get_wsgi_application()

import inspect
from apps.ml.registry import MLRegistry
from apps.ml.ner.dslim_bert_ner import DslimBertNER
from apps.ml.ner.roberta_large_ner_english import RobertaLargeNEREnglish
from apps.ml.ner.allen_nlp_ner import AllenNlpNER
from apps.ml.ner.spacy_ner import SpacyNER
from apps.ml.anonymization.w2v_allen_nlp_ner import W2VAllenNlpNER
from apps.ml.anonymization.spacy_ner_anony import SpacyNERAnony

try:
    registry = MLRegistry()  # create ML registry

    # DSLIM-BERT-BASE-NER
    endpoint_name = "ner"
    algorithm_object = DslimBertNER()
    algorithm_name = "dslim bert base ner"
    algorithm_version = "0.0.1"
    algorithm_creator = "David S. Lim"
    algorithm_description = "bert-base-NER is a fine-tuned BERT model that is ready to use for Named Entity Recognition and achieves state-of-the-art performance for the NER task."
    algorithm_code = inspect.getsource(DslimBertNER)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )

    # ROBERTA-LARGE-NER-ENGLISH
    endpoint_name = "ner"
    algorithm_object = RobertaLargeNEREnglish()
    algorithm_name = "roberta large ner english"
    algorithm_version = "0.0.1"
    algorithm_creator = "Jean-Baptiste"
    algorithm_description = "roberta-large-ner-english is an english NER model that was fine-tuned from roberta-large on conll2003 dataset. Model was validated on emails/chat data and outperformed other models on this type of data specifically. In particular the model seems to work better on entity that don't start with an upper case."
    algorithm_code = inspect.getsource(RobertaLargeNEREnglish)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )

    # ALLEN-NLP-NER
    endpoint_name = "ner"
    algorithm_object = AllenNlpNER()
    algorithm_name = "allen nlp ner"
    algorithm_version = "0.0.1"
    algorithm_creator = "AllenNLP team"
    algorithm_description = "The AllenNLP team envisions language-centered AI that equitably serves humanity. We work to improve NLP systems' performance and accountability, and advance scientific methodologies for evaluating and understanding those systems. We deliver high-impact research of our own and masterfully-engineered open-source tools to accelerate NLP research around the world."
    algorithm_code = inspect.getsource(AllenNlpNER)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )

    # SPACY-NER
    endpoint_name = "ner"
    algorithm_object = SpacyNER()
    algorithm_name = "spacy ner"
    algorithm_version = "0.0.1"
    algorithm_creator = "Spacy"
    algorithm_description = ""
    algorithm_code = inspect.getsource(SpacyNER)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )

    # W2V-ALLEN-NLP-NER-Anonymization
    endpoint_name = "anonymize"
    algorithm_object = W2VAllenNlpNER()
    algorithm_name = "word2vec allen nlp ner"
    algorithm_version = "0.0.1"
    algorithm_creator = "ScaDS Lab"
    algorithm_description = ""
    algorithm_code = inspect.getsource(W2VAllenNlpNER)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )

    # SPACY-NER-Anonymization
    endpoint_name = "anonymize"
    algorithm_object = SpacyNERAnony()
    algorithm_name = "spacy ner anonymization"
    algorithm_version = "0.0.1"
    algorithm_creator = "ScaDS Lab"
    algorithm_description = ""
    algorithm_code = inspect.getsource(SpacyNERAnony)
    # add to registry
    registry.add_algorithm(
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_version,
        algorithm_creator,
        algorithm_description,
        algorithm_code,
    )



except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
