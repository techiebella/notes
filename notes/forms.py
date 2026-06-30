from django import forms
from .models import Note, Category


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note

        fields = [
            "title",
            "content",
            "category",
            "priority",
            "color",
            "is_pinned",
            "is_favorite",
            "is_archived",
        ]

        labels = {
            "title": "Note Title",
            "content": "Content",
            "category": "Category",
            "priority": "Priority",
            "color": "Color",
            "is_pinned": "Pin this Note",
            "is_favorite": "Mark as Favorite",
            "is_archived": "Archive this Note",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter note title"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your thoughts here..."
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "color": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "is_pinned": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "is_favorite": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "is_archived": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)   # IMPORTANT FIX

        super().__init__(*args, **kwargs)

        # FIX: your Category model has NO user field
        self.fields["category"].queryset = Category.objects.all()

        # optional category selection
        self.fields["category"].required = False

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if not title or len(title.strip()) < 3:
            raise forms.ValidationError(
                "Title must be at least 3 characters long."
            )

        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")

        if not content or len(content.strip()) < 10:
            raise forms.ValidationError(
                "Content must be at least 10 characters long."
            )

        return content