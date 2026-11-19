from django.urls import path

from .views import SignUpView, AccountEditView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit/", AccountEditView.as_view(), name="account_edit"),
]
