from django.shortcuts import render
from operator import itemgetter
from PIL import Image

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.models import Account


# Create your views here.
# @login_required
def chat(request, id):
    print(request.user)
    if request.user.is_authenticated:
        account = Account.objects.get(user = request.user)
    else:
        return redirect('register')
    return render(request, "chat/chat.html", context = {"account": account, "id":id})


