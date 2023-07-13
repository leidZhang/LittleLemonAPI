from rest_framework import permissions 

class IsManagerOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True 
        return request.user.groups.filter(name='Manager').exists() 

class IsManagerOrDeliveryCrewOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True 
        return request.user.groups.filter(name__in=['Manager', 'Delivery Crew']).exists() 
    
class IsManagerOrDeliveryCrewOrCustomer(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True 
        return request.user.groups.filter(name__in=['Manager', 'Delivery Crew', 'Customer']).exists() 
    
class IsAdminOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True 
        return request.user.groups.filter(name='Admin').exists() 

class IsAdminOrReadOnly(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: 
            return True
        return request.user.groups.filter(name='Admin').exists() 
    
class IsCustomer(permissions.BasePermission): 
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Customer').exists() 

class IsAdmin(permissions.BasePermission): 
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists() 