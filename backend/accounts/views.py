from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, login, authenticate
from django.conf import settings
from django.views import generic

from .forms import LoginForm, SignupForm


User = get_user_model()


def test(request):
    return render(request, 'public/welcome.html')


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Signed In')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if '__all__' in form.errors:
            messages.warning(self.request, 'Invalid username or password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(self.request, f'{field.capitalize()}: {error}')

        return super().form_invalid(form)
    

class LogoutUserView(LogoutView):
    next_page = reverse_lazy(settings.LOGOUT_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You've been logged out.")
        return super().dispatch(request, *args, **kwargs)
    

class SignupUserView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('accounts:test')
    template_name = 'accounts/signup.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:test')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        user = authenticate(
            request=self.request,
            username=self.object.username,
            password=form.cleaned_data.get('password1')
        )

        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Signed Up')

        return response
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f'{field.capitalize()}: {error}')

        return super().form_invalid(form)

