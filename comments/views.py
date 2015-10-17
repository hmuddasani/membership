from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from videos.models import Video
from notifications.signals import notify

# Create your views here.
def comment_thread(request, id):
	comment = Comment.objects.get(id=id)
	form = CommentForm()
	context = {
			"comment": comment,
			"form" : form,
			}
	return render(request, "comments/comment_thread.html", context)
	
def comment_create_view(request):
	if request.method == "POST" and request.user.is_authenticated():
		parent_id = request.POST.get('parent_id')
		video_id = request.POST.get("video_id")
		origin_path = request.POST.get("origin_path")
		try:
			video = Video.objects.get(id=video_id)
		except:
			video = None

		print video
		parent_comment = None
		if parent_id is not None:
			try:
				parent_comment = Comment.objects.get(id=parent_id)
			except:
				parent_comment = None

			if parent_comment is not None and parent_comment.video is not None:
				video = parent_comment.video

		form = CommentForm(request.POST)
		if form.is_valid():
			comment_text = form.cleaned_data['Comment']
			if parent_comment is not None:
				# parent comments exists
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=parent_comment.get_origin, 
					text=comment_text,
					video = video,
					parent=parent_comment
					)
				notify.send(request.user, 
							recipient=parent_comment.user, 
							verb='Responded to user', 
							target=parent_comment, 
							action=new_comment)
				messages.success(request, "Thank you for your response.", extra_tags='safe')
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			else:
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=origin_path, 
					text=comment_text,
					video = video
					)
				notify.send(request.user, 
							recipient= request.user, 
							action=new_comment,
							target=new_comment.video,
							verb="commented on"
							)
				messages.success(request, "Thank you for the comment.")
				return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			print origin_path
			messages.error(request, "There was an error with your comment.")
			return HttpResponseRedirect(origin_path)

	else:
		raise Http404