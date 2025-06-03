from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm

def home(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MessageForm()

    messages = Message.objects.all()
    return render(request, 'board/home.html', {'form': form, 'messages': messages})
