from django.shortcuts import render, redirect
from .models import Portfolio, Project, Contact
from django.contrib import messages
from .forms import UserRegistration
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden


def portfolio(request, portfolio_name):
    data = {
        'portfolio': Portfolio.objects.get(link=portfolio_name),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=portfolio_name)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=portfolio_name))
    }

    return render(request, 'main/portfolio.html', data)


def home(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User {username} has been created! You can login now.')
            return redirect('login')
        else:
            messages.error(request, f'Nope')

    else:
        form = UserRegistration()
    return render(request, 'main/registration.html', {'form': form, 'title': 'Registration'})


@login_required
def create_portfolio(request):
    obj = Portfolio.objects.create(user=request.user)
    return redirect('change_about_me', pk=obj.pk)


@login_required
def change_portfolio(request, slug):

    if Portfolio.objects.get(link=slug).user != request.user:
        return HttpResponseForbidden()

    data = {
        'portfolio': Portfolio.objects.get(link=slug),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
    }
    return render(request, 'main/change_portfolio.html', data)


class UpdateAboutMe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    fields = ['image', 'header', 'about_me', 'link']
    template_name = 'main/change_create_template.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.user:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.success_url = '/change_portfolio/' + form.instance.link + '/'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change about me'
        context['header'] = 'Change'
        context['button_text'] = 'Save'
        return context


class UpdateProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/change_create_template.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change project'
        context['header'] = 'Change project'
        context['button_text'] = 'Save'
        return context


class UpdateContact(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/change_create_template.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change contact'
        context['header'] = 'Change contact'
        context['button_text'] = 'Save'
        return context


class CreateProject(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/change_create_template.html'

    def test_func(self):
        portfolio = Portfolio.objects.get(link=self.kwargs['slug'])
        if self.request.user == portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.portfolio = Portfolio.objects.get(link=self.kwargs['slug'])
        self.success_url = '/change_portfolio/' + self.kwargs['slug'] + '/'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create project'
        context['header'] = 'Create project'
        context['button_text'] = 'Create'
        return context


class CreateContact(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/change_create_template.html'

    def test_func(self):
        portfolio = Portfolio.objects.get(link=self.kwargs['slug'])
        if self.request.user == portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.portfolio = Portfolio.objects.get(link=self.kwargs['slug'])
        self.success_url = '/change_portfolio/' + self.kwargs['slug'] + '/'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create contact'
        context['header'] = 'Create contact'
        context['button_text'] = 'Create'
        return context


class DeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'main/delete_template.html'

    def test_func(self):
        project = self.get_object()
        self.success_url = '/change_portfolio/' + project.portfolio.link + '/'
        if self.request.user == project.portfolio.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['title'] = 'Delete project'
        context['header'] = 'Are you sure you want to delete the project?'
        context['link_back'] = '/change_portfolio/' + project.portfolio.link + '/'
        return context


class DeleteContact(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    template_name = 'main/delete_template.html'

    def test_func(self):
        contact = self.get_object()
        self.success_url = '/change_portfolio/' + contact.portfolio.link + '/'
        if self.request.user == contact.portfolio.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['title'] = 'Delete contact'
        context['header'] = 'Are you sure you want to delete the contact?'
        context['link_back'] = '/change_portfolio/' + project.portfolio.link + '/'
        return context


class DeletePortfolio(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'main/delete_template.html'
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete portfolio'
        context['header'] = 'Are you sure you want to delete the portfolio?'
        context['link_back'] = '/profile/'
        return context


@login_required
def profile(request):
    data = {
        'portfolios': Portfolio.objects.filter(user=request.user)
    }
    return render(request, 'main/profile.html', data)
