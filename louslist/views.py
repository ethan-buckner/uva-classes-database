from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewReviewForm
from .models import Dept, Subject, Review, UniqueUser, Friend_Request
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

def home(request):
    resp = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    context = {
        'data': resp
    }
    return render(request, 'louslist/index.html', context)


def initialize(request):
    resp = requests.get('http://luthers-list.herokuapp.com/api/deptlist/?format=json').json()
    for key in resp:
        dep = Dept(subject=key['subject'], js=resp)
        dep.save()
    for x in Dept.objects.all():
        print(x.subject)
        res = requests.get("http://luthers-list.herokuapp.com/api/dept/" + x.subject + "/?format=json").json()
        for a in res:
            days = ""
            starting_time = ""
            ending_time = ""
            fac_description = ""
            if a['meetings']:
                days = a['meetings'][0]['days']
                starting_time = a['meetings'][0]['start_time']
                ending_time = a['meetings'][0]['end_time']
                fac_description = a['meetings'][0]['facility_description']
            sub = Subject(
                instructor=a['instructor']['name'],
                email=a['instructor']['email'],
                course_number=a['course_number'],
                semester_code=a['semester_code'],
                course_section=a['course_section'],
                subject=a['subject'],
                catalog_number=a['catalog_number'],
                description=a['description'],
                units=a['units'],
                component=a['component'],
                class_capacity=a['class_capacity'],
                wait_list=a['wait_list'],
                wait_cap=a['wait_cap'],
                enrollment_total=a['enrollment_total'],
                enrollment_available=a['enrollment_available'],
                topic=a['topic'],
                days=days,
                start_time=starting_time,
                end_time=ending_time,
                facility_description=fac_description)
            sub.save()
    return HttpResponseRedirect(reverse('home'))


def departments(request, dept):
    print(request.path_info)

    data = requests.get("http://luthers-list.herokuapp.com/api/dept/" + dept.upper() + "/?format=json").json()

    context = {
        'data': data,
        'subject': dept
    }

    return render(request, 'louslist/subject.html', context)

def course(request, dept, course_num):
    review_total = 0
    difficulty_total = 0
    count = 0
    relevant_reviews = Review.objects.filter(course_id=dept + str(course_num))
    for review in relevant_reviews:
        count += 1
        review_total += review.overall_rating
        difficulty_total += review.difficulty_rating
    if count > 0:
        review_avg_string = str(review_total / count)
        difficulty_avg_string = str(difficulty_total / count)
    else:
        review_avg_string = "No reviews"
        difficulty_avg_string = "No reviews"
    context = {
        'reviews': relevant_reviews,
        'dept': dept,
        'course_num': course_num,
        'review_avg': review_avg_string,
        'difficulty_avg': difficulty_avg_string,
        'review_count': count
    }
    return render(request, 'louslist/course.html', context)


def leave_a_review(request, dept, course_num):
    submitted = False
    if request.method == "POST":
        form = NewReviewForm(request.POST)
        if form.is_valid():
            course_id = dept + str(course_num)
            overall_rating = form.cleaned_data['overall_rating']
            difficulty_rating = form.cleaned_data['difficulty_rating']
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email']
            review_title = form.cleaned_data['review_title']
            review_text = form.cleaned_data['review_text']
            review_date = timezone.now()
            new_review = Review(course_id=course_id, overall_rating=overall_rating, difficulty_rating=difficulty_rating,
                                user_name=user_name, user_email=user_email, review_title=review_title,
                                review_text=review_text, review_date=review_date)
            new_review.save()
            return HttpResponseRedirect('/' + str(dept) + '/' + str(course_num) + '/newreview?submitted=True')
    else:
        form = NewReviewForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'dept': dept,
        'course_num': course_num,
        'form': form,
        'submitted': submitted
    }
    return render(request, 'louslist/newReview.html', context)


def review_detail(request, dept, course_num, review_id):
    the_review = Review.objects.filter(id=review_id)[0]
    context = {
        'dept': dept,
        'course_num': course_num,
        'review_id': review_id,
        'review': the_review
    }
    return render(request, 'louslist/reviewDetail.html', context)


def add_user(request):
    return HttpResponseRedirect(reverse('create'))

def create(request):
    a=UniqueUser.objects.filter(Q(userID__icontains=request.user.id))
    if not a:
        user, created = UniqueUser.objects.get_or_create(
            user=request.user,
            userName=request.user.username,
            userID=request.user.id,
            userEmail=request.user.email,
        )
        posts=True
        return render(request, 'louslist/create.html', {'posts':posts})
    else:
        posts=True
        if(a.first().lastName==''):
            return render(request, 'louslist/create.html', {'posts':posts})
        else:
            messages.add_message(request, messages.SUCCESS, "You're Successfully logged in as: "+a.first().userName)
            return render(request, 'louslist/index.html', {'posts':posts})

def getTime(value):
    if value == "":
        return 0
    if value =='-':
        return 0
    v = value
    hour_string = ""
    minute_string = ""
    dot_count = 0
    for c in value:
        if c == '.':
            dot_count += 1
            if dot_count == 2:
                break
        else:
            if dot_count == 0:
                hour_string += c
            if dot_count == 1:
                minute_string += c
    hour = int(hour_string)
    return hour+ (int(minute_string)/60)

def add_class(request, dept, course_num, section):
    schedule = request.user.uniqueuser.userSchedule.split()
    for c in schedule:
        if c == dept + '_' + str(course_num) + '_' + str(section):
            messages.add_message(request, messages.ERROR, "You can't add the same class") 
            return HttpResponseRedirect(reverse('depts', args=[dept]))
        temp=c[c.find('_')+1:]
        temp=temp[temp.find('_')+1:]
        a=Subject.objects.filter(Q(course_number__icontains=temp)).first()
        b=Subject.objects.filter(Q(course_number__icontains=section)).first()
        a_start=getTime(a.start_time)
        a_end=getTime(a.start_time)
        b_start=getTime(b.start_time)
        b_end=getTime(b.end_time)
        if ( (b_start>=a_start and b_start<=a_end) or (b_end>=a_start and b_end<=a_end) ):
            messages.add_message(request, messages.ERROR, "The class that you have selected have time conflictions with your enrolled classes!") 
            return HttpResponseRedirect(reverse('depts', args=[dept]))
    request.user.uniqueuser.userSchedule += ' ' + dept + '_' + str(course_num) + '_' + str(section)
    request.user.uniqueuser.save()
    messages.add_message(request, messages.SUCCESS, "You have succesfully added a class!") 
    return HttpResponseRedirect(reverse('depts', args=[dept.lower()]))


def drop_class(request, dept, course_num, section):
    schedule = request.user.uniqueuser.userSchedule.split()
    dropped = ""
    for c in schedule:
        if c == dept.upper() + '_' + str(course_num) + '_' + str(section) or \
                c == dept + '_' + str(course_num) + '_' + str(section):
            dropped = c
            break
    if dropped != "":
        schedule.remove(dropped)
        new_schedule = ""
        for c in schedule:
            new_schedule += " " + c
        request.user.uniqueuser.userSchedule = new_schedule
        request.user.uniqueuser.save()
    print(request.user.uniqueuser.userSchedule)
    return HttpResponseRedirect(reverse('viewschedule'))


@login_required
def view_schedule(request):
    # user, created = UniqueUser.objects.get_or_create(
    #     user=request.user,
    #     userID=request.user.id,
    #     userName=request.user.username,
    #     userEmail=request.user.email,
    # )
    schedule = request.user.uniqueuser.userSchedule.split()
    if(request.user.uniqueuser.userSchedule==''):
        messages.add_message(request, messages.ERROR, "You don't have anything in Schedule. Please enroll in class first!") 
    print(schedule)
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []
    notime=[]
    for c in schedule:
        dept = ""
        course_num = ""
        section = ""
        count_spaces = 0
        for letter in c:
            if letter == '_':
                count_spaces += 1
            else:
                if count_spaces == 0:
                    dept += letter
                elif count_spaces == 1:
                    course_num += letter
                elif count_spaces == 2:
                    section += letter
        dept_json = requests.get('http://luthers-list.herokuapp.com/api/dept/' + dept.upper() + '/?format=json').json()
        meeting_days = ""
        meeting_start = ""
        meeting_end = ""
        course_description = ""
        location = ""
        course_id = ""
        subject = ""
        catalog_number = ""
        for cl in dept_json:
            if str(cl['course_number']) == section:
                subject = cl['subject']
                catalog_number = cl['catalog_number']
                course_id = cl['subject'] + cl['catalog_number']
                meeting_days = cl['meetings'][0]['days']
                meeting_start = cl['meetings'][0]['start_time']
                meeting_end = cl['meetings'][0]['end_time']
                course_description = cl['description']
                location = cl['meetings'][0]['facility_description']
        attributes = {
            'course_id': course_id,
            'course_description': course_description,
            'meeting_start': meeting_start,
            'meeting_end': meeting_end,
            'location': location,
            'subject': subject.lower(),
            'catalog_number': catalog_number,
            'section': section,
        }
        if "-" in meeting_days:
            notime.append(attributes)
        if "Mo" in meeting_days:
            monday.append(attributes)
        if "Tu" in meeting_days:
            tuesday.append(attributes)
        if "We" in meeting_days:
            wednesday.append(attributes)
        if "Th" in meeting_days:
            thursday.append(attributes)
        if "Fr" in meeting_days:
            friday.append(attributes)
        if "Sa" in meeting_days:
            saturday.append(attributes)
        if "Su" in meeting_days:
            sunday.append(attributes)
    monday.sort(key=_sort_times_)
    tuesday.sort(key=_sort_times_)
    wednesday.sort(key=_sort_times_)
    thursday.sort(key=_sort_times_)
    friday.sort(key=_sort_times_)
    saturday.sort(key=_sort_times_)
    sunday.sort(key=_sort_times_)
    context = {
        'monday': monday,
        'tuesday': tuesday,
        'wednesday': wednesday,
        'thursday': thursday,
        'friday': friday,
        'saturday': saturday,
        'sunday': sunday,
        'notime': notime
    }
    # print(monday)
    # print(tuesday)
    # print(wednesday)
    # print(thursday)
    # print(friday)
    # print(saturday)
    # print(sunday)
    return render(request, 'louslist/schedule.html', context)


def _sort_times_(course_dict):
    time_string = course_dict['meeting_start']
    hour_string = ""
    minute_string = ""
    count_dots = 0
    for c in time_string:
        if c == '.':
            count_dots += 1
        else:
            if count_dots == 0:
                hour_string += c
            if count_dots == 1:
                minute_string += 1
            else:
                break
    if hour_string == "":
        hour_string = "23"
    if minute_string == "":
        minute_string = "59"
    return int(hour_string) * 60 + int(minute_string)




def searchbar(request):
    return render(request, 'louslist/search.html')


def result(request):
    search_post = request.GET.get('search')
    sub_post = request.GET.get('num')
    inst_post = request.GET.get('inst')
    ty_post = request.GET.get('ty')
    bd_post = request.GET.get('bd')
    rn_post = request.GET.get('rn')
    dy_post = request.GET.get('dy')
    tm_post = request.GET.get('tm')
    print(inst_post)
    posts = Subject.objects.all().order_by("subject")
    if search_post:
        posts = posts.filter(Q(subject__iexact=search_post)).order_by("catalog_number")
    if sub_post:
        posts = posts.filter(Q(catalog_number__icontains=sub_post))
    if inst_post:
        posts = posts.filter(Q(instructor__icontains=inst_post))
    if ty_post:
        posts = posts.filter(Q(component__icontains=ty_post))
    if bd_post:
        posts = posts.filter(Q(facility_description__icontains=bd_post))
    if rn_post:
        posts = posts.filter(Q(facility_description__icontains=rn_post))
    if dy_post:
        posts = posts.filter(Q(days__icontains=dy_post))
    if tm_post:
        posts = posts.filter(Q(start_time__icontains=tm_post) or Q(end_time__icontains=tm_post))
    return render(request, 'louslist/result.html', {'posts': posts})

@login_required
def friendlist(request):
    if(request.user.uniqueuser.is_authenticate):
        posts= request.user.uniqueuser
    else:
        posts=""
    return render(request, 'louslist/friendlist.html',{'posts':posts})

def friend_result(request):
    search_post = request.GET.get('search')
    posts = UniqueUser.objects.all()
    if search_post:
        posts = posts.filter(Q(userEmail__icontains=search_post))
    return render(request, 'louslist/friend_result.html', {'posts': posts})


def addfriend(request, userName):
    request.user.uniqueuser.userFriends.add(UniqueUser.objects.get(userName=userName))
    request.user.uniqueuser.save()
    return HttpResponseRedirect(reverse('friendlist'))

def removefriend(request, userName):
    request.user.uniqueuser.userFriends.remove(UniqueUser.objects.get(userName=userName))
    request.user.uniqueuser.save()
    return HttpResponseRedirect(reverse('friendlist'))

def schedules(request,userName):
    user=UniqueUser.objects.get(userName=userName)
    schedule = user.userSchedule.split()
    print(schedule)
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday = []
    saturday = []
    sunday = []
    notime=[] 
    for c in schedule:
        dept = ""
        course_num = ""
        section = ""
        count_spaces = 0
        for letter in c:
            if letter == '_':
                count_spaces += 1
            else:
                if count_spaces == 0:
                    dept += letter
                elif count_spaces == 1:
                    course_num += letter
                elif count_spaces == 2:
                    section += letter
        dept_json = requests.get('http://luthers-list.herokuapp.com/api/dept/' + dept.upper() + '/?format=json').json()
        meeting_days = ""
        meeting_start = ""
        meeting_end = ""
        course_description = ""
        location = ""
        course_id = ""
        subject = ""
        catalog_number = ""
        for cl in dept_json:
            if str(cl['course_number']) == section:
                subject = cl['subject']
                catalog_number = cl['catalog_number']
                course_id = cl['subject'] + cl['catalog_number']
                meeting_days = cl['meetings'][0]['days']
                meeting_start = cl['meetings'][0]['start_time']
                meeting_end = cl['meetings'][0]['end_time']
                course_description = cl['description']
                location = cl['meetings'][0]['facility_description']
        attributes = {
            'course_id': course_id,
            'course_description': course_description,
            'meeting_start': meeting_start,
            'meeting_end': meeting_end,
            'location': location,
            'subject': subject.lower(),
            'catalog_number': catalog_number,
            'section': section,
        }
        if "-" in meeting_days:
            notime.append(attributes)
        if "Mo" in meeting_days:
            monday.append(attributes)
        if "Tu" in meeting_days:
            tuesday.append(attributes)
        if "We" in meeting_days:
            wednesday.append(attributes)
        if "Th" in meeting_days:
            thursday.append(attributes)
        if "Fr" in meeting_days:
            friday.append(attributes)
        if "Sa" in meeting_days:
            saturday.append(attributes)
        if "Su" in meeting_days:
            sunday.append(attributes)
    monday.sort(key=_sort_times_)
    tuesday.sort(key=_sort_times_)
    wednesday.sort(key=_sort_times_)
    thursday.sort(key=_sort_times_)
    friday.sort(key=_sort_times_)
    saturday.sort(key=_sort_times_)
    sunday.sort(key=_sort_times_)
    context = {
        'name': user.userName,
        'monday': monday,
        'tuesday': tuesday,
        'wednesday': wednesday,
        'thursday': thursday,
        'friday': friday,
        'saturday': saturday,
        'sunday': sunday,
        'notime': notime
    }
    # print(monday)
    # print(tuesday)
    # print(wednesday)
    # print(thursday)
    # print(friday)
    # print(saturday)
    # print(sunday)
    return render(request, 'louslist/schedules.html', context)

def finished(request):
    name_post = request.GET.get('name')
    lana_post = request.GET.get('lana')
    fina_post = request.GET.get('fina')
    major_post = request.GET.get('major')
    year_post= request.GET.get('year')
    if(name_post=='' or lana_post=='' or fina_post=='' or major_post==''):
        return render(request, 'louslist/create.html', {'posts':False})
    else:
        request.user.uniqueuser.times=1
        request.user.uniqueuser.is_authenticate=True
        request.user.uniqueuser.userName=name_post
        request.user.uniqueuser.lastName=lana_post
        request.user.uniqueuser.firstName=fina_post
        request.user.uniqueuser.Major=major_post
        request.user.uniqueuser.Year=year_post
        request.user.uniqueuser.save()
        messages.add_message(request, messages.SUCCESS, "You're Successfully logged in as: "+name_post)
        return HttpResponseRedirect(reverse('home'))

"""
@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.userFriends.add(friend_request.from_user)
        friend_request.from_user.userFriends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')
"""