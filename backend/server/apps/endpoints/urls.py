from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import EndpointViewSet, MLAlgorithmViewSet, MLRequestViewSet
from apps.endpoints.views import PredictView, TagsView

router = DefaultRouter()
router.register(r'api/v1/endpoints', EndpointViewSet, basename='endpoints')
router.register(r'api/v1/mlalgorithms', MLAlgorithmViewSet, basename='mlalgorithms')
router.register(r"api/v1/mlrequests", MLRequestViewSet, basename="mlrequests")

urlpatterns = router.urls

urlpatterns += [
    path("api/v1/tags/<str:endpoint>/<int:mlalgoindex>", TagsView.as_view(), name="tags"),
    path("api/v1/predict/<str:endpoint>/<int:mlalgoindex>", PredictView.as_view(), {'tag': None}, name="predict"),
    path("api/v1/predict/<str:endpoint>/<int:mlalgoindex>/<str:tag>", PredictView.as_view(), name="predict")
]