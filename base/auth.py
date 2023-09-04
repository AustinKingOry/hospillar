from django.contrib.auth.backends import ModelBackend
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .functions import user_perms
from django.utils import timezone
from django.contrib.auth.models import Permission

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def get_user_permissions(self, user_obj, obj=None):
        if not hasattr(user_obj, '_cached_permissions'):
            user_obj._cached_permissions = set()
        user_permissions = set()

        # Check the groups the user belongs to
        for group in user_obj.groups.all():
            # Retrieve permissions associated with the group
            permissions = Permission.objects.filter(group=group)
            
            # Add these permissions to the user's set
            user_permissions.update(permissions)
            user_obj._cached_permissions.update(user_permissions)
            print(user_obj._cached_permissions)

            # Store permissions in the user's session
            if self.get_user_session_key(user_obj) is not None:
                session_key = self.get_user_session_key(user_obj)
                print(session_key)
                session = Session.objects.get(session_key=session_key)
                session['cached_permissions'] = list(user_obj._cached_permissions)
                session.save()

        return user_obj._cached_permissions

    def get_user_session_key(self, user):
        sessions = Session.objects.all(expire_date__gte=timezone.now())
        for session in sessions:
            session_data = session.get_decoded()
            if user.pk == session_data.get('_auth_user_id'):
                return session.session_key
        return None
