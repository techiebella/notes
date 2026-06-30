from django.contrib import admin
from .models import Category, Note


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = ("name",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "category",
        "priority",
        "is_pinned",
        "is_favorite",
        "is_archived",
        "updated_at",
    )

    list_filter = (
        "priority",
        "is_pinned",
        "is_favorite",
        "is_archived",
        "category",
    )

    search_fields = (
        "title",
        "content",
    )

    ordering = ("-updated_at",)