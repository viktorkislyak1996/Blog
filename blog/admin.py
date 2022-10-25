from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'name', 'email', 'created', 'active')
    list_filter = ('updated', 'created', 'active', 'post')
    search_fields = ('post', 'name', 'body')