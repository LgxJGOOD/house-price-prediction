from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

TABLE_PREFIX = getattr(settings, 'TABLE_PREFIX', 't_')

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(BaseModel):
    name = models.CharField(_('角色名称'), max_length=100, unique=True)
    menus = models.ManyToManyField('Menu', related_name='roles', blank=True)

    def __str__(self):
        return self.name

    @property
    def accessible_menus(self):
        return self.menus.filter(is_visible=True)

    class Meta(BaseModel.Meta):
        db_table = f"{TABLE_PREFIX}role"
        ordering = ['id']

class Menu(BaseModel):
    title = models.CharField(_('菜单标题'), max_length=100)
    url = models.CharField(_('菜单URL'), max_length=200)
    level = models.PositiveSmallIntegerField(_('菜单级别'), default=1)
    is_visible = models.BooleanField(_('是否显示'), default=True)
    icon = models.CharField(_('图标'), max_length=50, blank=True, null=True)
    name = models.CharField(_('名称'), max_length=100, blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('父菜单')
    )

    def __str__(self):
        return self.title

    class Meta(BaseModel.Meta):
        db_table = f"{TABLE_PREFIX}menu"
        ordering = ['level', 'id']

class User(AbstractUser, BaseModel):
    username = models.CharField(_('账号'), max_length=150, unique=True)
    password = models.CharField(_('密码'), max_length=128)
    nickname = models.CharField(_('昵称'), max_length=150)
    email = models.EmailField(_('邮箱'), blank=True, null=True)
    phone_number = models.CharField(_('手机号'), max_length=15, blank=True, null=True)
    status = models.CharField(_('状态'), max_length=10, default='active')
    avatar = models.CharField(_('头像'), max_length=255, blank=True, null=True)
    gender = models.CharField(_('性别'), max_length=10, blank=True, null=True)
    age = models.PositiveIntegerField(_('年龄'), blank=True, null=True)
    birthday = models.DateField(_('生日'), blank=True, null=True)
    address = models.TextField(_('地址'), blank=True, null=True)
    bio = models.TextField(_('简介'), blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True, related_name='users')

    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.username

    @property
    def accessible_menus(self):
        if self.role:
            return self.role.accessible_menus.all()
        return Menu.objects.none()

    class Meta(AbstractUser.Meta, BaseModel.Meta):
        db_table = f"{TABLE_PREFIX}user"
        ordering = ['id']