from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


def user_picture_path(instance, filename):
    """
    Called when the profile is updated with an image. Supplies the correct
    path to save the user photo.
    """
    return f"user_{instance.id}/{filename}"


class Team(models.Model):
    """
    Students are grouped into teams so members can reach out to one another width
    help on the course material.
    """

    name = models.CharField(max_length=50)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    The profile keeps the student details apart from the auth concerns of the basic
    django user model. Some of the profile fields must be filled in by the course
    runner while others must be completed by the student once they are enrolled.

    These two states of incompletion are represented by the two first bool fields.
    All other fields simply represent the facts that the student may or may not
    want to share.
    """

    course_runner_complete: models.BooleanField = models.BooleanField(default=False)
    user_completed: models.BooleanField = models.BooleanField(default=False)

    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default="default.png", upload_to=user_picture_path
    )

    roles = ((1, "Student"), (2, "Mentor"), (3, "Instructor"))

    role = models.PositiveSmallIntegerField(choices=roles, null=True, blank=True)
    pronouns = models.CharField(max_length=15)
    team = models.ForeignKey("Team", null=True, on_delete=models.SET_NULL)
    buddy = models.ManyToManyField("self", blank=True)

    def save(self, *args, **kwargs) -> None:
        """
        Save the profile as usual but resize the image and save it to the
        appropriate path.
        """
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def get_absolute_url(self) -> str:
        return reverse("users:detail", args=[str(self.user.pk)])


@receiver(post_save, sender=User, dispatch_uid="irrelevant")
def create_profile(sender, instance, created, **kwargs) -> None:
    """
    Creates a new profile any time a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)
