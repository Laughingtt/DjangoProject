from crm import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.Show_Customer.as_view(),name='customer'),
    url(r'^add_customer/$',views.add_customer,name='add_customer'),
    url(r'^edit_customer/(\d*)$',views.edit_customer,name='edit_customer'),
    url(r'^my_customer/$',views.Show_Customer.as_view(),name='my_customer'),
    url(r'^all_customer/$',views.Show_Customer.as_view(),name='all_customer'),
    #客户跟进记录表
    url(r'^consult_list/(?P<customer_id>\d*)/$',views.ConsultRecord.as_view(),name='consult_list'),
    #增加客户记录
    url(r'^add_consult/$',views.add_consult,name='add_consult'),
    #编辑客户记录
    url(r'^edit_consult/(?P<consult_id>\d*)/$',views.edit_consult,name='edit_consult'),

    #报名表
    url(r'^enrolment_list/(?P<customer_id>\d*)/$',views.EnrolmentList.as_view(),name='enrolment_list'),
    #新增
    url(r'^add_enrolment/(?P<customer_id>\d*)/$',views.add_enrolment,name='add_enrolment'),
    #修改报名人员
    url(r'^edit_enrolment/(?P<enrolment_id>\d*)/$',views.edit_enrolment,name='edit_enrolment'),

    #班级列表
    url(r'^class_list/$',views.ClassList_view.as_view(),name='class_list'),
    #新增
    url(r'^add_class_list/$',views.add_class_list,name='add_class_list'),
    #编辑
    url(r'^edit_class_list/(?P<class_id>\d*)/$',views.add_class_list,name='edit_class_list'),

    #课程记录
    url(r'^course_list/(?P<class_id>\d*)/$',views.CourseList.as_view(),name='course_list'),
    #新增
    url(r'^add_course_list/$',views.add_course_list,name='add_course_list'),
    #编辑
    url(r'^edit_course_list/(?P<course_id>\d*)/$',views.add_course_list,name='edit_course_list'),

    #学习记录
    url(r'^study_list/(?P<course_id>\d*)/$',views.study_record,name='study_list'),



    # url(r'^page/',views.page,name='page'),
    # url(r'^test/',views.test,name='test'),
]