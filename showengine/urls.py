from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('showlist.api.urls')),
    path('account/', include('account.api.urls')),

    # path('api-auth/', include('rest_framework.urls')),
]
