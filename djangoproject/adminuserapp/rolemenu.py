# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Role,Menu
from .serializers import MenuSerializer,RoleSerializer
from rest_framework.decorators import action

def build_response(code, message, data=None):
    response_data = {
        "code": code,
        "message": message,
    }
    if data is not None:
        response_data["data"] = data
    return response_data



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]  # 只有认证用户可以访问

    def list(self, request, *args, **kwargs):
        """
        获取角色列表。
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(build_response(200, "Roles retrieved successfully.", {"roles": serializer.data}))

    def update(self, request, *args, **kwargs):
        """
        修改指定的角色信息。
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(build_response(200, "Role updated successfully.", {"role": serializer.data}))
        else:
            errors = {field: messages[0] for field, messages in serializer.errors.items()}
            return Response(build_response(400, "Validation failed.", {"errors": errors}), status=status.HTTP_400_BAD_REQUEST)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
               获取菜单列表，只包含 is_visible 为 True 的菜单。
               """

        # 定义递归函数来构建可见菜单树
        def build_visible_menu_tree(parent_id=None):
            children = Menu.objects.filter(parent_id=parent_id, is_visible=True)
            menu_list = []
            for child in children:
                menu_data = self.get_serializer(child).data
                menu_data['children'] = build_visible_menu_tree(child.id)
                menu_list.append(menu_data)
            return menu_list

        top_level_menus = build_visible_menu_tree()

        return Response(build_response(200, "Menus retrieved successfully.", {"menus": top_level_menus}))

    def partial_update(self, request, *args, **kwargs):
        """
        修改菜单的部分信息，例如名称。
        """
        kwargs['partial'] = True
        response = self.update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(build_response(200, "Menu updated successfully.", {"menu": response.data}))
        return response

    @action(detail=False, methods=['post'], url_path='assign-menus-to-role')
    def assign_menus_to_role(self, request):
        """
        根据提供的 role ID 和菜单 ID 数组，保存或更新角色与菜单的关系。
        """
        role_id = request.data.get('role_id')
        menu_ids = request.data.get('menu_ids', [])

        if not role_id or not isinstance(menu_ids, list):
            return Response(build_response(400, "Invalid input data."), status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(build_response(404, "Role not found."), status=status.HTTP_404_NOT_FOUND)

        # 清除旧的菜单关联并设置新的关联
        role.menus.set(menu_ids)

        # 序列化更新后的角色信息
        serializer = RoleSerializer(role)
        return Response(build_response(200, "Menus assigned to role successfully.", {"role": serializer.data}))

    @action(detail=False, methods=['get'], url_path='get-menus-by-role/(?P<role_id>[^/.]+)')
    def get_menus_by_role(self, request, role_id=None):
        """
        根据提供的角色 ID 获取该角色已分配的菜单，并返回简化的字典列表。
        """
        # 处理 role_id 为 'null' 字符串的情况
        if not role_id or role_id == 'null':
            return Response(build_response(400, "Role ID is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response(build_response(404, "Role not found."), status=status.HTTP_404_NOT_FOUND)

        # 获取角色关联的菜单并序列化
        menus = role.menus.all().values('id', 'name','title','parent_id')

        # 构建简化后的字典列表，包含父级信息（如果有的话）
        menu_list = []
        # 用于存储已经处理过的菜单，包括它们的父级信息
        processed_menus = {}

        for menu in menus:
            menu_id = menu['id']
            parent_id = menu['parent_id']

            # 如果当前菜单还没有被处理过
            if menu_id not in processed_menus:
                menu_dict = {
                    'menu_id': menu_id,
                    'name': menu['name'],
                    'title': menu['title']
                }

                # 如果有父级菜单，则尝试获取父级菜单的信息
                if parent_id is not None and parent_id not in processed_menus:
                    try:
                        parent_menu = Menu.objects.get(id=parent_id)
                        parent_dict = {
                            'menu_id': parent_menu.id,
                            'name': parent_menu.name,
                            'title': parent_menu.title,
                            'is_parent': True  # 标记为父级菜单
                        }
                        processed_menus[parent_id] = parent_dict
                        menu_list.append(parent_dict)  # 父级信息添加到列表中
                    except Menu.DoesNotExist:
                        pass  # 父级菜单不存在或已被删除，不做处理

                # 将当前菜单信息添加到列表中
                menu_list.append(menu_dict)
                processed_menus[menu_id] = menu_dict

        # 对菜单列表按照 ID 排序，确保父级菜单总是出现在子级之前
        menu_list.sort(key=lambda x: x['menu_id'])

        return Response(build_response(200, "Menus retrieved successfully.", {"menus": menu_list}))