from django.contrib import admin
from pro_file.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_photo')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


admin.site.register(Profile, ProfileAdmin)
