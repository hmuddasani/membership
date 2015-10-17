from django import forms

class LoginForm(forms.Form):
  UserName = forms.CharField(max_length=200)
  Password= forms.CharField(widget=forms.PasswordInput)
  def clean_username(self):
	UserName = self.cleaned_data.get("UserName")
	try:
		exists = MyUser.objects.all(UserName=UserName)
		print "UserName", UserName
		print "exists", exists
		if exists:
			raise forms.ValidationError("UserName exists")
	except:
			return UserName

  def clean_password(self):
		Password = self.cleaned_data.get("Password")
		return Password