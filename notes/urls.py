from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # CORE PAGES
    # ==========================
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_note, name="create_note"),
    path("all/", views.notes_list, name="note_list"),

    # ==========================
    # NOTE ACTIONS
    # ==========================
    path("edit/<int:pk>/", views.edit_note, name="edit_note"),
    path("delete/<int:pk>/", views.delete_note, name="delete_note"),

    # ==========================
    # QUICK ACTIONS (Phase 6)
    # ==========================
    path("pin/<int:pk>/", views.toggle_pin, name="toggle_pin"),
    path("favorite/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("archive/<int:pk>/", views.toggle_archive, name="toggle_archive"),

    # ==========================
    # TRASH SYSTEM
    # ==========================
    path("trash/", views.trash_list, name="trash_list"),
    path("restore/<int:pk>/", views.restore_note, name="restore_note"),
]