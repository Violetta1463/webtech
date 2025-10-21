from django.shortcuts import render, redirect
from .forms import EntryForm
from .models import Entry
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Entry
from .forms import EntryForm

class SearchMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(message__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '').strip()
        return ctx

class EntryListView(SearchMixin, ListView):
    model = Entry
    template_name = 'guestbook/entry_list.html'
    paginate_by = 5

class EntryDetailView(DetailView):
    model = Entry
    template_name = 'guestbook/entry_detail.html'
    context_object_name = 'entry'

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'guestbook/entry_form.html'
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        from django.contrib import messages
        messages.success(self.request, 'Запись добавлена')
        return reverse('guestbook-detail', args=[self.object.pk])

class OwnerOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (obj.user == self.request.user) or self.request.user.is_staff
    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, 'Недостаточно прав')
        return super().handle_no_permission()

class EntryUpdateView(LoginRequiredMixin, OwnerOrStaffRequired, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'guestbook/entry_form.html'
    def get_success_url(self):
        from django.contrib import messages
        messages.success(self.request, 'Запись обновлена')
        return reverse('guestbook-detail', args=[self.object.pk])

class EntryDeleteView(LoginRequiredMixin, OwnerOrStaffRequired, DeleteView):
    model = Entry
    template_name = 'guestbook/entry_confirm_delete.html'
    success_url = reverse_lazy('guestbook')
    def delete(self, request, *args, **kwargs):
        from django.contrib import messages
        messages.success(self.request, 'Запись удалена')
        return super().delete(request, *args, **kwargs)


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

def guestbook_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'guestbook/guestbook_detail.html', {'entry': entry})

@login_required
def guestbook_my(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    page_obj = Entry.objects.all()
    return render(request, 'guestbook/guestbook_my.html', {'entry': entry, 'page_obj': page_obj})

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