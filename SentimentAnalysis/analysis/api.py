from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('analyse-reviews', views.AnalyseReviews.as_view(), name='analyse-reviews'),
    path('analyse-sentiment', views.AnalyseSentiment.as_view(), name='analyse-sentiment'),

]