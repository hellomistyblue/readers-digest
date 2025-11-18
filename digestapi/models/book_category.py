from django.db import models
from .book import Book
from .category import Category

class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='book_categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'book_category'
        unique_together = ('book', 'category') 
