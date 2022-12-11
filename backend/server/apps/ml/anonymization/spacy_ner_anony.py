import joblib

class SpacyNERAnony:
    def __init__(self):
        path_to_artifacts_ner = "../../ml-models/NER/"
        self.nerModel = joblib.load(path_to_artifacts_ner + "spacy-ner.joblib")

        path_to_artifacts_w2v = "../../ml-models/Anonymization/Word2vec_AllenNLP/"
        self.model = joblib.load(path_to_artifacts_w2v + "word2vec.joblib")

        self.tags = ['CARDINAL',
                    'DATE',
                    'EVENT',
                    'FAC',
                    'GPE',
                    'LANGUAGE',
                    'LAW',
                    'LOC',
                    'MONEY',
                    'NORP',
                    'ORDINAL',
                    'ORG',
                    'PERCENT',
                    'PERSON',
                    'PRODUCT',
                    'QUANTITY',
                    'TIME',
                    'WORK_OF_ART']


    def fetch_tags(self):
        return {"tags": self.tags, "status": "OK"}

    def preprocessing(self, input_data, tag):
        ner_text = self.nerModel(input_data)
        output = self.extract_particular_tag(input_data, ner_text, tag)
        return output

    def predict(self, input_data):
        (new_input_data, final_words, idxs_of_tags) = input_data
        output = self.anonymize(final_words, idxs_of_tags)
        (anony_words, look_up) = output
        return (new_input_data, anony_words, look_up)

    def postprocessing(self, prediction):
        (new_input_data, _, look_up) = prediction
        output_string = self.generate_string(look_up, new_input_data)
        return {"prediction": output_string, "lookup": look_up, "status": "OK"}

    def compute_prediction(self, input_data, tag):
        try:
            processed_data = self.preprocessing(input_data, tag)
            prediction = self.predict(processed_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    def extract_particular_tag(self, input_data, processed_text, tag_of_interest):
        final_words = []
        idxs_of_tags = []
        for word in processed_text.ents:
            if word.label_ == tag_of_interest:
                final_words.append(word.text)


        i = 0
        final_words1 = []
        for key in final_words:
            replaced=''
            if ' ' not in key:
                continue
            else:
                idxs_of_tags.append(i)
                replaced = key.replace(' ','_')
                final_words1.append(replaced)
            i += 1

        input_data = input_data.replace(final_words[0], final_words1[0])

        return (input_data, final_words1, idxs_of_tags)

    def anonymize(self, final_words, idxs_of_tags):
        look_up = {}
        top_n = 20

        for i in idxs_of_tags:
            lst = []
            w = final_words[i]
            keys = list(look_up.keys())
            values = list(look_up.values())
            if w in keys:
                final_words[i] = look_up[w]
            else:
                if w in self.model.wv.key_to_index:
                    lst = self.model.wv.most_similar(w, topn=top_n)
                    j=0
                    while j<top_n:
                        if lst[i][0] in values:
                            j+=1
                            continue
                        else:
                            break

                    if j<top_n:
                        final_words[i] = lst[j][0]
                        look_up[w] = lst[j][0].replace('_', ' ')

        return (final_words, look_up)

    def generate_string(self, look_up, input_data):
        anonymized_string = ""
        final_words = input_data.split()

        for w in final_words:
            if anonymized_string == "":
                if(w in look_up):
                    anonymized_string = look_up[w]
                else:
                    anonymized_string = w
            else:
                if(w in look_up):
                    anonymized_string = anonymized_string + " " + look_up[w]
                else:
                    anonymized_string = anonymized_string + " " + w

        output = anonymized_string.replace('_', ' ')
        return output