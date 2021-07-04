from django import forms
from .models import Movie, Shows, Ticket, Payment

class PaymentForm(forms.ModelForm):
	card_num = forms.IntegerField()
	card_type = forms.CharField()
	cvv = forms.IntegerField()
	expiry_month = forms.IntegerField()
	expiry_year = forms.IntegerField()
	holder_name = forms.CharField()

	class Meta:
		model = Payment
		fields = ['card_num', 'card_type', 'cvv', 'expiry_month', 'expiry_year', 'holder_name']

class Form(forms.Form):
	number = forms.IntegerField()
	CHOICES =( 
	    ("1", "Gold"), 
	    ("2", "Silver"), 
	) 			
	seat_type = forms.ChoiceField(choices = CHOICES)