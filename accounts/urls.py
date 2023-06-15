from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet #, check_cookies ###
    
router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    # path('cookies/', check_cookies, name="check-cookies"),
    path('duplicate/', views.duplicateCheck, name="duplicateCheck"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('check-activate/', views.check_activate, name="checkActivate"),
    path('activate/<str:uidb64>/<str:token>', views.Activate.as_view(), name="activate"),
    path('send-email/', views.resendEmail, name="resendEmail"),
    # path('login-remain/', views.loginRemain, name="loginRemain"),
    path('logout/', views.logout, name="logout"),

    path('', include(router.urls)), # 이미지 처리를 위한 url
    # path('view-time-table/<str:email>', views.ViewTimeTable.as_view(), name="ViewTimeTable"),
    path('view-time-table/', views.viewTimeTable, name="ViewTimeTable"),
    path('create-time-table/', views.create_time_table, name='create_time_table'),
    path('img-time-table/', views.imgTimeTable, name="imgTimeTable"),
    path('text-time-table/', views.text_time_table, name="textTimeTable"),
    path('ics-time-table/', views.icsTimeTable, name="icsTimeTable"),
    path('save-ics-file/', views.save_ics_file, name="save_ics_file"),
    path('preference/', views.preference, name="preference"),
    path('del-time-table/', views.delTimeTable, name="delTimeTable"),
]