from django.db import models
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User

from profiles.models import Profile
from django.urls import reverse


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new',"New"
        IN_PROG = 'in_progress',"In Progress"
        COMP = 'complete',"Complete"

    subject = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='created')
    poster = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='tasks_posted')
    asignee = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='tasks_assigned', null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12,choices=Status.choices,
                              default=Status.NEW)
    ispushed = models.BooleanField(default=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject)
        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tasks:task_detail',
                       args=[self.pk,
                             self.slug])

    def get_possible_asignees(self):
        return User.objects.all().filter(groups__name='Second Line')

    def get_poster_profile(self):
        return get_object_or_404(Profile,user=self.poster_id)

    def get_asignee_profile(self):
        return get_object_or_404(Profile, user=self.asignee_id)

