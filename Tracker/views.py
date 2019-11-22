import datetime

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Create your views here.
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, DetailView, ListView

from Tracker.models import CheckIn, UserInProject, Project

class IndexView(LoginRequiredMixin, CreateView):
    template_name = "index.html"
    model = CheckIn
    fields = ("project", )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        proj_dict = []
        active_checkins = CheckIn.objects.filter(user=user).filter(is_active=True)
        if len(active_checkins) > 0:
            context["working"] = False
            context["value"] = "End work"
            context["project"] = active_checkins[0]
        else:
            context["working"] = True
            context["value"] = "Start work"


        context["my_checkins"] = CheckIn.objects.filter(user=self.request.user).order_by("-pk")
        context["total_hours"] = self.calc_hours()
        context["projects_count"] = len(UserInProject.objects.filter(user=self.request.user))
        context["my_projects"] = self.get_dict_with_proj_and_hours()
        context["projects_with_hours"] = 0

        return context

    def post(self, request, *args, **kwargs):

        active_checkins = CheckIn.objects.filter(user=self.request.user).filter(is_active=True)
        if len(active_checkins) > 0:
            checkin = active_checkins[0]
            checkin.stop = datetime.datetime.now()

            a = checkin.start
            time = datetime.datetime.now() - datetime.datetime(a.year, a.month, a.day, a.hour, a.minute, a.second)
            hours = time.seconds / 3600
            checkin.total_hours = str(hours)[:6]
            checkin.is_active = False
            checkin.save()
        else:
            try:
                proj = Project.objects.get(pk=self.request.POST.get("sel"))
                checkin = CheckIn(
                    project=proj,
                    user=self.request.user,
                    start=datetime.datetime.now(),
                    is_active=True
                )
                checkin.save()
            except Exception as e:
                pass
        return HttpResponseRedirect("/")

    def calc_hours(self):
        hours = 0
        checkins = CheckIn.objects.filter(user=self.request.user)
        for i in checkins:
            if not i.is_active:
                hours += float(i.total_hours[:6])
        return hours

    def get_dict_with_proj_and_hours(self):
        proj_dict = {}
        for p in UserInProject.objects.filter(user=self.request.user):
            hours = 0
            for c in CheckIn.objects.filter(user=self.request.user).filter(project=p.project):
                if not c.is_active:
                    hours += float(c.total_hours[:6])
            proj_dict[p.project] = hours
        return proj_dict


class SummaryView(LoginRequiredMixin, ListView):
    model = CheckIn
    template_name = "summary.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().get(request, kwargs)
        return HttpResponseRedirect("/")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["total_hours"] = str(sum([float(c.total_hours[:6]) for c in CheckIn.objects.filter(is_active=False)]))[:6]
        context["currently_working"] = CheckIn.objects.filter(is_active=True)
        return context