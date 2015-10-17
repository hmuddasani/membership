from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.utils.safestring import mark_safe
from videos.models import Video
from .forms import LoginForm

def auth_login(request):
  form = LoginForm(request.POST or None)
  next_url=request.GET.get('next')
  if form.is_valid():
     UserName = form.cleaned_data['UserName']
     Password = form.cleaned_data['Password']
     user=authenticate(UserName=UserName, Password=Password)
     print user
     if user is not None:
			login(request, user)
			if next_url is not None:
				return HttpResponseRedirect(next_url)
			return HttpResponseRedirect("/")
  context = { 
             "form" : form,
			 }
  return render(request, 'login.html', context)
  
def auth_logout(request):
   logout(request)
   return HttpResponseRedirect('/')