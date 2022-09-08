from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from .models import Poem, Comment, Category

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('created', 'body', 'active')
    readonly_fields = ('created', 'body')

@admin.register(Poem)
class PoemAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('id', 'title', 'count_view', 'get_html_photo', 'is_published', 'count_comm')
    list_display_links = ('id', 'title')
    readonly_fields = ('get_html_photo', 'count_view', 'time_update', 'photo')
    exclude = ('count_view',)
    search_fields = ('title', 'content')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]
    save_on_top = True
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo}' width=130>")
    def count_comm(self, object):
        return len(Comment.objects.filter(poem=object.id))
    get_html_photo.short_description = "Миниатюра"
    count_comm.short_description = "Кол-во комментов"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'poem', 'body', 'active')
    list_display_links = ('name', 'poem')
    readonly_fields = ('ip', 'sess',)
    list_editable = ('active',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    
    
admin.site.site_title = 'Админ-панель «Antonio»'
admin.site.site_header = 'Админ-панель «Antonio»'