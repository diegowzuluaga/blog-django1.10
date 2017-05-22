from __future__ import unicode_literals
from django.conf import settings 
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone 
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from markdown_deux import markdown
from comments.models import Comment
from .utils import get_read_time

# Create your models here.

#Post.objects.all()
#Post.objects.create(user=user, title="un titulo")
class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user         = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	titulo       = models.CharField(max_length=150)
	slug         = models.SlugField(unique=True)
	imagen       = models.ImageField(upload_to=upload_location, 
					null=True, 
					blank=True,
					height_field="height_field",
					width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field  = models.IntegerField(default=0)
	contenido    = models.TextField()
	draft        = models.BooleanField(default=False)
	publish      = models.DateField(auto_now=False, auto_now_add=False)
	read_time    = models.IntegerField(default=0)
	timestamp    = models.DateTimeField(auto_now_add=True, auto_now=False)
	actualizado  = models.DateTimeField(auto_now_add=False, auto_now=True)

	objects      = PostManager()

	def __unicode__(self):	#Python 2
		return self.titulo

	def __str__(self):		#Python 3
		return self.titulo

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-timestamp", "-actualizado"] 

	def get_markdown(self):
		contenido = self.contenido
		return mark_safe(markdown(contenido))
	
	@property	
	def comments(self):
		instance = self
		qs       = Comment.objects.filter_by_instance(instance)
		return qs

	@property	
	def get_content_type(self):
		instance     = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance, new_slug=None):
	slug = slugify(instance.titulo)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs): 
	if not instance.slug:
		instance.slug      = create_slug(instance)
	if instance.contenido:	
		html_string        = instance.get_markdown()
		read_time_var      = get_read_time(html_string)
		instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)