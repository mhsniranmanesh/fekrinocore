from django.contrib import admin

# Register your models here.
from match.models.match import Like, SuperLike, Dislike, Match, UnMatch

admin.site.register(Like)
admin.site.register(SuperLike)
admin.site.register(Dislike)
admin.site.register(Match)
admin.site.register(UnMatch)
