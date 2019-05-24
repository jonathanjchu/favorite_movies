from django.urls import path, include

urlpatterns = [
    path('', include("apps.login.urls")),
    path('movies/', include("apps.movies.urls")),
]