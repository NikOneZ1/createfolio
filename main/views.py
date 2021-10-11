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
    print(obj.link)
    return redirect(change_portfolio, slug=obj.link)


@login_required
def change_portfolio(request, slug):

    if Portfolio.objects.get(link=slug).user != request.user:
        return HttpResponseForbidden()

    data = {
        'portfolio': Portfolio.objects.get(link=slug),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=slug))
    }
    return render(request, 'main/change_portfolio.html', data)


class UpdateChangeMe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    fields = ['image', 'header', 'about_me', 'link']
    template_name = 'main/change_about_me.html'

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


class UpdateProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/change_project.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)


class UpdateContact(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/change_contact.html'

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)


class CreateProject(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/create_project.html'

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


class CreateContact(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/create_contact.html'

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


class DeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'main/delete_project.html'

    def test_func(self):
        project = self.get_object()
        self.success_url = '/change_portfolio/' + project.portfolio.link + '/'
        if self.request.user == project.portfolio.user:
            return True
        return False
