from rest_framework import status,serializers
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.timezone import  now
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import User
from django.db.models import Q
from .permissions import IsAdminOrSameUser
import os
import uuid
import hashlib
from django.conf import settings

def home(request):
    return render(request, 'home.html')  # 确保你有一个对应的模板文件


def build_response(code, message, data=None):
    response_data = {
        "code": code,
        "message": message,
    }
    if data is not None:
        response_data["data"] = data
    return response_data


##注册
class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)
        else:
            print("Errors:", serializer.errors)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                build_response(200, "User created successfully.", UserRegistrationSerializer(user).data),
                status=status.HTTP_201_CREATED
            )
        else:
            # 如果验证失败，构建带有 code 和 message 的错误响应
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")
            return Response(
                build_response(400, "; ".join(error_messages)),
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # 如果验证失败，构建带有 code 和 message 的错误响应
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")
            print('error_messages',error_messages)
            return Response(
                build_response(400, "; ".join(error_messages)),
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data
        user.last_login = now()
        user.save(update_fields=['last_login'])

        refresh = RefreshToken.for_user(user)
        return Response(
            build_response(
                "200",
                "Login successful.",
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            ),
            status=status.HTTP_200_OK
        )

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)



class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]  # 只有认证用户可以访问
    authentication_classes = [JWTAuthentication]  # 使用 JWT 验证

    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                build_response(404, "User not found."),
                status=status.HTTP_404_NOT_FOUND
            )

        # 确保当前认证用户只能修改自己的信息或者管理员
        if request.user != user and not request.user.is_superuser:
            return Response(
                build_response(403, "You do not have permission to modify this user."),
                status=status.HTTP_403_FORBIDDEN
            )

        # 检查是否有尝试更新 role 并且当前用户是否有权限这样做
        if 'role_id' in request.data and not request.user.is_superuser:
            return Response(
                build_response(403, "You do not have permission to change the role of this user."),
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                build_response(200, "User information updated successfully.", serializer.data),
                status=status.HTTP_200_OK
            )
        else:
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")
            return Response(
                build_response(400, "; ".join(error_messages)),
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 只有认证用户可以访问
    authentication_classes = [JWTAuthentication]  # 使用 JWT 验证

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        print("user_id:",user_id)
        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    build_response(404, "User not found."),
                    status=status.HTTP_404_NOT_FOUND
                )

            # 检查当前用户是否有权限修改指定用户的密码
            if not request.user.is_superuser and request.user != user:
                return Response(
                    build_response(403, "You do not have permission to change this user's password."),
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # 如果没有提供 user_id，则默认为修改自己的密码
            user = request.user

        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the two new passwords match
            if serializer.validated_data['new_password1'] != serializer.validated_data['new_password2']:
                return Response(
                    build_response(400, "New passwords do not match."),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Change password
            user.set_password(serializer.validated_data['new_password1'])
            user.save()

            return Response(
                build_response(200, "Password updated successfully."),
                status=status.HTTP_200_OK
            )
        else:
            # If serializer validation fails, return error messages
            errors = serializer.errors
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")
            return Response(
                build_response(400, "; ".join(error_messages)),
                status=status.HTTP_400_BAD_REQUEST
            )

class UserListPagination(pagination.PageNumberPagination):
    page_size = 5  # 每页显示的用户数量
    page_size_query_param = 'pagesize'  # 匹配前端的参数名
    page_query_param = 'pagenum'  # 前端可以通过此参数指定页码
    max_page_size = 100


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # 只有认证用户可以访问
    authentication_classes = [JWTAuthentication]  # 使用 JWT 验证
    pagination_class = UserListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query:
            queryset = queryset.filter(Q(username__icontains=query) | Q(nickname__icontains=query)| Q(gender__icontains=query)).order_by('id')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            response_data = build_response(
                200, "User list retrieved successfully.",
                data=paginated_response.data
            )
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            build_response(200, "User list retrieved successfully.", serializer.data),
            status=status.HTTP_200_OK
        )

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSameUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        print('request',request.data['username'])
        response = self.create(request, *args, **kwargs)
        print(response.data)
        # 修改响应以包含 code 和统一的响应格式
        data = build_response(
            200, "User created successfully.",
            data=response.data
        )
        user =User.objects.get(username=request.data['username'])
        user.role_id  = request.data['role_id']
        user.set_password('12345678')
        user.save()
        return Response(data, status=status.HTTP_200_OK)


class DeleteUserView(APIView):
    permission_classes = [IsAdminOrSameUser]  # 管理员或用户自己可以删除
    authentication_classes = [JWTAuthentication]  # 使用 JWT 验证

    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                build_response(404, "User not found."),
                status=status.HTTP_404_NOT_FOUND
            )
        # 删除用户
        user.delete()

        return Response(
            build_response(200, "User deleted successfully."),
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # 假设前端发送了 refresh token
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # 将刷新令牌添加到黑名单
            return Response(
                build_response("200", "Logout successful."),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                build_response(400, f"Failed to logout: {str(e)}"),
                status=status.HTTP_400_BAD_REQUEST
            )


class SaveChangesStatus(APIView):
    permission_classes = [permissions.IsAdminUser]  # 只允许超级用户访问此视图

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        is_superuser_str = kwargs.get('is_superuser', '').lower()

        if is_superuser_str not in ['true', 'false']:
            return Response({"code": 400, "message": "Invalid value for is_superuser"},
                            status=status.HTTP_400_BAD_REQUEST)

        is_superuser = (is_superuser_str == 'true')
        user = get_object_or_404(User, id=id)

        # 确保当前认证用户是超级用户才能更改其他用户的超级用户状态
        if not request.user.is_superuser:
            return Response(
                {"code": 403, "message": "You do not have permission to change the superuser status of this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        user.is_superuser = is_superuser
        user.save()

        return Response({"code": 200, "message": "状态更改成功！"}, status=status.HTTP_200_OK)

class UploadImgView(APIView):
    def post(self, request):
        """接收上传文件"""
        rev_file = request.FILES.get('file')
        if not rev_file:
            return Response({"code": 400, "message": '文件不存在'}, status=400)
        # 获取唯一的名字：uuid+hash
        new_name = self.get_random_str()
        ext = os.path.splitext(rev_file.name)[1]
        file_path = os.path.join(settings.UPLOAD_FILE, new_name + ext)
        print(r'http://127.0.0.1:8899/upload/'+new_name + ext)
        try:
            with open(file_path, 'wb') as f:
                for chunk in rev_file.chunks():
                    f.write(chunk)

            return Response({"code": 200, "data": r'http://127.0.0.1:8899/upload/'+new_name + ext}, status=200)
        except IOError as e:
            return Response({"code": 500, "message": str(e)}, status=500)

    @staticmethod
    def get_random_str():
        uuid_val = uuid.uuid4()
        uuid_str = str(uuid_val).encode('utf-8')
        md5_obj = hashlib.md5()
        md5_obj.update(uuid_str)
        return md5_obj.hexdigest()
