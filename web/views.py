from django.db.models.aggregates import Count
from django.views.generic import TemplateView
from reviews.models import Review
from services.models import Barber


class IndexView(TemplateView):
    template_name = 'web/home-page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_three_barbers'] = Barber.objects.annotate(bookings_count=Count('bookings')).order_by('-bookings_count')[:3]
        context['last_five_reviews'] = Review.objects.all().order_by('-created_at')[:5]
        return context