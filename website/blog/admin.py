from tabnanny import verbose

from django.contrib import admin
from .models import *
from django.contrib import admin
# Register your models here.



admin.sites.AdminSite.site_header = "پنل مدریت جنگو"
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "پنل مدریت"

class ImageInLine(admin.TabularInline):

    model = Image
    extera = 1

class CommentInLine(admin.TabularInline):
    model = Comment
    extera = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", 'author', 'publish', 'status']
    ordering = ["title"]
    list_filter = ["status"]
    search_fields = ["title"]
    date_hierarchy = "publish"
    prepopulated_fields = {"slug" : ["title"]}
    list_editable = ["status"]
    #list_display_links = ["title"]
    inlines = [ImageInLine, CommentInLine]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['phone','email','subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", 'post', 'created', 'active']
    list_filter = ["name", 'post', 'created', 'active']
    list_editable = ["active"]
    search_fields = ["name", 'post', 'created','publish']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'description']

