from django.urls import path#, #register_converter
from . import views#, converters
from django.contrib.auth.views import LogoutView

#register_converter(converters.DepartmentConverter, 'dID')

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/google/login/callback/adduser/', views.add_user, name='addUser'),
    path('search', views.searchbar, name='search'),
    path('result', views.result, name='result'),
    path('logout', LogoutView.as_view()),
    path('schedule', views.view_schedule, name='viewschedule'),
    path('create',views.create,name='create'),
    path('initialize', views.initialize, name='initialize'),
    path('finished',views.finished,name='finished'),

    path('friendlist', views.friendlist, name='friendlist'),
    path('friend_result', views.friend_result, name='friend_result'),
    path('<str:userName>/addfriend',views.addfriend,name='addfriend'),
    path('<str:userName>/removefriend',views.removefriend,name='removefriend'),
    path('<str:userName>/schedules',views.schedules,name='schedules'),
    #path('friendlist/<str:userName>/', views.add_friend, name='send friend request'),
    #path('friendlist/<int:requestID>/', views.accept_friend_request, name='accept friend request'),

    path('<str:dept>', views.departments, name='depts'),
    path('<str:dept>/<int:course_num>', views.course, name='course'),
    path('<str:dept>/<int:course_num>/newreview', views.leave_a_review, name='newreview'),
    path('<str:dept>/<int:course_num>/<str:review_id>', views.review_detail, name='reviewdetail'),
    path('<str:dept>/<int:course_num>/<int:section>/addclass', views.add_class, name='addclass'),
    path('<str:dept>/<int:course_num>/<int:section>/dropclass', views.drop_class, name='dropclass')
]
