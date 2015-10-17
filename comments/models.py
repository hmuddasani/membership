from django.db import models
from signup.models import MyUser
from videos.models import Video
from django.core.urlresolvers import reverse
# Create your models here.
class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager, self).filter(parent=None)
		
	def create_comment(self, user=None, path=None, video=None, text=None, parent=None):
 
		if not user:
				raise ValueError('Users must have be logged in')
		if not path:
				raise ValueError('Users must have a path')
		
		comment = self.model(
							user = user, 
							path = path,
							text = text,
				)
		if video is not None:
				comment.video = video
		if parent is not None:
				comment.parent = parent
		comment.save(using=self._db)
		return comment
	
class Comment(models.Model):
	user = models.ForeignKey(MyUser)
	text = models.TextField()
	parent = models.ForeignKey("self", null =True)
	path = models.CharField(max_length=500)
	video = models.ForeignKey(Video, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	objects = CommentManager()
	
	def __unicode__(self):
		return self.text
    
	@property
	def get_origin(self):
		return self.path
    
	@property
	def get_comment(self):
		return self.text
    
	@property
	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False
	
	def get_children(self):
		if self.is_child:
			return None
		else:
			return Comment.objects.filter(parent=self)
	
	
	def get_absolute_url(self):
		return reverse('comment_thread', kwargs={"id": self.id})	