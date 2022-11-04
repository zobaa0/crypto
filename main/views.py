from django.shortcuts import redirect, render
from django.contrib import messages
from dashboard.models import Subscription, Withdrawal
from .forms import ContactForm

# Create your views here.
def home(request):
    sub = Subscription.objects.all()
    withdraw = Withdrawal.objects.all()
    context = {
        'sub': sub,
        'withdraw': withdraw
    }
    return render(request, 'main/index.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send()
            messages.success(request, ('Thank you for contacting us. Our team will reach out to you soon.'))
            return redirect('main:contact')
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'main/contact.html', context)


def plans(request):
    return render(request, 'main/plans.html')

def about(request):
    return render(request, 'main/about.html')

def faq(request):
    return render(request, 'main/faq.html')

def privacy(request):
    return render(request, 'main/privacy.html')

def terms(request):
    return render(request, 'main/terms.html')

def services(request):
    return render(request, 'main/services.html')

def howto(request):
    return render(request, 'main/howto.html')

def refund(request):
    return render(request, 'main/refund.html')