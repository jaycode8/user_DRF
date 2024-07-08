from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UsersSerializer
from .models import Users
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def allUsers():
    users = Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response({"message": serializer.data, "status":status.HTTP_200_OK}) 

def register(req):
    serializer = UsersSerializer(data = req.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"success", "status": status.HTTP_200_OK})
    return Response({"message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

def signIn(req):
    user = Users.objects.filter(username = req.data["username"])
    if not user:
        return Response({"message":"username not found", "status":status.HTTP_400_BAD_REQUEST})
    found_user = authenticate(username = req.data["username"], password = req.data["password"])
    if not found_user:
        return Response({"message":"incorrect password", "status": status.HTTP_400_BAD_REQUEST})
    authed_user = Users.objects.get(username = req.data["username"])
    token, _ = Token.objects.get_or_create(user=authed_user)
    login(req, authed_user)
    return Response({"message":"sign in successfully", "token": token.key, "status": status.HTTP_200_OK})

def userData(user):    
    serializer = UsersSerializer(user)
    return Response({"message":serializer.data, "status":status.HTTP_200_OK})

def updateUser(req, user):
    serializer = UsersSerializer(user, data= req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User updated successfully", "status":status.HTTP_200_OK})
    return Response({"message": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

def deleteUser(req):
    id = req.user._id
    user = Users.objects.get(_id=id)
    print(user)
    user.delete()
    return Response({"message":"successfully deleted record"}, status=status.HTTP_200_OK)

def logOut(req):
    req.user.auth_token.delete()
    logout(req)
    return Response({"message":"logout"}, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def index(req):
    if req.method == 'GET':
        return allUsers()
    
    elif req.method == "POST":
        if req.headers["Form"] == "signup":
            return register(req)
        return signIn(req)
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(req):
    user = Users.objects.get(_id = req.user._id)
    if req.method == "GET":
        if req.headers["Purpose"] == "logout":
            return logOut(req)
        return userData(user)
    
    elif req.method == "PUT":
        return updateUser(req, user)

    elif req.method == "DELETE":
        return deleteUser(req)