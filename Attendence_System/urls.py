from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "FACE ATTENDENCE SYSTEM"
admin.site.site_title = "SING UP PAGE "
admin.site.index_title = "Welcome to Face recogniton base Attenence Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendence_sys.urls'))

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)