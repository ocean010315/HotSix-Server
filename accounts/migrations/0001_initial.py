# Generated by Django 4.2.1 on 2023-06-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountsImage',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('image', models.TextField(blank=True, db_column='Image', null=True)),
                ('time', models.CharField(blank=True, db_column='Time', max_length=5, null=True)),
            ],
            options={
                'db_table': 'accounts_image',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_code', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Group_Code', max_length=20, primary_key=True, serialize=False)),
                ('group_name', models.CharField(db_column='Group_Name', max_length=10)),
            ],
            options={
                'db_table': 'group',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('time', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(db_column='Email', max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='Password', max_length=100)),
                ('name', models.CharField(db_column='Name', max_length=10)),
                ('join_date', models.DateField(db_column='Join_Date')),
                ('is_active', models.IntegerField(db_column='is_Active')),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('time_id', models.AutoField(db_column='Time_ID', primary_key=True, serialize=False)),
                ('time_table', models.BinaryField(db_column='Time_Table', max_length=255, null=True)),
                ('preference', models.BinaryField(db_column='Preference', max_length=255, null=True)),
                ('email', models.ForeignKey(db_column='Email', on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'db_table': 'time',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupTimetable',
            fields=[
                ('timetable_id', models.AutoField(db_column='Timetable_ID', primary_key=True, serialize=False)),
                ('time_table', models.BinaryField(db_column='Time_Table', max_length=255)),
                ('group_code', models.ForeignKey(blank=True, db_column='Group_Code', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
            ],
            options={
                'db_table': 'group_timetable',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupTask',
            fields=[
                ('task_id', models.CharField(db_column='Task_ID', max_length=20, primary_key=True, serialize=False)),
                ('task_name', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Task_Name', max_length=15)),
                ('task_progress', models.IntegerField(db_column='Task_Progress')),
                ('group_code', models.ForeignKey(db_column='Group_Code', on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
                ('responsibility', models.ForeignKey(db_column='Responsiblity', max_length=100, on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'db_table': 'group_task',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_column='Schedule_ID', primary_key=True, serialize=False)),
                ('schedule_title', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Schedule_Title', max_length=15)),
                ('schedule_content', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', db_column='Schedule_Content', max_length=100, null=True)),
                ('start_time', models.DateField(db_column='Start_Time')),
                ('end_time', models.DateField(db_column='End_Time')),
                ('group_code', models.ForeignKey(db_column='Group_Code', on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
            ],
            options={
                'db_table': 'group_schedule',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupNotice',
            fields=[
                ('notice_id', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Notice_ID', max_length=20, primary_key=True, serialize=False)),
                ('notice_title', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Notice_Title', max_length=15)),
                ('notice_content', models.CharField(blank=True, db_collation='utf8mb4_0900_ai_ci', db_column='Notice_Content', max_length=100, null=True)),
                ('notice_date', models.DateField(db_column='Notice_Date')),
                ('group_code', models.ForeignKey(db_column='Group_Code', on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
            ],
            options={
                'db_table': 'group_notice',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('member_id', models.AutoField(db_column='Member_ID', primary_key=True, serialize=False)),
                ('email', models.ForeignKey(db_column='Email', on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('group_code', models.ForeignKey(db_column='Group_Code', on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
            ],
            options={
                'db_table': 'group_member',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GroupGoal',
            fields=[
                ('goal_id', models.CharField(db_column='Goal_ID', max_length=20, primary_key=True, serialize=False)),
                ('goal_name', models.CharField(db_collation='utf8mb4_0900_ai_ci', db_column='Goal_Name', max_length=100)),
                ('goal_progress', models.IntegerField(db_column='Goal_Progress')),
                ('group_code', models.ForeignKey(db_column='Group_Code', on_delete=django.db.models.deletion.CASCADE, to='accounts.group')),
            ],
            options={
                'db_table': 'group_goal',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='creator_id',
            field=models.ForeignKey(db_column='Creator_ID', max_length=100, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]