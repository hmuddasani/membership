#import urllib2
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

#DEFAULT_MESSAGE= "MESSAGE IS"

# Create your models here.
class Video(models.Model):
	title = models.CharField(max_length=120)
	slug = models.SlugField(null=True, blank=True)
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	#share_message=models.TextField(default='DEFAULT_MESSAGE')
	tag = GenericRelation("TaggedItem", null = True, blank=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	free_preview = models.BooleanField(default=False)
	category = models.ForeignKey("Category", null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	
	class Meta:
		unique_together = ('slug','category')
		
	def __unicode__(self):
		return self.title
    
	def get_absolute_url(self):
		return reverse("video_detail", kwargs={"vid_slug": self.slug, "cat_slug": self.category.slug})
		

	#def get_share_message(self):
	#	return urllib2.quote(self.share_message)
  

def video_post_save_signal(sender, instance, created, *args, **kwargs):
	if created:
		slug_title = slugify(instance.title)
		new_slug = "%s %s %s" %(instance.title, instance.category.slug, instance.id)
		try:
			obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
			instance.slug = slugify(new_slug)
			instance.save()
			print "model exists, new slug generated"
		except Video.DoesNotExist:
			instance.slug = slug_title
			instance.save()
			print "slug and model created"
		except Video.MultipleObjectsReturned:
			instance.slug = slugify(new_slug)
			instance.save()
			print "multiple models exists, new slug generated"
		except:
			pass
		  
   
post_save.connect(video_post_save_signal, sender=Video)

class Category(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(max_length=5000, null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	tag = GenericRelation("TaggedItem", null = True, blank=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
	def __unicode__(self):
	    return self.title
    
	def get_absolute_url(self):
	     return reverse("category_detail", kwargs={"cat_slug": self.slug})
	   
TAG_CHOICES = (
				("python", "python"),
				("django","django"),
				)
class TaggedItem(models.Model):
	
	tag = models.SlugField(choices=TAG_CHOICES)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	
	def __unicode__(self):
		return self.tag
