from django.forms.models import ModelForm
from reviews.models import Review



class BaseReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateForm(BaseReviewForm):
    ...


class ReviewEditForm(BaseReviewForm):
    ...


class ReviewDeleteForm(BaseReviewForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True