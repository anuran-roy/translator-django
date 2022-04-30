from django.contrib import admin
from worker.models import Project, Sentence

# Register your models here.
admin.sites.site.register(Project)
admin.sites.site.register(Sentence)
