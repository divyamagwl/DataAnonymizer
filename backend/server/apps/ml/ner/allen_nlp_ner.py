import dill

class AllenNlpNER:
    def __init__(self):
        path_to_artifacts = "../../ml-models/NER/"
        file = open(path_to_artifacts + "./allen-nlp-ner.dill", 'rb')
        self.model = dill.load(file)
        file.close()

    def preprocessing(self, input_data):
        return input_data

    def predict(self, input_data):
        return self.model.predict(sentence=input_data)

    def postprocessing(self, input_data):
        word_tag_tuples = self.extract_word_tag(input_data)
        combined_words_tag_tuples = self.combine_words(word_tag_tuples)
        return {"prediction": combined_words_tag_tuples, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    def extract_word_tag(self, predicted_result):
        word_tag_tuples = []

        for word, tag in zip(predicted_result['words'], predicted_result['tags']):
            word_tag_tuples.append((word, tag)) 

        return word_tag_tuples

    def combine_words(self, word_tag_tuples):
        n = len(word_tag_tuples)
        combined_words = []
        i = 0
        s = ""
        prev_tag = ""
        while i < n:
            ps = word_tag_tuples[i][0]
            pt = word_tag_tuples[i][1]

            if pt[0] == 'B':
                if s != "":
                    tpl = (s, prev_tag)
                    combined_words.append(tpl)
                s = ps
                prev_tag = pt[2:]

            elif pt[0] == 'I': 
                s = s + " " + ps
                prev_tag = pt[2:]

            elif pt[0] == 'L':
                s = s + " " + ps
                tpl = (s, pt[2:])
                combined_words.append(tpl)
                s = ""

            elif pt[0] == 'U':
                if s != "":
                    tpl = (s, prev_tag)
                    combined_words.append(tpl)
                tpl1 = (ps, pt[2:])
                combined_words.append(tpl1)
                s=""
                prev_tag=""

            elif pt == "O":
                if(prev_tag == "O"):
                    if ps == '.' or ps == ',':
                        s = s+ps
                    else:
                        s = s + " " + ps
                else:
                    if s!="":
                        tpl = (s, prev_tag)
                        combined_words.append(tpl)
                    s = ps
                prev_tag = pt

            i += 1

        if s != "":
            tpl = (s, prev_tag)
            combined_words.append(tpl)

        return combined_words
