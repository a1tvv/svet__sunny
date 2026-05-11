from django.shortcuts import render

def index(request):
    sheikh = {
        'links': {
            'rinat': 'https://t.me/toislam',
            'abu_yahya': 'https://t.me/abuyahya_net',
            'siraj': 'https://t.me/sirajabutalha',
        }
    }
    return render(request, 'index.html', sheikh)

def sira(request):
    return render(request, 'sira.html')