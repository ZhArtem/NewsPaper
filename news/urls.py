from django.urls import path
from .views import PostsList, PostDetail, PostSearch


urlpatterns = [
    path('', PostsList.as_view()),
    path('search', PostSearch.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]
