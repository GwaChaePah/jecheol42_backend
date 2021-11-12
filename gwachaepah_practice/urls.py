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
from django.urls import path
from board.views import main, board, show, search, new, create, edit, update, delete,\
    comment_create, comment_update, comment_delete,\
    ProductList, BoardSearchList, BoardList, PostCommentList, PostList, CommentList, CommentDetailList, SearchList,\
    user_login, user_logout, register, user_register, TestView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views


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
    path('', main, name="main"),
    path('board/', board, name="board"),
    path('show/<int:post_key>', show, name="show"),
    path('search/', search, name="search"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('edit/<int:post_key>', edit, name="edit"),
    path('update/<int:post_key>', update, name="update"),
    path('delete/<int:post_key>', delete, name="delete"),
    path('comment_create/<int:post_key>/', comment_create, name="comment_create"),
    path('comment_update/<int:comment_key>/', comment_update, name="comment_update"),
    path('comment_delete/<int:comment_key>/', comment_delete, name="comment_delete"),

    # api
    path('product-api/', ProductList.as_view()),
    path('board-api', BoardSearchList.as_view()), # 쿼리 스트링 받아서 필터링
    path('board-api/', BoardList.as_view()), # 전체 보드 데이터 + 페이지네이션 get, 새 글 작성 post
    path('post_comment-api/<int:pk>/', PostCommentList.as_view()), # 포스트 페이지에서 보일 특정 포스트 + 코멘트 리스트 get
    path('post-api/<int:pk>/', PostList.as_view()), # 특정 포스트의 put(+patch) delete
    path('comment-api/', CommentList.as_view()), # 특정 포스트 pk 에 코멘트를 post
    path('comment-api/<int:pk>/', CommentDetailList.as_view()), # 특정 코멘트 pk 의 코멘트를 put get delete
    path('search-api', SearchList.as_view()),

    # user
    path('user_login/', user_login, name="user_login"),
    path('user_logout/', user_logout, name="user_logout"),
    path('register/', register, name="register"),
    path('user_register/', user_register, name="user_register"),

    # jwt
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # test
    path('hello/', TestView.as_view(), name='TestView')
]
