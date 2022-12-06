from django import forms
from django.utils.timezone import datetime, timedelta
from . models import ArmorReview

class ArmorReviewForm(forms.ModelForm):
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if valid:
            buyer = self.cleaned_data.get("buyer")
            recent_posts = ArmorReview.objects.filter(
                buyer=buyer, 
                created_at__gte=(datetime.now()-timedelta(hours=1))
            )
            if recent_posts:
                return False
        return valid

    class Meta:
        model = ArmorReview
        fields = ('content', 'armor', 'buyer', )
        widgets = {
            'armor': forms.HiddenInput(),
            'buyer': forms.HiddenInput(),
        }