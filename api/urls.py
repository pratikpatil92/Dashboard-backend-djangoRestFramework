from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token


from . import views

router = routers.DefaultRouter()
router.register('register', views.RegisterView)
router.register('post', views.PostViewset)
# router.register('/auth_login', views.LoginView,basename='auth_login')



urlpatterns = [
    path('', include(router.urls)),
    # path('login/',views.MyObtainTokenPairView.as_view(),name='token_obtain_view'),
    path('auth/',obtain_auth_token),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('get_user/', views.GetSingleUserData.as_view(), name='auth_user_details'),
    path('get_category/', views.get_category),
    path('add_category/', views.addCategory),
    path('edit_category/<int:category_id>', views.updateCategory),
    path('delete_category/<int:category_id>', views.deleteCategory),

]