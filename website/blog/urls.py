from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
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
    path('logout/',views.log_out, name='logout'),

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url='/blog/password-change/done/'
        ),
        name='password-change'
    ),

    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password-change-done'
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url='/blog/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/blog/password-reset/complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    

]