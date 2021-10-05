from django.shortcuts import render
from .models import Portfolio, Project, Contact


def portfolio(request, portfolio_name):
    data = {
        'portfolio': Portfolio.objects.get(link=portfolio_name),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(link=portfolio_name)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(link=portfolio_name))
    }

    return render(request, 'main/portfolio.html', data)


def home(request):
    return render(request, 'main/home.html')
