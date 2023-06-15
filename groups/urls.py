from django.urls import path
from . import views

urlpatterns = [
    path('generate-group/', views.groupGenerate, name="groupGenerate"),
    path('join-group/', views.joinGroup, name="joinGroup"),
    path('delete-group/', views.deleteGroup, name="deleteGroup"),
    path('get-group/', views.getGroupList, name="getGroupList"),
    path('get-group-member/', views.getGroupMember, name="getGroupMember"),

    # path('view-group-table/<str:group_code>', views.ViewGroupTable.as_view(), name="ViewGroupTable"),
    path('view-group-table/', views.ViewGroupTable, name="ViewGroupTable"),
    path('create-group-table/', views.create_group_table, name="create_group_table"),
    path('integrated-table/', views.integrate_table, name="integrate_table"),
    path('del-group-table/', views.del_group_table, name="del_group_table"),

    path('create-group-task/', views.createGroupTask, name="generateGroupTask"),
    path('get-group-task/', views.getGroupTask, name="getGroupTask"),
    path('delete-group-task/', views.deleteGroupTask, name="deleteGroupTask"),
    path('update-group-task/', views.updateGroupTask, name="updateGroupTask"),

    path('create-group-notice/', views.createNotice, name="createNotice"),
    path('get-group-notice/', views.getNotice, name="getNotice"),
    path('delete-notice/', views.deleteNotice, name="deleteNotice"),

    path('create-group-goal/', views.createGoal, name="createGoal"),
    path('get-group-goal/', views.getGoal, name="getGoal"),
    path('update-group-goal/', views.updateGoal, name="updateGoal"),
    path('delete-group-goal/', views.deleteGoal, name="deleteGoal"),
]