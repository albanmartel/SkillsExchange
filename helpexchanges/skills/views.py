from django.shortcuts import render
from django.views import generic

class IndexView(generic.ListView):
    template_name = "skills/index.html"
    context_object_name = "latest_question_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Skills Exchange"
