from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm

class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                    algorithm_version, creator,
                    algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name)

        # get algorithm
        database_object, _ = MLAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                code=algorithm_code,
                version=algorithm_version,
                creator=creator,
                parent_endpoint=endpoint)

        # add to registry
        self.endpoints[database_object.id] = algorithm_object
