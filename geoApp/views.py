import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from .models import Record


def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            return render(request, 'upload.html', {
                'errors': ['Файл содержит неверный JSON.'],
                'success': False
            })

        errors = []
        success_count = 0

        for idx, item in enumerate(data):
            name = item.get('name')
            date_str = item.get('date')


            if not isinstance(name, str) or len(name) >= 50:
                errors.append(f'Строка {idx + 1}: "name" должно быть строкой длиной менее 50 символов.')
                continue

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
            except (TypeError, ValueError):
                errors.append(f'Строка {idx + 1}: "date" должно быть в формате YYYY-MM-DD_HH:mm.')
                continue


            Record.objects.create(name=name, date=date_obj)
            success_count += 1

        if not errors:
            return render(request, 'upload.html', {
                'success': True,
                'success_count': success_count
            })
        else:
            return render(request, 'upload.html', {
                'errors': errors,
                'success': False
            })

    return render(request, 'upload.html')

def show_table(request):
    records = Record.objects.all().order_by('-date')  
    return render(request, 'table.html', {'records': records})


def map_view(request):
    return render(request, 'map.html')