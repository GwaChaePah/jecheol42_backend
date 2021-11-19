"""gwachaepah_practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from board import views

from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="제철42",
      default_version='v1',
      description="제철42 swagger",
      terms_of_service="https://jecheol-42.herokuapp.com/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # swagger
    url(r'^swagger(?P<format>\.json)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # jecheol-42
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('board/', views.board, name="board"),
    path('show/<int:post_key>', views.show, name="show"),
    path('search/', views.search, name="search"),
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    path('edit/<int:post_key>', views.edit, name="edit"),
    path('update/<int:post_key>', views.update, name="update"),
    path('delete/<int:post_key>', views.delete, name="delete"),
    path('comment_create/<int:post_key>/', views.comment_create, name="comment_create"),
    path('comment_update/<int:comment_key>/', views.comment_update, name="comment_update"),
    path('comment_delete/<int:comment_key>/', views.comment_delete, name="comment_delete"),

    # api
    path('product/api/', views.ProductList.as_view()),
    path('board/api', views.BoardSearchList.as_view()), # 쿼리 스트링 받아서 필터링
    path('post/api/', views.PostCreateView.as_view()), # post POST
    path('post/api/<int:pk>/', views.PostDetailView.as_view()), # 특정 포스트의 get put(+patch) delete
    path('comment/api/list/<int:pk>/', views.CommentList.as_view()), # 특정 post(pk)의 comments GET
    path('comment/api/', views.CommentCreateView.as_view()), # 특정 포스트 pk 에 comment POST
    path('comment/api/detail/<int:pk>/', views.CommentDetailView.as_view()), # 특정 comment pk 의 comment put get delete
    path('search/api', views.SearchList.as_view()),

    # user
    # 나중에 지울 부분
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('register/', views.register, name="register"),
    path('user_register/', views.user_register, name="user_register"),
    # 여기 위까지
    path('user/api/check/', views.UserCheckView.as_view()),
    path('user/api/register/', views.UserRegisterView.as_view()),

    # jwt
    path('token/api/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/api/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/api/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    path('api-auth/', include('rest_framework.urls')),
]
