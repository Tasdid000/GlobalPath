from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import Userrenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'User created successfully'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'User logged in successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_field_error': ['Invalid email or password']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [Userrenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    
class UserChangePasswordView(APIView):
    renderer_classes = [Userrenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'Password reset link sent successfully.'})

class UserPasswordResetView(APIView):
    renderer_classes = [Userrenderer]

    def post(self, request, email, token, format=None):
        serializer = UserPasswordResetSerializer(
        data=request.data, context={'email': email, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    

class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    

class EnquiryAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any user, authenticated or not

    def get(self, request, format=None):
        enquiry_list = Enquiry.objects.all()
        enquiry_serializers = EnquirySerializer(enquiry_list, many=True)
        return Response(enquiry_serializers.data)

    def post(self, request, format=None):
        enquiry_serializers = EnquirySerializer(data=request.data)
        if enquiry_serializers.is_valid():
            enquiry_serializers.save()
            return Response(enquiry_serializers.data, status=status.HTTP_201_CREATED)
        return Response(enquiry_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    


class scholarshipsList(generics.ListAPIView):
    queryset = scholarships.objects.all()
    serializer_class = scholarshipsSerializer

class Pathways_ScholarshipsList(generics.ListAPIView):
    queryset = Pathways_Scholarships.objects.all()
    serializer_class = Pathways_ScholarshipsSerializer


class universityList(generics.ListAPIView):
    queryset = university.objects.all()
    serializer_class = UniversitySerializer
    

class universityDetail(generics.RetrieveAPIView):
    queryset = university.objects.all()
    serializer_class = UniversitySerializer

from django_filters.rest_framework import DjangoFilterBackend
from .filters import UniversityFilter

class UniversityListAPIView(generics.ListAPIView):
    queryset = university.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UniversityFilter

class VideoConferenceAppointmentView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve all video conference appointments from the database
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Appointment(request, id):
    try:
        Appointments = Appointment.objects.get(id=id)
        Appointments.delete()
        return JsonResponse({'message': 'Appointment deleted successfully'}, status=204)
    except Appointment.DoesNotExist:
        return JsonResponse({'message': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    



# meetings/views.py
class CreateMeetingView(generics.CreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class MeetingListView(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]