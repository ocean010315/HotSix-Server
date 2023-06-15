from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.views import View
from rest_framework import renderers
from rest_framework import viewsets
from urllib.parse import unquote
from rest_framework.renderers import JSONRenderer

from accounts.views import restore_time, add_prefer, compress_table, print_table, login_check, INIT_TIME_TABLE, INIT_PREFERENCE, cookie_check ###
from accounts.models import Group, GroupMember, GroupTimetable, Time, User, GroupTask, GroupNotice, GroupGoal
from accounts.serializers import GroupDataSerializer, GroupMemberSerializer, GroupTimetableSerializer, UserDataSerializer, GroupTaskSerializer, GroupNoticeSerializer, GroupGoalSerializer
from django.core.exceptions import ValidationError
from django.db.models import Q

import uuid
import base64
import codecs
import zlib
import jwt

# def login_check(func):
#     def wrapper(self, request, *args, **kwargs):
#         try:
#             access_token = request.COOKIE.get('jwt')

#             if not access_token:
#                 return Response(status=status.HTTP_401_UNAUTHORIZED)
            
#             payload = jwt.decode(access_token, "SecretJWTKey", algorithms=['HS256'])

#             user = User.objects.filter(email=payload['email']).first()
#             serializer = UserDataSerializer(user)

#         except jwt.ExpiredSignatureError:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         return func(self, request, *args, **kwargs)
#     return wrapper


# current date 'yyyy-mm-dd' format
def current_date():
    now = timezone.now()
    date = now.strftime("%Y-%m-%d")
    return date


# generate 8-character random code mixed with English case and number
def generateRandomCode(length=8):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, "base64").rstrip()
    ).decode()[:length]


# Group
# generate group
@api_view(['POST'])
@login_check
def groupGenerate(request):
    reqData = request.data # user email, group_name by request
    # email = reqData['email']
    email = request.email
    Group_Name = reqData['group_name']
    Group_Code = generateRandomCode()

    group = Group(group_code=Group_Code, group_name=Group_Name, creator_id=User.objects.get(pk=email))
    group.save()

    res = Response(status=status.HTTP_201_CREATED)
    res.data = Group_Code

    cgt = create_group_table(Group_Code)
    if cgt is False:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return res


# join group with group code
@api_view(['POST'])
@login_check
def joinGroup(request):
    reqData = request.data
    Group_Code = reqData['group_code']
    # email = reqData['email']
    email = request.email

    if Group.objects.filter(pk=Group_Code).exists():
        groupMember = GroupMember(group_code=Group.objects.get(pk=Group_Code), email=User.objects.get(pk=email))
        groupMember.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_404_NOT_FOUND)


# get group member list
@api_view(['GET'])
@login_check
def getGroupMember(request):
    member = []
    group_code = request.GET.get('group_code')
    group = Group.objects.get(pk=group_code)
    creator = group.creator_id
    member.append(creator.email)

    members = GroupMember.objects.filter(group_code=group_code)
    for m in members:
        member.append(m.email.email)

    res = Response(status=status.HTTP_200_OK)
    res.data = { "member_list" : member }
    return res


# get user group list
@api_view(['GET'])
@login_check
def getGroupList(request):
    try:
        user = request.email
        # reqData = request.data
        # user = reqData['email']

        group_codes = GroupMember.objects.filter(email=user).values('group_code')
        group_list = Group.objects.filter(Q(group_code__in=group_codes) | Q(creator_id=user))
        serializer = GroupDataSerializer(group_list, many=True)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except ValidationError:
        return Response({"error" : "TYPE_ERROR"}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({"error" : "KEY_ERROR"}, status=status.HTTP_400_BAD_REQUEST)

# group delete
@api_view(['POST', 'DELETE'])
@login_check
def deleteGroup(request):
    user = request.email
    group_code = request.data['group_code']

    try:
        group = Group.objects.get(pk=group_code)
        creator_id = group.creator_id_id

        # 그룹 생성자일 경우 - 그룹 삭제
        if(user == creator_id):
            group.delete()
        # 그룹원일 경우 - 그룹 나가기
        else:
            group_member = GroupMember.objects.get(group_code=Group.objects.get(pk=group_code), email=User.objects.get(pk=user))
            member_id = group_member.pk
            delete = GroupMember.objects.get(pk=member_id)
            delete.delete()

        
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

  
# 그룹 멤버들의 시간표 조회
@api_view(['GET'])
@login_check 
def ViewGroupTable(request):
    if request.method == 'GET':
        group_code = request.GET.get('group_code')
        group_code = unquote(group_code)
        print(group_code)
        if Group.objects.filter(group_code=group_code).exists():
            check = integrate_table(group_code)

            # if GroupTimetable.objects.filter(group_code=group_code).exists():
            if check is True:
                group = GroupTimetable.objects.get(group_code=group_code)
                group_table = group.time_table
                res_group_table = restore_group_time(group_table)

                res = Response(status=status.HTTP_200_OK)
                res.data  = {
                    "integrated_table" : res_group_table
                }

                return res
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 그룹 시간표 초기화 (일정 없는 시간표 생성)
# @api_view(['POST'])
# @login_check
# def create_group_table(request):
#     if request.method == 'POST':
def create_group_table(group_code):
    post_group_code = group_code

    z_table = compress_table(INIT_TIME_TABLE)

    if Group.objects.filter(group_code=post_group_code).exists():
        input_data = {
            'group_code':post_group_code,
            'time_table':z_table
        }
        serializer = GroupTimetableSerializer(data=input_data)

        if serializer.is_valid():
            serializer.save()
            return True
        else: 
            return False
    else:
        return False
        

# 그룹 멤버들의 시간표를 통합
# @api_view(['PUT'])
# @login_check
def integrate_table(group_code):
    #if group_code.method == 'PUT':
        # try:
            # reqData = group_code.data
            post_group_code = group_code
            
            if Group.objects.filter(group_code=post_group_code).exists():
                if GroupMember.objects.filter(group_code=post_group_code).exists():
                    # 그룹 멤버들의 시간표 통합
                    group_members = GroupMember.objects.filter(group_code=post_group_code).values() # 그룹 멤버들 받아 오기
                    group_table = integrated_members_table(group_members) # 그룹 멤버들의 시간표 통합
                    z_table = compress_table(group_table)
                    if GroupTimetable.objects.filter(group_code=post_group_code).exists(): 
                        update_table = GroupTimetable.objects.get(group_code=post_group_code)
                        update_table.time_table = z_table
                        update_table.save()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        # except:
        #     return Response(status=status.HTTP_409_CONFLICT) 
       
@api_view(['DELETE'])
@login_check
def del_group_table(request):
    if request.method == 'DELETE':
        try:
            reqData = request.data
            del_group_code = reqData['group_code']

            if Group.objects.filter(group_code=del_group_code).exists():
                if GroupTimetable.objects.filter(group_code=del_group_code).exists():
                    del_group_table =  GroupTimetable.objects.get(group_code=del_group_code)
                    del_group_table.delete()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_409_CONFLICT) 

          
# GroupProject
# 할 일 생성 - progress를 default로 지정하기 위해 serializer가 아니라 수동으로 save
@api_view(['POST'])
@login_check
def createGroupTask(request):
    reqData = request.data
    
    if request.method == 'POST':
        # 할 일 생성
        task_name = reqData['task_name']
        task_id = generateRandomCode()
        group_code = reqData['group_code']
        responsibility = request.email
        task_progress = 0 # 0 = not started, 1 = ~ing, 2 = done

        group = Group.objects.get(pk=group_code)
        creator = group.creator_id_id
        if request.email == responsibility or request.email == creator:
            group_task = GroupTask(task_id=task_id, task_name=task_name, 
                                            task_progress=task_progress, group_code=Group.objects.get(pk=group_code), responsibility=User.objects.get(pk=responsibility))
            group_task.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_check
def getGroupTask(request):
    group_code = request.GET.get('group_code')
    user = request.email

    try:
        group = Group.objects.filter(group_code=group_code)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    my_task = GroupTask.objects.filter(group_code=group_code, responsibility=user)
    my_serializer = GroupTaskSerializer(my_task, many=True)
    others = GroupTask.objects.filter(Q(group_code=group_code) & ~Q(responsibility=user))
    other_serializer = GroupTaskSerializer(others, many=True)
    data = {
        "mine" : my_serializer.data,
        "others" : other_serializer.data,
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@login_check
def updateGroupTask(request):
    reqData = request.data
    task_id = reqData['task_id']
    task_progress = reqData['task_progress']

    task = GroupTask.objects.get(pk=task_id)
    group = Group.objects.get(pk=task.group_code_id)
    
    if request.email == task.responsibility_id or request.email == group.creator_id_id:
        task.task_progress = task_progress
        task.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# task name, progress, responsibility 수정 시 - project_id는 pk로 쓰기 때문에 변경 X
@api_view(['POST', 'DELETE'])
@login_check
def deleteGroupTask(request):
    reqData = request.data
    task_id = reqData['task_id']

    try:
        task = GroupTask.objects.get(task_id=task_id)
    except GroupTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task = GroupTask.objects.get(pk=task_id)
    group = Group.objects.get(pk=task.group_code_id)
    
    if request.email == task.responsibility_id or request.email == group.creator_id_id:
        task.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# 그룹 멤버들의 시간표를 통합하는 함수
def integrated_members_table(group_members):
    # 그룹의 멤버들의 시간표 받아 오기
    members_time_table = []
    for member in group_members:
        user_time = Time.objects.get(email=member['email_id']) # 해당 그룹 멤버
        user_table, user_prefer = restore_time(user_time.email) # 해당 그룹 멤버의 시간표
        integrated_table = add_prefer(user_table, user_prefer) # 해당 그룹 멤버의 시간표와 우선 순위 통합
        members_time_table.append(integrated_table) # 그룹 멤버들의 시간표 리스트에 추가

    group_table = members_time_table[0] # 첫 시간표 미리 추가

    # 시간표 통합
    for idx in range(1, len(members_time_table)): # 그룹 멤버 각각의 시간표 (첫 시간표 건너뛰기)
        for time in range(len(members_time_table[idx])): # 시간표의 각 시간대
            for day in range(7): # 시간대의 각 요일
                if group_table[time][day] == 0 or group_table[time][day] >= 2: # (그룹 테이블) 공강일 시
                    if members_time_table[idx][time][day] == 1: # (개인 시간표) 강의 있을 시 => (그룹 테이블) 공강 -> 일정
                        group_table[time][day] = 1
                    else: # (개인 시간표) 강의 없을 시 => (그룹 테이블) 공강 -> 일정
                        group_table[time][day] += members_time_table[idx][time][day]

    return group_table


# 압축한 그룹 시간표 리스트로 복원하는 함수
def restore_group_time(group_time_table):
    if group_time_table != None:
        str_table = zlib.decompress(group_time_table).decode('utf-8')
    else: 
        str_table = INIT_TIME_TABLE

    lst_table = []
    table_element = []
    i = 0
    for ch in str_table:
        i += 1
        table_element.append(ch)

        if i % 7 == 0 and i != 0: 
            table_element_int = [int(i) for i in table_element]
            lst_table.append(table_element_int)
            table_element = []

    return lst_table
  

# group notice
@api_view(['POST'])
@cookie_check
# @login_check
def createNotice(request):
    if request.method == 'POST':
        reqData = request.data

        group_code = reqData['group_code']
        notice_id = generateRandomCode()
        notice_title = reqData['notice_title']
        notice_content = reqData['notice_content']
        notice_date = current_date()

        notice = GroupNotice(notice_id=notice_id, notice_title=notice_title, notice_content=notice_content,
                             notice_date=notice_date, group_code=Group.objects.get(pk=group_code))
        notice.save()
        
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@login_check
def getNotice(request):
    # reqData = request.data
    group_code = unquote(request.GET.get('group_code'))

    if request.method == 'GET':
        # group_code = reqData['group_code']

        notice_list = GroupNotice.objects.filter(group_code=group_code)
        serializer = GroupNoticeSerializer(notice_list, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@login_check
def deleteNotice(request):
    reqData = request.data
    notice_id = reqData['notice_id']
    print(notice_id)
    
    try:
        notice = GroupNotice.objects.get(pk=notice_id)
    except GroupNotice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    notice.delete()
    return Response(status=status.HTTP_200_OK)


# group goal
@api_view(['POST'])
@login_check
def createGoal(request):
    # try: 
    #     token = request.COOKIE.get('jwt')
    #     payload = jwt.decode(token, "SecretJWTKey", algorithms=['HS256'])
    #     email = payload['email']

    #     reqData = request.data
    #     group_code = reqData['group_code']

    #     creator = Group.objects.filter(group_code=group_code, creator_id=email)

    # except Group.DoesNotExist:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    creator = request.email
    reqData = request.data
    group_code = reqData['group_code']
    group = Group.objects.get(pk=group_code)

    if group.creator_id_id == creator:
        goal_id = generateRandomCode()
        goal_name = reqData['goal_name']
        goal_progress = 0 # 0 = 진행 안 됨, 1 = 완료

        goal = GroupGoal(goal_id=goal_id, goal_name=goal_name, goal_progress=goal_progress, group_code=Group.objects.get(pk=group_code))
        goal.save()

        res = Response(status=status.HTTP_201_CREATED)
        res.data = {
            "goal_id" : goal_id
        }

        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@login_check
def getGoal(request):
    group_code = unquote(request.GET.get('group_code'))
    try:
        goal_list = GroupGoal.objects.filter(group_code=group_code)
        serializer = GroupGoalSerializer(goal_list, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except GroupGoal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@login_check
def updateGoal(request):
    reqData = request.data
    goal_id = reqData['goal_id']
    progress = reqData['goal_progress']

    goal = GroupGoal.objects.get(pk=goal_id)
    group = Group.objects.get(pk=goal.group_code_id)

    if request.email == group.creator_id_id:
        goal.goal_progress = progress
        goal.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
@login_check
def deleteGoal(request):
    # try: 
    #     token = request.COOKIE.get('jwt')
    #     payload = jwt.decode(token, "SecretJWTKey", algorithms=['HS256'])
    #     email = payload['email']

    #     reqData = request.data
    #     group_code = reqData['group_code']

    #     creator = Group.objects.filter(group_code=group_code, creator_id=email)

    # except Group.DoesNotExist:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    reqData = request.data
    goal_id = reqData['goal_id']

    try:
        goal = GroupGoal.objects.get(pk=goal_id)
        group = Group.objects.get(pk=goal.group_code_id)

        if request.email == group.creator_id_id:
            goal.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except GroupGoal.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)