from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from accounts.views import RegisterView, CustomTokenObtainPairView, UserProfileView
from properties.views import PropertyTypeViewSet, PropertyViewSet
from reservations.views import ReservationViewSet
from payments.views import PaymentViewSet, LoyaltyAccountViewSet
from reviews.views import ReviewViewSet

# Router for ViewSets
router = DefaultRouter()
router.register('properties/types', PropertyTypeViewSet, basename='property-type')
router.register('properties/units', PropertyViewSet, basename='property')
router.register('reservations', ReservationViewSet, basename='reservation')
router.register('payments', PaymentViewSet, basename='payment')
router.register('loyalty', LoyaltyAccountViewSet, basename='loyalty')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Auth endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # API routes
    path('api/', include(router.urls)),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "NexStay Administration"
admin.site.site_title = "NexStay Admin"
admin.site.index_title = "Welcome to NexStay Admin Portal"
