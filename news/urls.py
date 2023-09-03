from django.urls import path
from .views import *


urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/', PostByCategoryListView.as_view(), name='post_by_category'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
