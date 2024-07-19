from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError
from django import forms

class Trigger(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_isbn_number(self):
        isbn_number = self.cleaned_data.get('isbn_number')
        if not isbn_number:
            raise forms.ValidationError("ISBN number field is required.")
        # Regular expression pattern for ISBN format ISBN{genre}{3 digit number}
        pattern = r'^ISBN[A-Za-z]{2,5}[0-9]{3}$'

        if not re.match(pattern, isbn_number):
            raise forms.ValidationError("Invalid ISBN format. Please use the format ISBN{genre with 2 to 5 characters}{3 digit number}.")
        return isbn_number

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email',)
    search_fields = ('student_id', 'first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    form = Trigger
    list_display = ('book_id', 'isbn_number', 'title', 'author',)
    search_fields = ('book_id', 'isbn_number', 'title', 'author',)
    list_filter = ('genre',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name')


class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'first_name', 'last_name', 'email',)
    search_fields = ('admin_id', 'first_name', 'last_name', 'email',)


admin.site.register(Student, StudentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Admin, AdminAdmin)
