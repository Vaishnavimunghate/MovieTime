from django.contrib import admin
from .models import Movie, Shows, Ticket, Payment

admin.site.register(Movie)
admin.site.register(Shows)
admin.site.register(Ticket)
admin.site.register(Payment)