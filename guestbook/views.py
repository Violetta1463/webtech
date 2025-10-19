from django.shortcuts import render, redirect
from .forms import EntryForm
from .models import Entry

def guestbook_view(request):
    form = EntryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('guestbook')
    entries = Entry.objects.all()
    return render(request, 'guestbook/guestbook_list.html', {'form': form, 'entries': entries})
