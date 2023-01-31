from django.test import TestCase
from . import views
from django.urls import reverse
from django.test.client import RequestFactory
from .models import *
import datetime


# Create your tests here.

class GoogleTests(TestCase):

    def test_urls(self):
        url = reverse('depts', args=['acct'])
        self.assertEqual(url, '/acct')

        url = reverse('depts', args=['wgs'])
        self.assertEqual(url, '/wgs')

    def test_other_urls(self):
        url = reverse('depts', args=['cs'])
        self.assertEqual(url, '/cs')


class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_departments(self):
        request = self.factory.get('/acct')
        response = views.departments(request, 'acct')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        request = self.factory.get('')
        response = views.home(request)
        self.assertEqual(response.status_code, 200)


class UserModelTests(TestCase):
    def test_initial_values(self):
        user = UniqueUser.objects.create(userID=1, userName="test", userEmail="test@test.test")
        self.assertEquals(user.userEmail, 'test@test.test')
        self.assertEquals(user.userName, 'test')
        self.assertEquals(user.userID, 1)
        self.assertEquals(user.userSchedule, '')

    def test_string_method(self):
        name = UniqueUser(userName="This is my username")
        self.assertEqual(str(name), name.userName)


class SubjectModelTests(TestCase):
    def test_initial_values(self):
        subject = Subject.objects.create(instructor="Test Instructor",
                                         email="test@test.test",
                                         description="test description",
                                         class_capacity=1244994,
                                         topic="test topic",
                                         semester_code=1,
                                         wait_list=1,
                                         wait_cap=1,
                                         enrollment_total=1,
                                         enrollment_available=2)
        self.assertEquals(subject.instructor, 'Test Instructor')
        self.assertEquals(subject.email, 'test@test.test')
        self.assertEquals(subject.description, "test description")
        self.assertEquals(subject.class_capacity, 1244994)
        self.assertFalse(subject.class_capacity == 10)
        self.assertEquals(subject.topic, 'test topic')

    def test_default_values(self):
        subject = Subject.objects.create(instructor="Test Instructor",
                                         email="test@test.test",
                                         description="test description",
                                         class_capacity=1244994,
                                         topic="test topic",
                                         semester_code=1,
                                         wait_list=1,
                                         wait_cap=1,
                                         enrollment_total=1,
                                         enrollment_available=2)
        self.assertEquals(subject.facility_description, '')
        self.assertNotEqual(subject.end_time, 'a')


class Friend_RequestModelTests(TestCase):
    def test_values(self):
        user = UniqueUser.objects.create(userID=1,
                                         userName="test",
                                         userEmail="test@test.test")
        user2 = UniqueUser.objects.create(userID=2,
                                          userName="test2",
                                          userEmail="test2@test.test")
        self2 = Friend_Request.objects.create(
            from_user=user,
            to_user=user2
        )
        self.assertEqual(self2.to_user.userID, 2)
        self.assertEqual(self2.from_user.userID, 1)


class ReviewModelTests(TestCase):
    def test_values(self):
        review = Review.objects.create(
            course_id="TEST",
            overall_rating=4.5,
            difficulty_rating=10.6,
            user_email='test@test.test',
            review_title="Test Title",
            review_text="Test",
            review_date=datetime.date(2010, 1, 1)
        )
        self.assertEquals(review.course_id, "TEST")
        self.assertEquals(review.overall_rating, 4.5)
        self.assertEquals(review.user_name, "anonymous")
        self.assertEquals(review.review_title, "Test Title")
        self.assertEquals(review.review_date, datetime.date(2010, 1, 1))


class DeptModelTests(TestCase):
    def test_values(self):
        dept = Dept.objects.create(subject="Test")
        empty_dict = {}
        self.assertEquals(dept.subject, "Test")
        self.assertEquals(dept.js, empty_dict)
