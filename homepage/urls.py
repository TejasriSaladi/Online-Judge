from django.urls import path
from homepage.views import home_page, login_view, register_view  # Adjust the import based on your actual views file and function

urlpatterns = [
    path('page/', home_page, name='home_page'),
    path('login/', login_view, name='login_view'),  # Comma added here
    path('signup/', register_view, name='register_view'),  # Comma added here
]
