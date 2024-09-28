from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('api/submit-response/', views.SubmitResponse.as_view(), name='submit-response'),
    path('get-reviews/<int:company_id>/', views.get_reviews, name='get_reviews'),

]