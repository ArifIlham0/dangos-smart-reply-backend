from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dangos_smart_reply_backend.views.user_view import create_user, fetch_users, fetch_user, update_user, delete_users
from dangos_smart_reply_backend.views.authentication_view import login, logout, reset_password, activate_users, refresh_token
from dangos_smart_reply_backend.views.smart_reply_view import smart_reply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Users
    path('api/dangos-smart-reply/v1/user/create', create_user),
    path('api/dangos-smart-reply/v1/user/fetch', fetch_users),
    path('api/dangos-smart-reply/v1/user/fetch-by-id/<int:id>', fetch_user),
    path('api/dangos-smart-reply/v1/user/update/<int:id>', update_user),
    path('api/dangos-smart-reply/v1/user/delete', delete_users),
    # Authentication
    path('api/dangos-smart-reply/v1/authentication/login', login),
    path('api/dangos-smart-reply/v1/authentication/refresh-token', refresh_token),
    path('api/dangos-smart-reply/v1/authentication/logout', logout),
    path('api/dangos-smart-reply/v1/authentication/reset-password', reset_password),
    path('api/dangos-smart-reply/v1/authentication/activate-users', activate_users),
    # Smart Reply
    path('api/dangos-smart-reply/v1/smart-reply/ask', smart_reply),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)