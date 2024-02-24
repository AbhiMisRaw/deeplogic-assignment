from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileUploadForm
from dataExtractor.celery import process_text
from celery.result import AsyncResult
import os

def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            save_path = os.path.join(settings.MEDIA_ROOT, request.FILES['file_object'].name)
            print("---------")
            print(os.path.splitext(request.FILES['file_object'].name))
            with open(save_path, 'wb') as file:
                for chunk in request.FILES['file_object'].chunks():
                    file.write(chunk)
            task = process_text.delay(save_path)
            return redirect('result', task.id)
    else:
        form = FileUploadForm()
    return render(request, 'extractor_app/index.html', {'form': form})


def result_view(request, result_id):
    result = AsyncResult(result_id)
    context = {'task_id': result_id}

    if result.state == 'PENDING':
        context['status'] = 'pending'
    elif result.state == 'SUCCESS':
        context['status'] = 'completed'
        if result.result['status'] == 'success':
            print(result.result)
            # Get the absolute path to the CSV file
            absolute_csv_file_path = os.path.splitext(result.result.get('file_path'))[0] + '.csv'

            # Get the relative path from the '/media/' directory
            relative_csv_file_path = os.path.relpath(absolute_csv_file_path, settings.MEDIA_ROOT)

            # Construct the full file path
            csv_file_path = os.path.join(settings.MEDIA_URL, relative_csv_file_path)

            if os.path.exists(absolute_csv_file_path):
                context['message'] = 'Text is valid and in English. CSV file created.'
                context['csv_file_path'] = csv_file_path
            else:
                context['message'] = 'CSV file not found.'
        else:
            context['error'] = True
            context['message'] = 'Text is noisy or not in English. CSV creation failed.'
    else:
        context['status'] = 'error'
        context['message'] = f"Task state: {result.state}"

    return render(request, 'extractor_app/result.html', context)