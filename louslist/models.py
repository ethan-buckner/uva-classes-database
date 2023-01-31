from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings


class Dept(models.Model):
    subject = models.CharField(max_length=200, primary_key=True, db_column='subject_id')
    js = models.JSONField(default=dict)


class Subject(models.Model):
    instructor = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='x')
    course_number = models.IntegerField(primary_key=True, db_column='subj_id')
    semester_code = models.IntegerField()
    course_section = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    catalog_number = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    units = models.CharField(max_length=200)
    component = models.CharField(max_length=200)
    class_capacity = models.IntegerField()
    wait_list = models.IntegerField()
    wait_cap = models.IntegerField()
    enrollment_total = models.IntegerField()
    enrollment_available = models.IntegerField()
    topic = models.CharField(max_length=200)
    days = models.CharField(max_length=200, default='')
    start_time = models.CharField(max_length=200, default='')
    end_time = models.CharField(max_length=200, default='')
    facility_description = models.CharField(max_length=200, default='')


class Review(models.Model):
    course_id = models.CharField(max_length=8)
    overall_rating = models.IntegerField()
    difficulty_rating = models.IntegerField()
    user_name = models.CharField(max_length=50, default='anonymous')
    user_email = models.CharField(max_length=50)
    review_title = models.CharField(max_length=200)
    review_text = models.CharField(max_length=600)
    review_date = models.DateTimeField(null=True)


class UniqueUser(models.Model):
    userID = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=50)
    userEmail = models.CharField(max_length=50)
    userFriends = models.ManyToManyField("UniqueUser", blank=True)
    userSchedule = models.CharField(max_length=500, default="")
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_authenticate=models.BooleanField(default=False)
    times = models.IntegerField(default=0)
    lastName = models.CharField(max_length=50,default='')
    firstName = models.CharField(max_length=50,default='')
    Major = models.CharField(max_length=50,default='')
    Year= models.CharField(max_length=50,default='')

    def __str__(self):
        return self.userName


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        UniqueUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        UniqueUser, related_name='to_user', on_delete=models.CASCADE)
