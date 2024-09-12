from rest_framework.permissions import BasePermission


class CustomPermissionsForToolsInUse(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name='SUPERADMIN').exists():
            print('superadmin is here')
            return True

        if user.groups.filter(name='Manager').exists():
            print('manager is here')
            if request.method == 'GET':
                return True
            if request.method == 'DELETE':
                # return user.has_perm('can_destroy_toolsInUse')
                return True

        if user.groups.filter(name='Supervisor').exists():
            print('supervisor is here')
            if request.method == 'GET':
                return True

            if request.method == 'DELETE':
                # return user.has_perm('can_destroy_toolsInUse')
                return True

        if user.groups.filter(name='Operator').exists():
            print('operator is here')
            if request.method == 'GET':
                return True

            if request.method == 'POST':
                # return user.has_perm('can_create_toolsInUse')
                return True

            if request.method == 'PATCH' or request.method == 'PUT':
                # return user.has_perm('can_modify_toolsInUse')
                return True

        return False


class CustomPermissionsExceptToolsInUse(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name='SUPERADMIN').exists():
            print('superadmin is here')
            return True

        if user.groups.filter(name='Manager').exists():
            print('manager is here')
            if request.method == 'GET':
                return True

            if request.method == 'POST':
                # return user.has_perm('can_create_machine')
                return True

            if request.method == 'PUT' or request.method == 'PATCH':
                # return user.has_perm('can_modify_machine')
                return True

        if user.groups.filter(name='Supervisor').exists():
            print('supervisor is here')
            if request.method == 'GET':
                return True

            if request.method == 'POST':
                # return user.has_perm('can_create_machine')
                return True

        if user.groups.filter(name='Operator').exists():
            print('operator is here')
            if request.method == 'GET':
                return True

        return False


class ReadingDataPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name='SUPERADMIN').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Supervisor').exists() or user.groups.filter(name='Operator').exists():
            return True

        return False
