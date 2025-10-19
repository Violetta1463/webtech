from django.shortcuts import render
from datetime import date

def home(request):
    message = None
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            message = f"Спасибо, {name}!"
        else:
            message = "Пожалуйста, введите имя."
    context = {
        "course": "Технология разработки web-приложений",
        "today": date.today(),
        "message": message,
    }
    return render(request, "pages/home.html", context)
