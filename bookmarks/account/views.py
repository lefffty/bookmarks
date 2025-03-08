from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import LoginForm, UserRegistrationForm


User = get_user_model()


@login_required
def dashboard(request):
    context = {
        'section': 'dashboard',
    }
    return render(
        request,
        'account/dashboard.html',
        context,
    )


def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password2']
            )
            new_user.save()
            return render(
                request,
                'account/register_done.html',
                {
                    'new_user': new_user,
                }
            )
    else:
        form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {
            'user_form': form,
        }
    )


def user_login(request: HttpRequest):
    """
    Аутентификация пользователей по базе данных
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(
                request,
                username=cleaned_data['username'],
                password=cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User authenticated successfully!')
                else:
                    return HttpResponse('Disabled account!')
            else:
                return HttpResponse('Invalid login or password!')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(
        request,
        'account/login.html',
        context
    )
