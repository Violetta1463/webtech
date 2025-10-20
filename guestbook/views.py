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


from django.core.paginator import Paginator
from django.db.models import Q

def guestbook_view(request):
    form = EntryForm(request.POST or None)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            from django.contrib import messages
            messages.error(request, 'Чтобы оставлять записи, войдите или зарегистрируйтесь')
            return redirect('login')
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            from django.contrib import messages
            messages.success(request, 'Запись добавлена')
            return redirect('guestbook')

    q = request.GET.get('q', '').strip()
    qs = Entry.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(message__icontains=q))

    paginator = Paginator(qs, 5)  # по 5 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'guestbook/guestbook_list.html', {
        'form': form,
        'page_obj': page_obj,
        'q': q,
    })


from django.shortcuts import get_object_or_404
from django.contrib import messages

def guestbook_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'guestbook/guestbook_detail.html', {'entry': entry})

def guestbook_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    form = EntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Запись обновлена')
        return redirect('guestbook-detail', pk=entry.pk)
    return render(request, 'guestbook/guestbook_form.html', {'form': form, 'entry': entry})

def guestbook_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Запись удалена')
        return redirect('guestbook')
    return render(request, 'guestbook/guestbook_confirm_delete.html', {'entry': entry})


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def signup(request):
   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
           user = form.save()
           auth_login(request, user)  # сразу войдём
           from django.contrib import messages
           messages.success(request, 'Аккаунт создан и выполнен вход')
           return redirect('guestbook')
   else:
       form = UserCreationForm()
   return render(request, 'registration/signup.html', {'form': form})


from django.contrib.auth.decorators 
import login_required

@login_required
def guestbook_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if not (entry.user == request.user or request.user.is_staff):
        messages.error(request, 'Недостаточно прав')
        return redirect('guestbook-detail', pk=pk)
    form = EntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Запись обновлена')
        return redirect('guestbook-detail', pk=entry.pk)
    return render(request, 'guestbook/guestbook_form.html', {'form': form, 'entry': entry})

@login_required
def guestbook_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if not (entry.user == request.user or request.user.is_staff):
        messages.error(request, 'Недостаточно прав')
        return redirect('guestbook-detail', pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Запись удалена')
        return redirect('guestbook')
    return render(request, 'guestbook/guestbook_confirm_delete.html', {'entry': entry})
