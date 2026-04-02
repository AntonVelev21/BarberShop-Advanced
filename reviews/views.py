from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from reviews.forms import ReviewCreateForm, ReviewEditForm
from reviews.models import Review
from services.models import Barber


class ListReviewsView(ListView):
    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        barber_id = self.request.GET.get('barber')
        if barber_id:
           return Review.objects.filter(barber_id=barber_id)
        return Review.objects.all()


class ReviewDetailsView(DetailView):
    model = Review
    template_name = 'reviews/details.html'
    context_object_name = 'review'


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    success_url = reverse_lazy('home-page')
    context_object_name = 'review'
    template_name = 'reviews/form.html'

    def get_initial(self):
        initial = super().get_initial()
        barber_id = self.request.GET.get('barber')
        if barber_id:
            barber = get_object_or_404(Barber, id=barber_id)
            initial['barber'] = barber.id
        return initial
    
    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = self.request.user.user_profile
        review.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    success_url = reverse_lazy('home-page')
    context_object_name = 'review'
    template_name = 'reviews/form.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('home-page')
    context_object_name = 'review'
    template_name = 'reviews/delete.html'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('accounts.have_full_access'):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
