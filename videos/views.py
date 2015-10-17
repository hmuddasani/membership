from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from videos.models import Video
from .models import Video, Category, TaggedItem
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.

#def get_video_title(request):
 #   title = Video.objects.all()
  #  print "title", title
   # return title
@login_required
def home(request):
	videos = Video.objects.all()
	embeds = []

	for vid in videos:
		code = mark_safe(vid.embed_code)
		embeds.append("%s" %(code))

	context = {
		"number": videos.count(),
		"videos": videos,
		"the_embeds": embeds,
		#"code": mark_safe(videos.embed_code)
	}
	return render(request, "video_home.html", context)

def video_list(request):
   try:
		videos = Video.objects.all()
		
		context = {
					"videos" : videos,
				  }
		return render(request,"video_list.html", context)
   except:
        raise Http404
   
def video_detail(request, cat_slug, vid_slug):
	obj = Video.objects.get(slug=vid_slug)
	comments = obj.comment_set.all()
	#content_type = ContentType.objects.get_for_model(obj)
	#tags = TaggedItem.objects.filter(content_type=content_type, object_id=obj.id)
	#print obj.tag.all()
	for c in comments:
		c.get_children()
	try:
		cat = Category.objects.get(slug=cat_slug)
	except:
		raise Http404
	try:
		obj = Video.objects.get(slug=vid_slug)
		comments = obj.comment_set.all()
		comment_form = CommentForm()
		return render(request, "video_detail.html", {"obj": obj, "comments":comments, "comment_form": comment_form})
	except:
		raise Http404

def category_list(request):
   try:
		category = Category.objects.all()
		context = {
					"category" : category,
				  }
		return render(request,"category_list.html", context)
   except:
        raise Http404
   
def category_detail(request, cat_slug):
   try:
		obj = Category.objects.get(slug=cat_slug)
		queryset= obj.video_set.all()
		context = {
					"obj" : obj, 
					"queryset" : queryset,
					
		
				  }
		return render(request,"category_detail.html", context)
   except:
        raise Http404