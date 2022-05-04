from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scripts import translate, scrape, parser
from typing import List, Dict, Tuple, Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from worker.models import Project, Sentence
from worker.forms.forms import TranslationForm, UserAuthForm
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.utils.timezone import now

# Create your views here.
@login_required
def index(request) -> HttpResponse:
    # return HttpResponse("Hello, world. You're at the translator index.")
    return render(request, "pages/home.html")


@login_required
def translate_sample(request) -> HttpResponse:
    data: str = scrape.scrape_summary("India")
    parsed_data: List[str] = (
        parser.parse(to_parse=data, lang="en") if data != "ERROR!" else "ERROR!"
    )

    translated_strings: List[str] = []

    for i in parsed_data[:1]:
        translated_string: str = (
            translate.use_just_translated(sentence=i, to="fr", src="en")
            if i != "ERROR!"
            else "ERROR!"
        )

        translated_strings += [translated_string]

    # return HttpResponse(translated_strings.join("\n"))
    print(type(parsed_data))
    # print(parsed_data)
    print(translated_strings)
    return HttpResponse("<br>".join(translated_strings))


@login_required
def view_project(request, project_pk: int) -> HttpResponse:
    return HttpResponse("Project Page!")


@receiver(post_save, sender=Project)
def process_input(sender, instance, **kwargs) -> Any:
    try:
        print("\n\nprocess_input() triggered!\n\n")
        wiki_title: str = instance.wiki_title
        print(f"wiki_title = {wiki_title}")
        data: str = scrape.scrape_summary(title=wiki_title)
        print(f"wiki_data = {data}")

        print("\nParsing the current project's data...\n")

        parsed_data: List[str] = (
            parser.parse(to_parse=data, lang="en") if data != "ERROR!" else "ERROR!"
        )

        print(f"Parsed Data = {parsed_data}")
        newProject = instance

        for i in parsed_data:
            newSentence = Sentence(
                project_id=newProject,
                original_sentence=i,
                translated_sentence="",
                accessible_to=instance.accessible_to,
            )
            newSentence.save()

        # return newProject
    except Exception as e:
        print(f"Error occured. Details: {e}")


@login_required
def create_project(request) -> HttpResponse:
    if request.method == "POST":
        try:
            project: Project = Project.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                language=request.POST.get("language"),
                accessible_to=request.user,
            )

            project.save()
        except Exception as e:
            return HttpResponse(f'An Exception Occured: "{e}"')
    elif request.method == "GET":
        return render(
            request, "pages/create_project.html", {form: TranslationForm(request.POST)}
        )


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = TranslationForm
    template_name: str = "pages/create_project.html"
    success_url: str = "/"

    def form_valid(self, form):
        print("form_valid invoked!")
        self.object = form.save(commit=False)
        self.object.accessible_to = self.request.user
        print(f"Now it's accessible to : {self.request.user}")
        
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    success_url: str = "/projects/"
    template_name: str = "pages/delete_project.html"

class ListProjects(LoginRequiredMixin, ListView):
    model = Project
    template_name: str = "pages/projects_list.html"
    queryset = Project.objects.all()
    # fields = (
    #     "__all__"
    # )
    context_object_name = "projects"
    paginate_by: int = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            return Project.objects.filter(accessible_to=self.request.user)


@login_required
def get_project_details(request, project_pk: int) -> HttpResponse:
    sentences = Sentence.objects.filter(project_id=project_pk).filter(accessible_to=request.user)
    project = (
        Project.objects.filter(id=project_pk).filter(accessible_to=request.user).first()
    )

    if project is None:
        return render(request, 'pages/404.html')
    else:
        return render(
            request,
            "pages/project_details.html",
            {
                "sentences": sentences,
                "project": project,
            },
        )


@login_required
def modify_translation(request, project_pk: int) -> HttpResponse:
    if request.method == "POST":
        # try:
        sentences = Sentence.objects.filter(project_id=project_pk)

        for i in sentences:
            sentence_item = request.POST.get(f"sentence-{i.id}")
            i.translated_sentence = sentence_item

            i.save()
            # print(request.__dict__)

        # except Exception as e:
        # print(e)

    return HttpResponseRedirect(f"/projects/")


class UserLogin(LoginView):
    template_name = "pages/login.html"
    form_class = UserAuthForm

    def get_success_url(self):
        return "/"
