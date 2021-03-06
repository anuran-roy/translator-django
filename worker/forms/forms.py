from django import forms
from worker.models import Project, Sentence

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class TranslationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["wiki_title"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["target_lang"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"

    class Meta:
        model = Project
        fields = ("wiki_title", "target_lang")


class UserAuthForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

        self.fields["username"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["password"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
