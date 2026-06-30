from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Note(models.Model):

    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )

    COLOR_CHOICES = (
        ("Primary", "Primary"),
        ("Success", "Success"),
        ("Warning", "Warning"),
        ("Danger", "Danger"),
        ("Info", "Info"),
        ("Dark", "Dark"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    content = models.TextField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="Primary"
    )

    # ===== QUICK ACTION FLAGS =====
    is_pinned = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    # 🗑️ Soft delete (Trash system)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-is_pinned",      # pinned first
            "-is_favorite",    # favorites next
            "-updated_at"      # latest updated first
        ]

        indexes = [
            models.Index(fields=["user", "is_deleted"]),
            models.Index(fields=["user", "is_archived"]),
            models.Index(fields=["user", "is_favorite"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    # ===== OPTIONAL HELPERS (VERY USEFUL IN VIEWS) =====

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.save(update_fields=["is_pinned"])

    def toggle_favorite(self):
        self.is_favorite = not self.is_favorite
        self.save(update_fields=["is_favorite"])

    def toggle_archive(self):
        self.is_archived = not self.is_archived
        self.save(update_fields=["is_archived"])

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])