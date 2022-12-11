import joblib

class DslimBertNER:
    def __init__(self):
        path_to_artifacts = "../../ml-models/NER/"
        self.model = joblib.load(path_to_artifacts + "dslim-bert-base-NER-nlp.joblib")

    def preprocessing(self, input_data):
        return input_data

    def predict(self, input_data):
        return self.model(input_data)

    def postprocessing(self, input_data):
        return {"prediction": input_data, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction