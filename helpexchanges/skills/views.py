from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView

from .models import Activity
from .forms import SkillForm


class IndexView(TemplateView):
    template_name = "skills/index.html"
    context_object_name = "activity_list"

    def get_queryset(self):
        """
        Return the queryset that should be shown to the user

        """
        return Activity.objects.order_by("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Skills Exchange"

        return context

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

