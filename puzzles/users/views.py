from django.shortcuts import render,redirect
from users.models import CustomUser
from django.contrib.auth import login,authenticate,logout
import random
from .forms import CustomUserCreationForm

 
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
            form.save()
            return redirect('login')  # Change as needed
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
            return redirect('user')  # change to your homepage URL name
        else:
            error = "Invalid credentials"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("user")