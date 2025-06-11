from django.shortcuts import render,redirect
from users.models import CustomUser
from django.contrib.auth import login,authenticate,logout
import random
from .forms import CustomUserCreationForm
from puzzles.logger import logging
import time

 
def user(request):
    users = CustomUser.objects.all()
      
    sentences = [ "Sharpen your mind—one word at a time.","Find the hidden. Train the brain.",

     "Play. Learn. Grow.",    "Every word you find makes you smarter.",

     "Puzzle your way to greatness.", "Unlock the power of focus and fun!",

     "Discover words. Discover yourself.", "Turn spare time into brain time.", "Be curious. Be clever. Be unstoppable."]
    
    sentence = random.choice(sentences) 

    return render(request,"user.html",{"sentence":sentence})

 


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logging.info(f"{user.username} created account")
            return redirect('login')
        else:
            logging.warning(f"Failed registration attempt: {form.errors}")
             
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logging.info(f"{user.username} logged in")
            return redirect('user')  # change to your homepage URL name
        else:
            error = "Invalid credentials"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
         
        logging.info(f"{username} logged out")
        time.sleep(1)
    logout(request)
    return redirect("user")