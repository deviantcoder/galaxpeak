from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView

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
