from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.new_movie),
    path('new/add', views.process_new_movie),
    path('<int:mov_id>', views.view_movie),
    path('<int:mov_id>/fav', views.add_to_favs),
    path('<int:mov_id>/unfav', views.remove_from_favs),
    path('<int:mov_id>/delete', views.delete_movie),
]