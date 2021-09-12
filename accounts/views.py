from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        photo = request.FILES.get('photo')
        room_id = request.POST["id"]
        user, created = User.objects.get_or_create(username = username)
        if created:
            """condition for new account created"""
            user.set_password(
                    password 
                )
            user.save()
            Account.objects.create(user=user)
            user = auth.authenticate(username=username, password = password)
            auth.login(request, user)
        else:
            """condition for already a user. so log in"""
            user = auth.authenticate(username = username, password = password) 
            if user is not None:
                auth.login(request, user)
            else:
                """password error"""
                return render(request, 'accounts/register.html', 
                        context= {"wrong_password": "wrong password"}
                )
        return redirect( f"/chat/{room_id}")
    return render(request, 'accounts/register.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('register')

