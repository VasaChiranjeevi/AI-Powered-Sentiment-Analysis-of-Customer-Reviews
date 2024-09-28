from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('analyse-reviews', views.AnalyseReviews.as_view(), name='analyse-reviews'),
    path('submit-response/', views.SubmitResponse.as_view(), name='submit-response'),

]