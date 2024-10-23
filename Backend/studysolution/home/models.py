from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
#Create user manager
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone_Number, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc, password and password2.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_Number=phone_Number,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_Number , password=None):
        """
        Creates and saves a superuser with the given email, name, phone_Number and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone_Number=phone_Number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True, 
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    image = models.ImageField(upload_to='media/userimage', default=" ")
    name = models.CharField(max_length=255)
    phone_Number = models.CharField(max_length=11, default="")
    address = models.CharField(max_length=300, default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    crtate_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    objects = MyUserManager()
    email_verified  = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_Number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    Event_Image = models.ImageField(upload_to="media/Event/images", default ="")
    Event_Name = models.CharField(max_length=2000)
    Event_Venue = models.TextField()
    Organizer_Name = models.CharField(max_length=200)
    Organizer_Phone= models.CharField(max_length=11)
    Organizer_Email = models.EmailField(max_length=255)
    Event_start = models.DateField(null=False)
    Event_End = models.DateField(null=True, blank=True)
    Event_Time = models.CharField(max_length=255, null=True, blank=True)
    Event_Content = models.TextField()

class country(models.Model):
    country = models.CharField( primary_key=True,max_length=255)
    def __str__(self):
        return self.country

class available_courses(models.Model):
    course_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.course_name
    
class degree(models.Model):
    degree = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.degree

class university(models.Model):
    University_Name = models.CharField(max_length=500, primary_key=True)
    University_Image = models.ImageField(upload_to="media/university/images", default="")
    About_University = models.TextField(default="")
    country = models.ForeignKey(country, on_delete=models.CASCADE, null=False, blank=False, default="")
    Entry_Requirements = models.TextField(default="")
    English_Requirements = models.TextField(default="")
    Tuition_Fees = models.TextField(default="")
    available_courses = models.ManyToManyField(available_courses, related_name='universities')
    degree = models.ManyToManyField(degree, related_name='universities')
    Why_This_University = models.TextField(default="")

    def __str__(self):
        return self.University_Name

scholarship= (
    ('Undergraduate', 'Undergraduate'),
    ('Postgraduate', 'Postgraduate')
)
class scholarships(models.Model):
    id = models.AutoField(primary_key=True)    
    country = models.ForeignKey(country, on_delete=models.CASCADE, null=False, blank=False, default="")
    university_Name = models.CharField(max_length=255)
    scholarship = models.CharField(max_length=100, default='', choices=scholarship)
    scholarship_Name = models.CharField(max_length=1000)
    Percentage = models.CharField(max_length=1000)

class Pathways_Scholarships(models.Model):
    id = models.AutoField(primary_key=True)    
    country = models.ForeignKey(country, on_delete=models.CASCADE, null=False, blank=False, default="")
    scholarship_Name = models.CharField(max_length=1000)
    Percentage = models.CharField(max_length=1000)





Test = (
    ('IELTS', 'IELTS'),
    ('UKVI IELTS', 'UKVI IELTS'),
    ('Pearson', 'Pearson'),
    ('TOEFL', 'TOEFL'),
    ('Other', 'Other'),
    ('No', 'No'),
)

Purpose = (
    ('Language Course', 'Language Course'),
    ('Undergraduate', 'Undergraduate'),
    ('Postgraduate', 'Postgraduate'),
)

class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=500)
    Date_of_Birth = models.DateField(blank=False, auto_now=False)
    phone_Number= models.CharField(max_length=11, blank= False)
    Study_Destination = models.ForeignKey(country, on_delete=models.CASCADE, null=False, blank=False, default="")
    Interested = models.CharField(max_length=100, default='', choices=Purpose)
    Course_Title = models.CharField(max_length=1000)
    Work_Experience = models.CharField(max_length=255, null=True, blank=True)
    English_Test = models.CharField(max_length=100, default='', choices=Test)
    English_Test_Results = models.CharField(max_length=300, null=True, blank=True)
    Message = models.TextField()

class Appointment_time_slot(models.Model):
    time = models.CharField(max_length=10, primary_key=True)
    
    def __str__(self):
        return self.time
    
class Appointment(models.Model):
    id= models.AutoField(primary_key=True)
    Name = models.CharField(max_length=2000, default="")
    phone_Number = models.CharField(max_length=11)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default="")
    degree = models.ForeignKey(degree, on_delete=models.CASCADE, null=False, blank=False, default="")
    Date = models.DateField()
    Time = models.ForeignKey(Appointment_time_slot, on_delete=models.CASCADE, null=False, blank=False, default="")
    link = models.CharField(max_length=3000, default='')


class Meeting(models.Model):
    topic = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()  # Duration in minutes
    start_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic