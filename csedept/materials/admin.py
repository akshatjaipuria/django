from django.contrib import admin
from .models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'semester', 'created')
    list_filter = ("semester",)
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)