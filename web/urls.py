from django.urls.conf import path

from web.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home-page'),

]