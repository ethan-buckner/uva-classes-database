from django.contrib import admin
from .models import Dept, Subject, Review, UniqueUser


class DeptAdmin(admin.ModelAdmin):
    fields = ['subject', 'js']


class SubjectAdmin(admin.ModelAdmin):
    search_fields= ['course_number']
    fields = ['course_number', 'instructor', 'email', 'semester_code', 'course_section', 'subject', 'catalog_number',
              'description', 'units', 'component', 'class_capacity', 'wait_list', 'wait_cap', 'enrollment_total',
              'enrollment_available', 'topic', 'days', 'start_time', 'end_time', 'facility_description']


class ReviewAdmin(admin.ModelAdmin):
    fields = ['course_id', 'overall_rating', 'difficulty_rating', 'user_name', 'user_email', 'review_title',
              'review_text', 'review_date']


class UniqueUserAdmin(admin.ModelAdmin):
    fields = ['user','userID','userName', 'userEmail', 'userFriends', 'userSchedule','is_authenticate','lastName','firstName','Major','Year']


admin.site.register(Dept, DeptAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UniqueUser, UniqueUserAdmin)
# Register your models here.
