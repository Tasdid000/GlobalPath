from django.urls import path
from .views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('update_profile/<str:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<email>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('event/', EventList.as_view()),
    path('event/<int:pk>/', EventDetail.as_view()),
    path('enquiry/feedback', EnquiryAPIView.as_view()),
    path('scholarships/', scholarshipsList.as_view()),
    path('pathways_Scholarships/', Pathways_ScholarshipsList.as_view()),
    path('university/', universityList.as_view()),
    path('university/<str:pk>/', universityDetail.as_view()),
    path('universities/search', UniversityListAPIView.as_view(), name='university-list-api'),
    path('video-conference-appointment/', VideoConferenceAppointmentView.as_view(), name='video-conference-appointment'),
    path('delete_Appointment/<int:id>/', delete_Appointment, name='delete_Appointment'),

    path('meetings/', MeetingListView.as_view(), name='meeting-list'),
    path('meetings/create/', CreateMeetingView.as_view(), name='create-meeting'),
]