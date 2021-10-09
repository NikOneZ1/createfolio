from django.shortcuts import render, redirect
from .models import Portfolio, Project, Contact
from django.contrib import messages
from .forms import UserRegistration
from django.contrib.auth.decorators import login_required


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
    data = {
        'portfolio': Portfolio.objects.get(link=slug),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=slug)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=slug))
    }
    return render(request, 'main/change_portfolio.html', data)
