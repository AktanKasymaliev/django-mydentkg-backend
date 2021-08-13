from rest_api.views.views import CategoryListView, CommentAddView, \
     CommentsView, MakeReserveView, ReceptionAddView, ReceptionView, ReservedView
from django.urls import path
from rest_api.views.doc_users import (DoctorChangePasswordView,
                                     DoctorUsersView, DoctorUserRegisterView, 
                                     DoctorLoginView, DoctorForgotPasswordView)
from rest_api.views.client_users import (ClientChangePasswordView, 
                ClientForgotPasswordView, ClientUsersView, 
                ClientUserRegisterView, ClientLoginView)
from rest_api.activate import activate_client, activate_doctors, reset_password
from ratings.views import RatingAddView, RatingRemove


urlpatterns = [
    path("api/v1/doctors/users/", DoctorUsersView.as_view()),
    path("api/v1/doctors/user/create/", DoctorUserRegisterView.as_view()),
    path('api/v1/doctor/user/login/', DoctorLoginView.as_view()),
    path("api/v1/doctor/user/change/password/", DoctorChangePasswordView.as_view()),
    path("api/v1/doctor/user/reset/password/", DoctorForgotPasswordView.as_view()),
    path("api/v1/doctors/<str:category>/", CategoryListView.as_view()),

    path("api/v1/client/users/", ClientUsersView.as_view()),
    path("api/v1/client/user/create/", ClientUserRegisterView.as_view()),
    path('api/v1/client/user/login/', ClientLoginView.as_view()),
    path("api/v1/client/user/change/password/", ClientChangePasswordView.as_view()),
    path("api/v1/client/user/reset/password/", ClientForgotPasswordView.as_view()),
    path("api/v1/client/user/reset/password/<slug:uidb64>/<slug:token>/", reset_password, name='resetpassword'),

    path('api/v1/client/users/activate/<slug:uidb64>/<slug:token>/', activate_client, name='activate_client'),
    path('api/v1/doctors/users/activate/<slug:uidb64>/<slug:token>/', activate_doctors, name='activate_doctors'),

    path("api/v1/comments/", CommentsView.as_view()),
    path("api/v1/comments/add/", CommentAddView.as_view()),

    path("api/v1/receptions/", ReceptionView.as_view()),
    path("api/v1/reception/add/", ReceptionAddView.as_view()),
    path("api/v1/make/reserve/", MakeReserveView.as_view()),
    path("api/v1/reserves/", ReservedView.as_view()),

    path("api/v1/rating/add/", RatingAddView.as_view()),
    path("api/v1/rating/remove/<int:pk>/", RatingRemove.as_view()),
]