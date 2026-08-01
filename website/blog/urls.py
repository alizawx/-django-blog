from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    # path('posts/', views.post_list, name='post_list'),
    path('posts/', views.post_list, name='post_list'),
    # path('posts/<int:id>/', views.post_detail,name="post_detail"),
    path('posts/<int:pk>/', views.post_detail,name="post_detail"),
    path('ticket', views.ticket, name="ticket"),
    path('posts/<pk>/comment', views.post_comment,name="post_comment"),
    path('category/<slug:slug>/',views.category_posts,name='category_posts'),
    path('author/<str:username>', views.author_detail, name='author_detail'),
    path("search/", views.searching, name="search"),
    path('profile/',views.profile,name='profile'),
    path('profile/create_post',views.create_post,name='create_post'),
    path('profile/delete_post/<post_id>',views.delete_post,name='delete_post'),
    path('profile/edite_post/<post_id>',views.edite_post,name='edite_post'),
    path('profile/delete_image/<image_id>',views.delete_image,name='delete_image'),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    # path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('logout/',views.log_out, name='log_out'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password-change-done'),


]