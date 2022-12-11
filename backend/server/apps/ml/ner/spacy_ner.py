import joblib

class SpacyNER:
    def __init__(self):
        path_to_artifacts = "../../ml-models/NER/"
        self.model = joblib.load(path_to_artifacts + "spacy-ner.joblib")

    def preprocessing(self, input_data):
        return input_data

    def predict(self, input_data):
        return self.model(input_data)

    def postprocessing(self, input_data):
        output = []
        for word in input_data.ents:
            output.append((word.text, word.label_))
        return {"prediction": output, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

    