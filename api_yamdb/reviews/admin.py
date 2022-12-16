from django.contrib import admin
from .models import Title, Category, Genre, User

EMPTY_CONST = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'genre',
        'category',
    )
    list_editable = ('genre', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = EMPTY_CONST



# admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(User)