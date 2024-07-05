from django.urls import path
from .views import problem_list, problem_detail
from submit.views import submit  # Import submit_code view from submit app

app_name = 'problems'  # Optional: namespace for URL namespacing

urlpatterns = [
    path("list/", problem_list, name="problem_list"),
    path('problem/<str:pk>/', problem_detail, name='problem_detail'),
    path('', submit, name='submit'),  # Route for code submission
]
