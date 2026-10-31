from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User,Role, Menu


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  ##validate_password 密码校验
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'password', 'password2', 'email', 'phone_number', 'avatar', 'gender', 'age', 'birthday', 'address', 'bio','role_id')
        extra_kwargs = {
            'username': {'required': True},
            'nickname': {'required': True},
            'email': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
            'gender': {'required': False},
            'age': {'required': False},
            'birthday': {'required': False},
            'address': {'required': False},
            'bio': {'required': False},
            'role_id':{'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"code": 400, "message": "Password fields didn't match."})

        if len(attrs['password']) < 3:
            raise serializers.ValidationError({"code": 400, "message": "Password must be at least 3 characters long."})

        return attrs

    def create(self, validated_data):
        role_id = self.initial_data.get('role_id', None)  # 使用 initial_data 替代 validated_data 获取 role_id
        validated_data.pop('password2')  # 移除确认密码字段

        user = User.objects.create_user(**validated_data)

        if role_id is not None:
            try:
                user.role_id = int(role_id)
                user.save()
            except ValueError:
                raise serializers.ValidationError({"code": 400, "message": "Invalid role_id format."})
        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'nickname', 'email', 'phone_number', 'avatar', 'gender', 'role_id', 'birthday', 'address', 'is_active','is_superuser','bio','last_login']

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()  # 添加这个字段

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'phone_number', 'avatar', 'gender', 'role_id', 'birthday', 'address', 'is_active', 'is_superuser', 'bio', 'last_login', 'role_name']  # 包含新字段

    def get_role_name(self, obj):
        return obj.role.name if obj.role else None  # 如果用户有角色，则返回角色名称，否则返回None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user or not user.is_active:
            raise serializers.ValidationError({
                "code": 400,
                "message": _("用户名不存在或用户已停用.")
            })
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'nickname', 'email', 'phone_number', 'avatar', 'gender', 'age', 'birthday',
            'address', 'bio', 'role'
        )
        extra_kwargs = {
            'nickname': {'required': True},
            'email': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
            'gender': {'required': False},
            'age': {'required': False},
            'birthday': {'required': False},
            'address': {'required': False},
            'bio': {'required': False},
            'role': {'required': False, 'queryset': Role.objects.all()}
        }



class UserCreareSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'nickname', 'email', 'phone_number', 'avatar', 'gender', 'age', 'birthday',
            'address', 'bio')
        extra_kwargs = {
            'nickname': {'required': True},
            'email': {'required': False},
            'phone_number': {'required': False},
            'avatar': {'required': False},
            'gender': {'required': False},
            'age': {'required': False},
            'birthday': {'required': False},
            'address': {'required': False},
            'bio': {'required': False},
        }

    def create(self, validated_data):
        # 设置默认密码并创建用户
        password = validated_data.pop('password', '12345678')
        user = User(**validated_data)
        user.set_password(password)  # 使用 set_password 方法确保密码被正确哈希
        user.save()
        return user

class PasswordChangeSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        """
        Check that the two new passwords match.
        """
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data




class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ('id', 'title', 'url', 'level', 'is_visible', 'icon', 'name', 'parent', 'children')

    def get_children(self, obj):
        # 获取子菜单并递归序列化
        return MenuSerializer(obj.children.all(), many=True).data

class RoleSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)
    accessible_menus_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'menus', 'accessible_menus_count', 'created_at', 'updated_at']

    def get_accessible_menus_count(self, obj):
        return obj.accessible_menus.count()