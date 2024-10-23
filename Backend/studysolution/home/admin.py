from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name", "phone_Number", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "phone_Number","image","address"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "email_verified"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "image","address","name", "phone_Number", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "name", "phone_Number"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)

class Eventadmin(admin.ModelAdmin):
    list_display = ["id", "Event_Name" , "Event_start"]
    class Meta:
        model = Event
admin.site.register(Event, Eventadmin)

class countryadmin(admin.ModelAdmin):
    list_display = ["country"]
    class Meta:
        model = country
admin.site.register(country, countryadmin)

class Enquiryadmin(admin.ModelAdmin):
    list_display = ["name", "Email", "phone_Number"]
    class Meta:
        model = Enquiry
admin.site.register(Enquiry, Enquiryadmin)

class scholarshipsadmin(admin.ModelAdmin):
    list_display = ["country", "university_Name", "scholarship"]
    class Meta:
        model = scholarships
admin.site.register(scholarships, scholarshipsadmin)


class Pathways_Scholarshipsadmin(admin.ModelAdmin):
    list_display = ["country", "scholarship_Name"]
    class Meta:
        model = Pathways_Scholarships
admin.site.register(Pathways_Scholarships, Pathways_Scholarshipsadmin)


# Register Available Courses
@admin.register(available_courses)
class AvailableCoursesAdmin(admin.ModelAdmin):
    list_display = ['course_name']
    search_fields = ['course_name']

# Register Degree
@admin.register(degree)
class degreeAdmin(admin.ModelAdmin):
    list_display = ['degree']
    search_fields = ['degree']


# Register University with ManyToManyField for Available Courses
@admin.register(university)

class UniversityAdmin(admin.ModelAdmin):
    list_display = ['University_Name', 'country']
    search_fields = ['University_Name', 'country__name']
    list_filter = ['country']
    
    # Customizing the form to display Available Courses as a filter horizontal field
    filter_horizontal = ('available_courses', 'degree')

    # Customizing the fields displayed on the admin page
    fieldsets = (
        (None, {
            'fields': ('University_Name', 'University_Image', 'About_University', 'country', 'Entry_Requirements', 'English_Requirements', 'Tuition_Fees', 'available_courses', 'degree','Why_This_University')
        }),
    )

class Appointment_time_slotadmin(admin.ModelAdmin):
    list_display = ["time"]
    class Meta:
        model = Appointment_time_slot
admin.site.register(Appointment_time_slot, Appointment_time_slotadmin)

class Appointmentadmin(admin.ModelAdmin):
    list_display = ["UserId","Name","Date", "Time"]
    class Meta:
        model = Appointment
admin.site.register(Appointment, Appointmentadmin)