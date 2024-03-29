from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def save_file(request, file):
    file_name = file.name
    file_path = default_storage.save(f"static/save-file/{file_name}", ContentFile(file.read()))
    url = request.build_absolute_uri(default_storage.url(file_path))
    return url