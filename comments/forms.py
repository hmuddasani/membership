from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment

#class CommentForm(forms.ModelForm):
#	class Meta:
#			model = Comment
#			fields = ('user','text','path')
			
class CommentForm(forms.Form):
	Comment = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Your Comment/Reply"})
	)
	
	def __init__(self, data=None, files=None, **kwargs):
		super(CommentForm, self).__init__(data, files, kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.add_input(Submit('submit', 'Add Comment', css_class='btn btn-primary',))