from django.contrib import admin
from .models import Post, PostImage
from .models import CustomUser
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(PostImage)