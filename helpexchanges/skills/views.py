from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    TemplateView,
    ListView,
)

from .models import (
    Activity,
    Assistance,
)
from .forms import (
    SkillForm,
)

why = """
Skills Exchange was created with a specific goal in mind: to popularize the exchange of free services in order to strengthen the spirit of solidarity throughout France. We aspire not only to make the exchange of free services more widespread, but also to make it the norm—a habit deeply rooted in the daily lives of the French people. The idea is simple: for certain services, instead of thinking about payment, we want to encourage the instinct to help one another and share.

We dream of a society where the exchange of knowledge, skills, and various forms of assistance would become the first option considered, even before monetary exchange.

We recognize that this approach may not be feasible for all services. However, it is important to emphasize that the potential for applying this model is much broader than one might initially think.

By fostering a spirit of solidarity, we also hope to build a tighter-knit network of local communities, where people know, support, and value one another.

Ultimately, our goal is to contribute to a more united and supportive society, where the exchange of free services becomes common practice, reflecting a sharing economy that enriches everyone.
"""

class AboutView(TemplateView):
    template_name = "skills/about.html"
    context_object_name = "activity_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "About Skills Exchange"
        context["objective"] = "connects individuals who want to help one another and exchange services"
        context["mission"] = why

        return context

class IndexView(ListView):
    model = Assistance
    template_name = "skills/index.html"
    context_object_name = "assistances"

def skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            # Create a new skill. It will be saved in the database
            form.save()
            # Instructs the browser to automatically navigate to
            # a different page once the form has been submitted,
            # to avoid duplicate entries.
            return redirect("skill_list")
    else:
        # in which case a blank form is inserted
        form = SkillForm()  # Formulaire vide

    context = {
        "form": form,
        # This variable is important for {{ title }} HTML template
        'title': "Add a skill",
    }

    return render(request, "skills/form.html", context)

