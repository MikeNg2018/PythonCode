from django.contrib import admin
from .models import Article, Person
# Register your models here.

# 也可用装饰器，等同下面admin.site.register(Article, ArticleAdmin)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'update_time',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


# admin.site.register(Article, ArticleAdmin)
# admin.site.register(Person, PersonAdmin)
