from django.urls import path
from rest_api.views.doc_users import DoctorUsersView
from rest_api.views.client_users import ClientUsersView

urlpatterns = [
    path("api/v1/doctors/users/", DoctorUsersView.as_view()),
    path("api/v1/client/users/", ClientUsersView.as_view())
]