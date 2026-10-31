from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterUserAPIView,LoginAPIView,
                    UserProfileAPIView,UserListView,ChangePasswordView,
                    UpdateUserView,UserCreateView,DeleteUserView,LogoutAPIView,SaveChangesStatus,UploadImgView)
from .rolemenu import RoleViewSet, MenuViewSet

# 创建默认路由器并注册视图集
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'menus', MenuViewSet)

# 定义其他 API 路由
urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('change/psd/', ChangePasswordView.as_view(), name='user-password-change'),
    path('users/list/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:user_id>/update/', UpdateUserView.as_view(), name='user-update'),
    path('users/<int:user_id>/delete/', DeleteUserView.as_view(), name='user-delete'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('users/<int:id>/state/<str:is_superuser>/', SaveChangesStatus.as_view(), name='changes-status'),
    path('upload/images/', UploadImgView.as_view(), name='upload-images'),  # 上传用户图片
]

urlpatterns += [path('', include(router.urls))]


