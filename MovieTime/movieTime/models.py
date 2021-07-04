from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Movie(models.Model):
	movie_name = models.CharField(max_length=500)
	genre = models.CharField(max_length=1000)
	image = models.ImageField(default='default.jpg', upload_to='posters')

	def __str__(self):
		return self.movie_name

	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)	

class Shows(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	time = models.TimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	date = models.DateField(default=timezone.now)
	theater_name = models.CharField(max_length=300)
	gold_seats = models.PositiveIntegerField(default=1)
	silver_seats = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.theater_name

class Ticket(models.Model):
	movie = models.CharField(max_length=500)
	date = models.DateField(default=timezone.now)
	time = models.TimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	theater_name = models.CharField(max_length=300)
	seat_type = models.CharField(max_length=15)
	number = models.PositiveIntegerField(default=1)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return f'{self.user} ticket'

class Payment(models.Model):
	card_num = models.PositiveIntegerField(default=0)
	card_type = models.CharField(max_length=8)
	cvv = models.PositiveIntegerField(default=0)
	expiry_month = models.PositiveIntegerField(default=0)
	expiry_year = models.PositiveIntegerField(default=0)
	holder_name = models.CharField(max_length=50)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user} payment'
