from rest_framework import serializers
from .models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "phone_Number",  "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating the user
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "image", "phone_Number", "address", "is_admin", 'is_active']

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("email", "name", "image", "phone_Number", "address")

    def validate_email(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError("You don't have permission to update this user.")

        # Update fields based on the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_Number = validated_data.get('phone_Number', instance.phone_Number)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance

    
class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['current_password', 'password', 'password2']

    def validate(self, attrs):
        user = self.context.get('user')
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Validate current password
        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        # Validate new passwords
        if password != password2:
            raise serializers.ValidationError({"password": "New passwords must match."})

        return attrs

    def save(self):
        user = self.context.get('user')
        user.set_password(self.validated_data['password'])
        user.save()


import logging

logger = logging.getLogger(__name__)

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')

        # Check if the user with the provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('You are not a Registered User')

        # Encode user ID and generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        logger.debug(f'Encoded UID: {uid}')
        logger.debug(f'Password Reset Token: {token}')

        # Construct the password reset link
        link = f'http://localhost:3000/apiv1/user/reset/{uid}/{token}'
        logger.debug(f'Password Reset Link: {link}')

        # Send email
        body = f'Click the following link to reset your password: {link}'
        data = {
            'subject': 'Reset Your Password',
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)

        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      email = self.context.get('email')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      uid = force_str(urlsafe_base64_decode(email))
      user = User.objects.get(pk=uid)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class EventSerializer(serializers.ModelSerializer):
    Event_End = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    Event_Time = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = Event
        fields = '__all__'

class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = country
        fields = '__all__'


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'

class scholarshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = scholarships
        fields = '__all__'

class Pathways_ScholarshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathways_Scholarships
        fields = '__all__'


class AvailableCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = available_courses
        fields = '__all__'


class degreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = degree
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    available_courses = AvailableCoursesSerializer(many=True)
    degree = degreeSerializer(many=True)

    class Meta:
        model = university
        fields = '__all__'
    
    def create(self, validated_data):
        courses_data = validated_data.pop('available_courses')
        degrees_data = validated_data.pop('Degree')

        university_instance = university.objects.create(**validated_data)

        for course_data in courses_data:
            course, created = available_courses.objects.get_or_create(**course_data)
            university_instance.available_courses.add(course)

        for degree_data in degrees_data:
            degree, created = degree.objects.get_or_create(**degree_data)
            university_instance.Degree.add(degree)

        university_instance.save()
        return university_instance
    
    def update(self, instance, validated_data):
        courses_data = validated_data.pop('available_courses', None)
        degrees_data = validated_data.pop('Degree', None)
        
        instance.University_Name = validated_data.get('University_Name', instance.University_Name)
        instance.About_University = validated_data.get('About_University', instance.About_University)
        instance.Entry_Requirements = validated_data.get('Entry_Requirements', instance.Entry_Requirements)
        instance.English_Requirements = validated_data.get('English_Requirements', instance.English_Requirements)
        instance.Tuition_Fees = validated_data.get('Tuition_Fees', instance.Tuition_Fees)
        instance.Why_This_University = validated_data.get('Why_This_University', instance.Why_This_University)

        instance.save()

        if courses_data is not None:
            instance.available_courses.clear()
            for course_data in courses_data:
                course, created = available_courses.objects.get_or_create(**course_data)
                instance.available_courses.add(course)

        if degrees_data is not None:
            instance.Degree.clear()
            for degree_data in degrees_data:
                degree, created = degree.objects.get_or_create(**degree_data)
                instance.Degree.add(degree)

        instance.save()
        return instance
    

class Appointment_time_slotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment_time_slot
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
    


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'topic', 'host', 'duration', 'start_time']