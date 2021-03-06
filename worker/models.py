from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

choices = (
    ("bn", "Bengali"),
    ("gu", "Gujarati"),
    ("hi", "Hindi"),
    ("kn", "Kannada"),
    ("ml", "Malayalam"),
    ("mr", "Marathi"),
    ("ne", "Nepali"),
    ("or", "Oriya"),
    ("pa", "Panjabi"),
    ("si", "Sinhala"),
    ("ta", "Tamil"),
    ("te", "Telugu"),
    ("ur", "Urdu"),
)


# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    wiki_title = models.CharField(max_length=500, default="Unknown")
    target_lang = models.CharField(max_length=255, choices=choices)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(default=now)
    accessible_to = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE
    )  # , symmetrical=False)

    def __str__(self):
        return f"{self.id} - Translation of {self.wiki_title} to {self.target_lang}"

    class Meta:
        ordering = (
            "-modified_on",
            "-created_on",
        )


class Sentence(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    original_sentence = models.TextField(blank=True)
    translated_sentence = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    accessible_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"Sentence of project {self.project_id}"

    class Meta:
        ordering = ("created_on",)
