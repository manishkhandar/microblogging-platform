from django.urls import path
from .views import UserDetailView

urlpatterns = [
    path('', UserDetailView.as_view()),  # create
    path('<int:user_id>/', UserDetailView.as_view()),  # get , update
]
