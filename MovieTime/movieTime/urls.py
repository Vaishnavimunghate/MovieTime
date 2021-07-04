from django.urls import path
from django.conf.urls import url
from . import views
from .views import PaymentView

urlpatterns = [
	path('', views.home, name='home'),
	url(r'^movie/(?P<movie_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^movie/(?P<movie_id>[0-9]+)/(?P<shows_id>[0-9]+)/$', views.book ,name='book'),
	url(r'^payment/$', PaymentView.as_view() , name='pay'),
	path('bookings/', views.bookings, name='bookings'),
	url(r'^bookings/(?P<ticket_id>[0-9]+)/', views.cancel, name='cancel'),
]