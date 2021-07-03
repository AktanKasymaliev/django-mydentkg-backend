from django.urls import path
from rest_api.views.doc_users import DoctorUsersView, DoctorUserRegisterView
from rest_api.views.client_users import ClientUsersView, ClientUserRegisterView
from rest_api.activate import activate_client, activate_doctors

urlpatterns = [
    path("api/v1/doctors/users/", DoctorUsersView.as_view()),
    path("api/v1/doctors/user/create/", DoctorUserRegisterView.as_view()),

    path("api/v1/client/users/", ClientUsersView.as_view()),
    path("api/v1/client/user/create/", ClientUserRegisterView.as_view()),

    path('api/v1/client/users/activate/<slug:uidb64>/<slug:token>/', activate_client, name='activate_client'),
    path('api/v1/doctors/users/activate/<slug:uidb64>/<slug:token>/', activate_doctors, name='activate_doctors'),
]