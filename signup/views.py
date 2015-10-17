from django.shortcuts import render, redirect
from .models import SignUp, MyUser
from .forms import SignUpForm, RegisterForm

# Create your views here.

def home(request):
   return render(request, 'home.html', {})

def register(request):
   form = RegisterForm(request.POST or None)

   if form.is_valid():
	  username = form.cleaned_data['username']
	  email = form.cleaned_data['email']
	  password = form.cleaned_data['password2']
	  instance = MyUser()
	  instance.username = username
	  instance.email = email
	  instance.set_password(password)
	  instance.save()
	  return redirect('login')
   context = {
			"form": form,
			"action_value": "",
			"submit_btn_value": "Register",
			   }
   return render(request, 'register.html', context)
  