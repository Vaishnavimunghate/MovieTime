from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Shows, Ticket, Payment
from .forms import PaymentForm, Form
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

def home(request):
	context = {
		'movies': Movie.objects.all()
	}
	return render(request,'movieTime/home.html', context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    t_form = Form()
    return render(request, 'movieTime/movie_detail.html', {'movie':movie, 't_form':t_form})

def book(request, movie_id, shows_id):
	movie = get_object_or_404(Movie, pk=movie_id)
	show = Shows.objects.get(pk=shows_id)
	name = show.movie
	time = show.time
	date = show.date
	theater_name = show.theater_name
	gold_seats = show.gold_seats
	silver_seats = show.silver_seats
	gs = show.gold_seats
	ss = show.silver_seats
	if request.POST:
		number = request.POST.get('number')
		seat_type = request.POST.get('seat_type')
		show.delete()
		seat = 'Gold'
		if seat_type=='1':
			price=(250)*int(number)
			seat = 'Gold'
			gs = int(gold_seats) - int(number)
		else:
			price=(200)*int(number)
			seat = 'Silver'
			ss = int(silver_seats) - int(number)
		show1 = Shows(movie=name, date=date, time=time, theater_name=theater_name, gold_seats=gs, silver_seats=ss)
		show1.save()
		ticket = Ticket(movie=name, date=date, time=time, theater_name=theater_name, seat_type=seat, number=number)
		ticket.user = request.user
		ticket.save()	
		return render(request, 'movieTime/book.html', {'ticket':ticket, 'price':price})	
	else:
		return redirect('home')	

@login_required
def bookings(request):
	return render(request,'movieTime/bookings.html')	

@login_required
def cancel(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    quantity = ticket.number
    seat = ticket.seat_type
    time = ticket.time
    date = ticket.date
    theater_name = ticket.theater_name
    name= ticket.movie
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if str(curr_date) > str(date):
        messages.error(request, f'Out of date!')
        return redirect('bookings') 
    else:
        if str(curr_date) == str(date):
            if str(curr_time) >= str(time):
                messages.error(request, f'Out of date!')
                return redirect('bookings')
    ticket.delete() 
    shows = Shows.objects.all()
    gold_seats = 20
    silver_seats = 10
    gs = 20
    ss = 10	
    for show in shows:
        if str(ticket.movie) == str(show.movie):
            if str(ticket.date) == str(show.date):
                if str(ticket.time) == str(show.time):
                    if str(ticket.theater_name) == str(show.theater_name):
                        gold_seats = show.gold_seats
                        silver_seats = show.silver_seats
                        gs = show.gold_seats
                        ss = show.silver_seats	 
                        show.delete()
    if seat == 'Gold':
        price = (200)*quantity
        gs = int(gold_seats) + int(quantity)
    else:     
        price = (150)*quantity
        ss = int(silver_seats) + int(quantity)				    
    show1 = Shows(date=date, time=time, theater_name=theater_name, gold_seats=gs, silver_seats=ss)
    show1.movie = Movie.objects.filter(movie_name=name).first()
    show1.save()          
    return render(request, 'movieTime/cancel.html', {'price':price})	

class PaymentView(TemplateView):
	template_name = 'movieTime/payment.html'

	def get(self, request):
		p_form = PaymentForm()
		return render(request, self.template_name, {'p_form':p_form})	
	
	def post(self, request):
		form = PaymentForm(request.POST)
		if form.is_valid():
			card_num = request.POST.get('card_num')
			card_type = request.POST.get('card_type')
			cvv = request.POST.get('cvv')
			month = request.POST.get('expiry_month')
			year = request.POST.get('expiry_year')
			if card_type != 'Credit':
				if card_type != 'Debit':
					messages.error(request, f'Card Types are: Credit or Debit')
					return redirect('pay')
			if len(card_num) != 12:
				messages.error(request, f'card number should have exactly 12 digits!')
				return redirect('pay')
			if len(cvv) != 3:
				messages.error(request, f'cvv should have exactly 3 digits!')
				return redirect('pay')
			if int(month)>12 or int(month)<1:
				messages.error(request, f'month should be between 01 to 12!')
				return redirect('pay')
			if int(year) <= 00 or int(year) >= 99:
				messages.error(request, f'enter last two digits of the year!')
				return redirect('pay')	
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			form = PaymentForm()
			messages.success(request, f'Tickets Successfully Booked!')
			return redirect('bookings')

		args = {'p_form': p_form}
		return render(request, self.template_name, args)


	
