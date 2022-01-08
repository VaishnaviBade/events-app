from django.db import models

from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Event(models.Model):
    """
    Description:
        -Name
        -Event Description
        -Date Time Event held
        -Location (text field)
        -image
        -people liked
        -created by user
    """

    name = models.CharField("Name Of Event", max_length=150)
    description = models.TextField("Describe Your Event", max_length=500)
    location = models.CharField("Location Of Event", max_length=150)
    image = models.ImageField("Event Image", upload_to="event_images")
    like_people = models.ManyToManyField(User, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_events"
    )
    time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100)

    def get_number_like(self):
        return self.like_people.all().count()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name[:100]) + f"{self.id}-{self.created_by.id}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)
