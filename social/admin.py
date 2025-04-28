from django.contrib import admin
from .models import Post, Comment, FriendRequest

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content_summary')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def content_summary(self, obj):
        return (obj.content[:50] + '...') if obj.content else '(No Text)'
    content_summary.short_description = 'Content'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'content', 'post__content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'accepted', 'created')
    list_filter = ('accepted', 'created')
    search_fields = ('from_user__username', 'to_user__username')
    ordering = ('-created',)
