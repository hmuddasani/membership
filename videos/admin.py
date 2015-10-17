from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Video
from .models import Category
from .models import TaggedItem

class TaggedItemInline(GenericTabularInline):
	model = TaggedItem
	
class VideoAdmin(admin.ModelAdmin):
   inlines = [TaggedItemInline]
   list_display=['__unicode__', 'slug']
   fields = ['title', 'slug','embed_code', 'active',
            'featured', 'free_preview', 'category']
   class Meta:
      model = Video
   
   prepopulated_fields={
                        'slug' : ["title"],
						}
admin.site.register(Video, VideoAdmin)
admin.site.register(Category)
admin.site.register(TaggedItem)

# Register your models here.
 