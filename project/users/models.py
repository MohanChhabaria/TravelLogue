from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete


class UserProfile(models.Model):
    
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=20, unique=True, null=False)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    # country = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    is_verified = models.BooleanField(default=False)
    user_image = models.ImageField(default='default.jpg', upload_to='user_images')
    registration_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
    

class UserFollowing(models.Model):

    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"
    


def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()


post_delete.connect(delete_user, sender=UserProfile)