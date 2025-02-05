from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import Buyer
from .models import Game


def main_page(request):

    title = 'Главная страница'

    context = {
        'title': title,
        }

    return render(request, 'main_page.html', context)


def shop(request):

    title = 'Игры'

    games = [
        'Atomic Heart',
        'Cyberpunk 2077',
        'PayDay 2'
        ]

    games = Game.objects.all()

    context = {
        'title': title,
        'games': games
        }

    return render(request, 'shop.html', context)


def cart(request):

    title = 'Корзина'

    description = 'Извините, ваша корзина пуста'

    context = {
        'title': title,
        'desc': description
        }

    return render(request, 'cart.html', context)


users = ['tom', 'ivan', 'mary']


def sign_up_by_django(request):

    context = {
        'info': {},
        'info_user': {
            'username': '',
            'password': '',
            'repeat_password': '',
            'age': ''
        }
    }
    buyers = [buyer.name for buyer in Buyer.objects.all()]
    if request.method == 'POST':
        form = UserRegister(request.POST)

        if form.is_valid():
            print('Form is valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            context['info_user']['username'] = username
            context['info_user']['password'] = password
            context['info_user']['repeat_password'] = repeat_password
            context['info_user']['age'] = age

            if (username not in buyers and
                password == repeat_password and
                int(age) >= 18):
                users.append(username)
                Buyer.objects.create(name=username, age=age)
                return HttpResponse(f'Приветствуем, {username}')

            elif password != repeat_password:
                context['info']['error'] = 'Пароли не совподают'
                return render(request, 'registration_page.html', context)

            elif int(age) <= 18:
                context['info']['error'] = 'Вы должны быть старше 18'
                return render(request, 'registration_page.html', context)

            elif username in users:
                context['info']['error'] = 'Пользователь уже существует'
                return render(request, 'registration_page.html', context)
    else:
        print('Form is not valid')
        form = UserRegister()

    context['form'] = form

    return render(request, 'registration_page.html', context)