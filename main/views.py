from django.shortcuts import render, redirect
from .models import Portfolio, Project, Contact
from django.contrib import messages
from .forms import UserRegistration
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from .serializers import PortfolioSerializer, ProjectSerializer, ContactSerializer
from .permissions import PortfolioUserPermission, ProjectContactUserPermission


class UserPortfolioListView(generics.ListAPIView):
    """Get list of user portfolios"""
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(user=user.pk)


class PortfolioCreateView(generics.CreateAPIView):
    """
    Create portfolio
    If you trying to create portfolio you don't have to send 'id' field in request
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        user = self.request.user
        self.request.data['user'] = str(user.id)
        kwargs['data'] = self.request.data
        return serializer_class(user, *args, **kwargs)


class PortfolioView(generics.RetrieveUpdateDestroyAPIView):
    """Get, Update, Delete portfolio"""
    permission_classes = [IsAuthenticatedOrReadOnly, PortfolioUserPermission]
    serializer_class = PortfolioSerializer
    lookup_field = 'link'
    queryset = Portfolio.objects.all()


class ProjectCreateView(generics.CreateAPIView):
    """Create project"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer


class ProjectUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Update or remove project"""
    permission_classes = [IsAuthenticated, ProjectContactUserPermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ContactCreateView(generics.CreateAPIView):
    """Create contact"""
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer


class ContactUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Update or remove contact"""
    permission_classes = [IsAuthenticated, ProjectContactUserPermission]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


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


# function for creating a portfolio, it creates portfolio with default values
# and redirects to change_about_me page
@login_required
def create_portfolio(request):
    obj = Portfolio.objects.create(user=request.user)
    return redirect('change_about_me', pk=obj.pk)


# function for change portfolio. It shows already created project and contacts
# that can be changed, and have links for creating new projects and new contacts
@login_required
def change_portfolio(request, slug):

    # checking if the user matches the portfolio owner
    if Portfolio.objects.get(link=slug).user != request.user:
        return HttpResponseForbidden()

    data = {
        'portfolio': Portfolio.objects.get(link=slug),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
    }
    return render(request, 'main/change_portfolio.html', data)


# class view for changing about_me part of portfolio information
class UpdateAboutMe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Portfolio
    fields = ['image', 'header', 'about_me', 'link']
    template_name = 'main/change_create_template.html'

    # checking if the user matches the portfolio owner
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

    # context for using one template for all update views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change about me'
        context['header'] = 'Change'
        context['button_text'] = 'Save'
        return context


# class view for changing project information
class UpdateProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/change_create_template.html'

    # checking if the user matches the portfolio owner
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)

    # context for using one template for all update views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change project'
        context['header'] = 'Change project'
        context['button_text'] = 'Save'
        return context


# class view for changing contact information
class UpdateContact(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/change_create_template.html'

    # checking if the user matches the portfolio owner
    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.portfolio.user:
            return True
        else:
            return False

    def form_valid(self, form):
        self.success_url = '/change_portfolio/' + form.instance.portfolio.link + '/'
        return super().form_valid(form)

    # context for using one template for all update views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change contact'
        context['header'] = 'Change contact'
        context['button_text'] = 'Save'
        return context


# class view for creating project
class CreateProject(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['image', 'name', 'description', 'project_link']
    template_name = 'main/change_create_template.html'

    # checking if the user matches the portfolio owner
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

    # context for using one template for all create views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create project'
        context['header'] = 'Create project'
        context['button_text'] = 'Create'
        return context


# class view for creating project
class CreateContact(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Contact
    fields = ['logo', 'social_network', 'link']
    template_name = 'main/change_create_template.html'

    # checking if the user matches the portfolio owner
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

    # context for using one template for all create views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create contact'
        context['header'] = 'Create contact'
        context['button_text'] = 'Create'
        return context


# class view for deleting project
class DeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'main/delete_template.html'

    # checking if the user matches the portfolio owner
    def test_func(self):
        project = self.get_object()
        self.success_url = '/change_portfolio/' + project.portfolio.link + '/'
        if self.request.user == project.portfolio.user:
            return True
        return False

    # context for using one template for all delete views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['title'] = 'Delete project'
        context['header'] = 'Are you sure you want to delete the project?'
        context['link_back'] = '/change_portfolio/' + project.portfolio.link + '/'
        return context


# class view for deleting contact
class DeleteContact(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    template_name = 'main/delete_template.html'

    # checking if the user matches the portfolio owner
    def test_func(self):
        contact = self.get_object()
        self.success_url = '/change_portfolio/' + contact.portfolio.link + '/'
        if self.request.user == contact.portfolio.user:
            return True
        return False

    # context for using one template for all delete views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['title'] = 'Delete contact'
        context['header'] = 'Are you sure you want to delete the contact?'
        context['link_back'] = '/change_portfolio/' + project.portfolio.link + '/'
        return context


# class view for deleting portfolio
class DeletePortfolio(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'main/delete_template.html'
    success_url = '/profile/'

    # context for using one template for all delete views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete portfolio'
        context['header'] = 'Are you sure you want to delete the portfolio?'
        context['link_back'] = '/profile/'
        return context


# view that shows all portfolios created by the user
@login_required
def profile(request):
    data = {
        'portfolios': Portfolio.objects.filter(user=request.user)
    }
    return render(request, 'main/profile.html', data)
