from django import forms
from django.forms import ModelForm
from .models import Review


class NewReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('overall_rating', 'difficulty_rating', 'user_name', 'user_email', 'review_title', 'review_text')