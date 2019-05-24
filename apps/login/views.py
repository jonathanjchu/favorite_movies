from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

# Create your views here.
def index(request):
    return render(request, "login/index.html")

def create_user(request):
    if request.method == "POST":
        validation = User.objects.validator(request.POST)

        if len(validation) == 0:
            # hash password
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            # create new user
            new_user = User.objects.create(username=request.POST['username'],
                                        email=request.POST['email'],
                                        password=hash1.decode(),
                                        birthday=request.POST['birthday'])

            print(new_user.id)
            request.session['id'] = new_user.id

            return redirect(f"/movies")
        else:
            for key, val in validation.items():
                # messages.add_message(request, messages.ERROR, val, key)
                messages.add_message(request, messages.ERROR, val, key)
            return redirect("/")
    else:
        return redirect("/")

def view_user(request, id):
    if 'id' in request.session and request.session['id'] == id:
        # user = User.objects.get(id=id)
        # context = { 'user': user }
        # return render(request, "login/view_user.html", context)
        return redirect("/movies")
    else:
        return redirect("/logout")

def login(request):
    # check if user exists
    results = User.objects.filter(email=request.POST['email_address'])
    if len(results) > 0:
        if bcrypt.checkpw(request.POST['pwd'].encode(), results[0].password.encode()):
            request.session['id'] = results[0].id

            # return redirect(f"/users/{results[0].id}")
            return redirect("/movies")

    messages.add_message(request,
            messages.ERROR,
            "Email and/or password is invalid",
            "login")
    return redirect("/")

def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect("/")