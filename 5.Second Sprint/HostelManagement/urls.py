from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [

##################################################################################################
    path('admin/', admin.site.urls),
    path('',include('webapp.urls')),
##################################################################################################

##################################################################################################
# for Book APi:
    path('api/' ,include('API.urls')),
##################################################################################################

##################################################################################################
# for djoser:
    # http://127.0.0.1:8000/auth/users/
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
#####################################################################################################

########################################################################################################################
# To Get the API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
# http://127.0.0.1:8000/librarymanagement/api/stream/firstsprint/documentation/
    path("librarymanagement/api/stream/firstsprint/documentation/", SpectacularSwaggerView.as_view(url_name="schema")),
#########################################################################################################################
]
