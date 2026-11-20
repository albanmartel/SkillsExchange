from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

from .models import OfferActivity


class IndexView(TemplateView):
    template_name = "skills/index.html"

    def get_queryset(self):
        """
        Return the queryset that should be shown to the user

        """
        return OfferActivity.objects.order_by("")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Skills Exchange"

        return context

