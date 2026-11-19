from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .models import CustomUser
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class AccountEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username", "email", "zip"]
    template_name = "accounts/account_edit.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user