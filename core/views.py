from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView, FormView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from . import models, forms
# Create your views here.

class LoginView(FormView):
    template_name = "core/login.html"
    form_class = forms.LoginForm

    def post(self, request):
        form = forms.LoginForm(request.POST)
        # Verify if it needs to redirect to some page.
        next_page = request.POST.get('next')
        if next_page is None:
            next_page = 'core:home'

        # Validate the form.
        if not form.is_valid():
            messages.error(request, 'Invalid form')
            context = {'form': form}
            return render(request, 'core/login.html', context)

        username = form.cleaned_data["username"]
        password  = form.cleaned_data["password"]
        remember = form.cleaned_data["remember"]
        
        user = authenticate(request, username=username, password=password)

        # Check if authentication worked.
        if user is None:
            messages.error(request, 'Invalid username and/or password.')
            context = {'form': form}
            return render(request, 'core/login.html', context)

        # At this point the authentication was successful.    
        login(request, user) 

        # If remember is not selected, the session expires when the browser is
        # closed. The default value, defined in settings, is 24 hours.
        if not remember:
            request.session.set_expiry(0)

        return redirect(next_page)           


class LogoutView(TemplateView):
    template_name = "core/logout.html"    

    def get(self, request):
        logout(request)
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "core/home.html"

@method_decorator(login_required, name='dispatch')
class BoxCreateView(SuccessMessageMixin, CreateView):
    model = models.Box
    template_name = 'core/box/create.html'
    form_class = forms.BoxForm
    success_message = 'Box created successfuly.'
    success_url = reverse_lazy('core:box-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class BoxListView(ListView):
    model = models.Box
    template_name = 'core/box/list.html'
    context_object_name = 'boxes'
    paginate_by = 3
    ordering = '-pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user)

@method_decorator(login_required, name='dispatch')
class BoxEditView(UpdateView):
    model = models.Box
    template_name = 'core/box/edit.html'
    form_class = forms.BoxForm
    success_message = 'Box edited successfuly.'
    success_url = reverse_lazy('core:box-list')


class BoxVersionListView(ListView):
    model = models.BoxVersion
    template_name = 'core/box-version/list.html'
    context_object_name = 'box_versions'
    paginate_by = 3
    ordering = '-pk'

    def get(self, request, **kwargs):
        pk = kwargs.pop("pk")
        self.box = get_object_or_404(models.Box, pk=pk)
        return super().get(request, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box"] = self.box
        return context