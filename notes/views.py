from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Category, Note
from .forms import NoteForm


# ==========================
# DASHBOARD
# ==========================
@login_required
def dashboard(request):

    notes = Note.objects.filter(user=request.user, is_deleted=False)

    context = {
        "total_notes": notes.count(),
        "pinned_notes": notes.filter(is_pinned=True).count(),
        "favorite_notes": notes.filter(is_favorite=True).count(),
        "archived_notes": notes.filter(is_archived=True).count(),
        "recent_notes": notes.order_by("-updated_at")[:5],
    }

    return render(request, "notes/dashboard.html", context)


# ==========================
# CREATE NOTE
# ==========================
@login_required
def create_note(request):

    if request.method == "POST":
        form = NoteForm(request.POST, user=request.user)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            messages.success(request, "Note created successfully!")
            return redirect("dashboard")

    else:
        form = NoteForm(user=request.user)

    return render(request, "notes/create_note.html", {"form": form})


# ==========================
# NOTES LIST (FILTER + SEARCH)
# ==========================
@login_required
def notes_list(request):

    notes = Note.objects.filter(user=request.user, is_deleted=False)

    search = request.GET.get("search")
    category = request.GET.get("category")
    priority = request.GET.get("priority")
    status = request.GET.get("status")
    sort = request.GET.get("sort")

    if search:
        notes = notes.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    if category:
        notes = notes.filter(category_id=category)

    if priority:
        notes = notes.filter(priority=priority)

    if status == "favorite":
        notes = notes.filter(is_favorite=True)

    elif status == "pinned":
        notes = notes.filter(is_pinned=True)

    elif status == "archived":
        notes = notes.filter(is_archived=True)

    if sort == "oldest":
        notes = notes.order_by("created_at")
    else:
        notes = notes.order_by("-is_pinned", "-updated_at")

    context = {
        "notes": notes,
        "categories": Category.objects.all(),
        "search": search,
        "selected_category": category,
        "selected_priority": priority,
        "selected_status": status,
        "selected_sort": sort,
    }

    return render(request, "notes/note_list.html", context)


# ==========================
# EDIT NOTE
# ==========================
@login_required
def edit_note(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=False)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect("note_list")

    else:
        form = NoteForm(instance=note, user=request.user)

    return render(request, "notes/edit_note.html", {"form": form, "note": note})


# ==========================
# SOFT DELETE (MOVE TO TRASH)
# ==========================
@login_required
def delete_note(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user)

    if request.method == "POST":
        note.is_deleted = True
        note.save()

        messages.success(request, "Note moved to trash!")
        return redirect("note_list")

    return render(request, "notes/delete_note.html", {"note": note})


# ==========================
# TRASH LIST
# ==========================
@login_required
def trash_list(request):

    notes = Note.objects.filter(user=request.user, is_deleted=True)

    return render(request, "notes/trash_list.html", {"notes": notes})


# ==========================
# RESTORE NOTE
# ==========================
@login_required
def restore_note(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=True)

    note.is_deleted = False
    note.save()

    messages.success(request, "Note restored successfully!")
    return redirect("trash_list")


# ==========================
# QUICK ACTIONS
# ==========================
@login_required
def toggle_pin(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=False)
    note.is_pinned = not note.is_pinned
    note.save()

    return redirect("note_list")


@login_required
def toggle_favorite(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=False)
    note.is_favorite = not note.is_favorite
    note.save()

    return redirect("note_list")


@login_required
def toggle_archive(request, pk):

    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=False)
    note.is_archived = not note.is_archived
    note.save()

    return redirect("note_list")