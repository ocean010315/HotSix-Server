# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=10)  # Field name made lowercase.
    join_date = models.DateField(db_column='Join_Date')  # Field name made lowercase.
    is_active = models.IntegerField(db_column='is_Active')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user'


class AccountsImage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(db_column='Time', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accounts_image'


class Group(models.Model):
    group_code = models.CharField(db_column='Group_Code', primary_key=True, max_length=20, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    group_name = models.CharField(db_column='Group_Name', max_length=10)  # Field name made lowercase.
    creator_id = models.ForeignKey(User, models.CASCADE, max_length=100, db_column='Creator_ID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group'


class GroupMember(models.Model):
    member_id = models.AutoField(db_column='Member_ID', primary_key=True)  # Field name made lowercase.
    group_code = models.ForeignKey(Group, models.CASCADE, db_column='Group_Code')  # Field name made lowercase.
    email = models.ForeignKey(User, models.CASCADE, db_column='Email')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_member'


class GroupNotice(models.Model):
    notice_id = models.CharField(db_column='Notice_ID', primary_key=True, max_length=20, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    group_code = models.ForeignKey(Group, on_delete=models.CASCADE, db_column='Group_Code')  # Field name made lowercase.
    notice_title = models.CharField(db_column='Notice_Title', max_length=15, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.       
    notice_content = models.CharField(db_column='Notice_Content', max_length=100, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)  # Field name made lowercase.
    notice_date = models.DateField(db_column='Notice_Date')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_notice'


class GroupTask(models.Model):
    task_id = models.CharField(db_column='Task_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    group_code = models.ForeignKey(Group, models.CASCADE, db_column='Group_Code')  # Field name made lowercase.
    task_name = models.CharField(db_column='Task_Name', max_length=15, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.       
    task_progress = models.IntegerField(db_column='Task_Progress')  # Field name made lowercase.
    responsibility = models.ForeignKey('User', models.CASCADE, db_column='Responsiblity', max_length=100) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_task'


class GroupGoal(models.Model):
    goal_id = models.CharField(db_column='Goal_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    group_code = models.ForeignKey(Group, models.CASCADE, db_column='Group_Code')  # Field name made lowercase.
    goal_name = models.CharField(db_column='Goal_Name', max_length=100, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.       
    goal_progress = models.IntegerField(db_column='Goal_Progress')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_goal'


class GroupSchedule(models.Model):
    schedule_id = models.AutoField(db_column='Schedule_ID', primary_key=True)  # Field name made lowercase.
    group_code = models.ForeignKey(Group, models.CASCADE, db_column='Group_Code')  # Field name made lowercase.
    schedule_title = models.CharField(db_column='Schedule_Title', max_length=15, db_collation='utf8mb4_0900_ai_ci')  # Field name made lowercase.
    schedule_content = models.CharField(db_column='Schedule_Content', max_length=100, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)  # Field name made lowercase.
    start_time = models.DateField(db_column='Start_Time')  # Field name made lowercase.
    end_time = models.DateField(db_column='End_Time')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_schedule'


class GroupTimetable(models.Model):
    timetable_id = models.AutoField(db_column='Timetable_ID', primary_key=True)  # Field name made lowercase.
    group_code = models.ForeignKey(Group, models.CASCADE, db_column='Group_Code', blank=True, null=True)  # Field name made lowercase.
    time_table = models.BinaryField(db_column='Time_Table', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'group_timetable'


class Time(models.Model):
    time_id = models.AutoField(db_column='Time_ID', primary_key=True)  # Field name made lowercase.
    email = models.ForeignKey('User', models.CASCADE, db_column='Email')  # Field name made lowercase.
    time_table = models.BinaryField(db_column='Time_Table', max_length=255, null=True)  # Field name made lowercase.
    preference = models.BinaryField(db_column='Preference', max_length=255, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'time'


# 이미지 처리
class Image(models.Model):
    image = models.ImageField(upload_to='images/') # 이미지가 저장될 위치
    time = models.CharField(max_length=5) # 시간