import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .serializers import CategorySerializer, MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer, \
    UpdateUserSerializer, PostSerializer
from .models import Category, Post


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer


class RegisterView(viewsets.ModelViewSet):
    """This viewset is used to register new user"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request):
        """Register new user"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name,
                                            last_name=last_name)
            message = f'profile is created'
            return Response({"data": serializer.data, "message": message}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """Change password of current user logged in"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    """Update the user details of currnt login user"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        """update function which used to update user by passing id or pk"""
        instance = self.get_object()
        instance.username = request.data.get("username")
        instance.first_name = request.data.get('first_name')
        instance.last_name = request.data.get('last_name')
        instance.email = request.data.get('email')

        instance.save()

        serializer = self.get_serializer(instance)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        return Response({"data": serializer.data, "status": status.HTTP_200_OK})


class GetSingleUserData(generics.ListAPIView):
    """Its return single user profile detalis as per user id is given"""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})


##### Category CRUD Operations########
@api_view(['GET'])
def get_category(request):
    """List all category"""
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"msg":"Somthing Wrong!"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addCategory(request):
    """add Category"""
    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # category = Category.objects.create(categoryName=serializer.validated_data.get['categoryName'])
            serializer.save()
            return Response(
                {'data': serializer.data,"message": "category is inserted"},status=status.HTTP_200_OK)
        elif ObjectDoesNotExist:
            return Response({'error': "Insert category first", "status": status.HTTP_404_NOT_FOUND})
        else:
            return Response({'error': "Somthing went wrong", "status": status.HTTP_400_BAD_REQUEST})


@api_view(['GET', 'PUT'])
def updateCategory(request, category_id):
    """Update or edit category"""
    try:
        category = Category.objects.get(id=category_id)
        print("id", category)
    except Category.DoesNotExist:
        return Response({'message': "requested category does not exist", "status": status.HTTP_404_NOT_FOUND})

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})

    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data, "message": "Data updated successfullt", "status": status.HTTP_200_OK})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def deleteCategory(request, category_id):
    """Update or edit category"""
    try:
        category = Category.objects.get(id=category_id)
        print("id", category)
    except Category.DoesNotExist:
        return Response({'message': "requested category does not exist", "status": status.HTTP_404_NOT_FOUND})

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})

    elif request.method == "DELETE":
        category.delete()
        return Response({"message": "Catagory deleted successfully", "status": status.HTTP_200_OK})


#### Post CRUD Operations ####

class PostViewset(viewsets.ModelViewSet):
    """manage post in database"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()


    # @action(methods=['POST'], detail=True, url_path='upload-image')
    # def upload_image(self, request, pk=None):
    #

