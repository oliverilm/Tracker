import datetime

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Create your views here.
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, DetailView

from Tracker.models import CheckIn, UserInProject, Project


class IndexView(LoginRequiredMixin, CreateView):
    template_name = "index.html"
    queryset = None
    model = CheckIn
    fields = ("project", )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        active_checkins = CheckIn.objects.filter(user=user).filter(is_active=True)
        if len(active_checkins) > 0:
            print(active_checkins)
            context["working"] = False
            context["value"] = "End work"
            context["project"] = active_checkins[0]
        else:
            context["working"] = True
            context["value"] = "Start work"

        context["my_checkins"] = CheckIn.objects.filter(user=self.request.user)
        context["total_hours"] = 0
        context["projects_with_hours"] = 0

        return context

    def post(self, request, *args, **kwargs):
        active_checkins = CheckIn.objects.filter(user=self.request.user).filter(is_active=True)
        if len(active_checkins) > 0:
            checkin = active_checkins[0]
            checkin.stop = datetime.datetime.now()
            checkin.total_hours = 1
            checkin.is_active = False
            checkin.save()
            print(active_checkins[0].is_active)

        else:
            proj = Project.objects.get(pk=self.request.POST.get("project"))
            checkin = CheckIn(
                project=proj,
                user=self.request.user,
                start=datetime.datetime.now(),
                is_active=True
            )
            checkin.save()
        return HttpResponseRedirect("/")
