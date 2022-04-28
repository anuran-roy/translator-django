from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scripts import translate, scrape, parser
from typing import List

# Create your views here.
def index(request) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the translator index.")


def translate_sample(request) -> HttpResponse:
    data: string = scrape.scrape_summary("India")
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

def translate(request):
    if request.method == "GET":
        return HttpResponse("Translation Page!")
    # elif request.method == "POST":
    #     data: string = request.POST.get("")