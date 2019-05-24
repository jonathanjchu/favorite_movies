from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    if 'id' in request.session:
        user_id = request.session['id']
        user = User.objects.get(id=user_id)

        fav_movies = Movie.objects.filter(favorited_by__id=user_id)
        nonfav_movies = Movie.objects.exclude(favorited_by__id=user_id)

        context = {
            'fav_movies': fav_movies,
            'nonfav_movies': nonfav_movies,
            'user': user,
        }

        return render(request, "movies/index.html", context)
    
    else:
        return redirect("/")

def new_movie(request):
    if 'id' not in request.session:
        return redirect("/")
    
    return render(request, "movies/new_movie.html")

def process_new_movie(request):
    if request.method == "POST":
        results = Movie.objects.validate(request.POST)
        if len(results) == 0:
            user = User.objects.get(id=request.session['id'])
            movie = Movie.objects.create(title=request.POST['title'],
                                        year=int(request.POST['year']),
                                        added_by=user)
            movie.favorited_by.add(user)

            return redirect(f"/movies/{movie.id}")
        else:
            for key, val in results.items():
                messages.add_message(request, messages.ERROR, val, key)

    return redirect("/movies/new")

def view_movie(request, mov_id):
    movie = Movie.objects.get(id=mov_id)
    return render(request, "movies/view_movie.html", { 'movie': movie })

def add_to_favs(request, mov_id):
    if 'id' not in request.session:
        return redirect("/")
        
    user = User.objects.get(id=request.session['id'])
    movie = Movie.objects.get(id=mov_id)
    movie.favorited_by.add(user)
    return redirect("/movies")

def remove_from_favs(request, mov_id):
    if 'id' not in request.session:
        return redirect("/")

    user = User.objects.get(id=request.session['id'])
    movie = Movie.objects.get(id=mov_id)
    movie.favorited_by.remove(user)
    return redirect("/movies")
    
def delete_movie(request, mov_id):
    if 'id' not in request.session:
        return redirect("/")

    movie = Movie.objects.get(id=mov_id)

    # check the right user is making the delete call
    if movie.added_by.id == request.session['id']:
        movie.delete()
        return redirect("/movies")
    else:
        # wrong user, suspicious activity
        return redirect("/logout")