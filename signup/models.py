from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from notifications.signals import notify


class MyUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
	   if not email:
				raise ValueError('Users must have an email address')
	   if not username:
				raise ValueError('Users must have an UserName')
	   user = self.model( 
							email=self.normalize_email(email),
							username = username,
						)
	   user.set_password(password)
	   user.save(using=self._db)
	   return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
			"""
        user = self.create_user(email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True,)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return str(self.email)+ " "+ str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
		

		
class UserProfile(models.Model):
	user = models.OneToOneField(MyUser)
	bio = models.TextField(max_length=500, blank=True)
	facebook_link = models.CharField(max_length=500,
							verbose_name='Facebook Profile URL',
							null=True,
							blank=True)
							
	def __unicode__(self):
	    return self.user.username


class SignUp(models.Model):
   name = models.CharField(max_length=120, blank=False)
   email= models.EmailField()
   
   def __unicode__(self):
      return str(self.name)+ " " + str(self.email)
	  
def new_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
		notify.send(instance, 
					recipient=MyUser.objects.get(username='user1'), #admin user
					verb='New user created.')
		# merchant account customer id -- stripe vs braintree
		# send email for verifying user email

post_save.connect(new_user_receiver, sender=MyUser)	  
