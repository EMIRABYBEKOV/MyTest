from django.urls import path
from .views import find_screen_view, find_test_view, TestView, check_answers, create_test_view


urlpatterns = [
    path('test/', find_test_view, name='test'),
    path('test/<str:slug>/', TestView.as_view(), name='test_page'),
    path('test/result/', check_answers, name='result_page'),
    path('create/test/', create_test_view, name='create_test'),



]
