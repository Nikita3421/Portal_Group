from django.contrib.auth.mixins import UserPassesTestMixin


class PermissionOrOwnerRequiredMixin(UserPassesTestMixin):
    permission_required = None
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        instance = self.get_object()
        if not instance:
            return True
        if instance.creator == self.request.user:
            return True
        
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        
        return self.request.user.has_perms(perms)