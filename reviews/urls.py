from django.urls import path, include

from reviews.views import ListReviewsView, CreateReviewView, ReviewDetailsView, EditReviewView, DeleteReviewView

app_name = 'reviews'

urlpatterns = [
    path('', ListReviewsView.as_view(), name='list'),
    path('create/', CreateReviewView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('details/', ReviewDetailsView.as_view(), name='details'),
        path('edit/', EditReviewView.as_view(), name='edit'),
        path('delete/', DeleteReviewView.as_view(), name='delete')
    ]))
]