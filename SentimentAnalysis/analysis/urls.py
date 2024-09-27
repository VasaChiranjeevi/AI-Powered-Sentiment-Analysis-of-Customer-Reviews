from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-reviews/<int:company_id>/', views.get_reviews, name='get_reviews'),
    path('submit-review/', views.submit_review, name='submit_review'),
]
