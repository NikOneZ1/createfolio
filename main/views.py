from django.shortcuts import render, redirect
from .models import Portfolio, Project, Contact
from django.contrib import messages
from .forms import UserRegistration


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
            messages.success(request, f'User {username} has been created!')
            #return redirect('login')
            return redirect('home')
        else:
            messages.error(request, f'Nope')

    else:
        form = UserRegistration()
    return render(request, 'main/registration.html', {'form': form, 'title': 'Registration'})