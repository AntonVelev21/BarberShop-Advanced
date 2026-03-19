from django.urls.conf import path

from web.views import index

urlpatterns = [
    path('', index, name='home-page'),

]