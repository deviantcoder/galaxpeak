from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from .forms import LoginForm


def test(request):
    return render(request, 'public/welcome.html')


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = False # True

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
