import joblib

from apps.ml.ner.allen_nlp_ner import AllenNlpNER

class W2VAllenNlpNER:
    def __init__(self):
        path_to_artifacts = "../../ml-models/Anonymization/Word2vec_AllenNLP/"
        self.model = joblib.load(path_to_artifacts + "word2vec.joblib")
        self.tags = ["LOC", "PER", "ORG"]

    def fetch_tags(self):
        return {"tags": self.tags, "status": "OK"}

    def preprocessing(self, input_data, tag):
        allen_nlp_ner = AllenNlpNER()
        response = allen_nlp_ner.compute_prediction(input_data)
        combined_words_tag_tuples = response["prediction"]
        output = self.extract_particular_tag(combined_words_tag_tuples, tag)
        return output

    def predict(self, input_data):
        (final_words, idxs_of_tags) = input_data
        output = self.anonymize(final_words, idxs_of_tags)
        return output

    def postprocessing(self, input_data):
        (final_words, look_up) = input_data
        output_string = self.generate_string(final_words)
        return {"prediction": output_string, "lookup": look_up, "status": "OK"}

    def compute_prediction(self, input_data, tag):
        try:
            input_data = self.preprocessing(input_data, tag)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    def extract_particular_tag(self, word_tag_tuples, tag_of_interest):
        final_words = []
        idxs_of_tags = []
        i = 0
        for tpl in word_tag_tuples:
            word = ""
            if tpl[1] != 'O':
                word = tpl[0].replace(' ', '_')
            else:
                word = tpl[0]

            if tpl[1] == tag_of_interest:
                idxs_of_tags.append(i)

            final_words.append(word)
            i+=1
        
        return (final_words, idxs_of_tags)

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

    def generate_string(self, final_words):
        anonymized_string = ""

        for w in final_words:
            if anonymized_string == "":
                anonymized_string = w
            else:
                anonymized_string = anonymized_string + " " + w

        output = anonymized_string.replace('_', ' ')
        return output