from django.contrib import admin
from .models import User, Posts, Followers, Likes


admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Followers)
admin.site.register(Likes)

