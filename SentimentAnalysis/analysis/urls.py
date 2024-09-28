from django.urls import path, include
from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path('get-reviews/<int:company_id>/', views.get_reviews, name='get_reviews'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('api/', include(api.urlpatterns)),

]
