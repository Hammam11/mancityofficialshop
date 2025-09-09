from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Hammam Muhammad Mubarak',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
