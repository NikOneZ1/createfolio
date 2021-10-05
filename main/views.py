from django.shortcuts import render
from .models import Portfolio, Project, Contact


def home(request):
    data = {
        'portfolio': Portfolio.objects.get(user=request.user),
        'projects': Project.objects.filter(portfolio=Portfolio.objects.get(user=request.user)),
        'contacts': Contact.objects.filter(portfolio=Portfolio.objects.get(user=request.user))
    }

    return render(request, 'main/home.html', data)
