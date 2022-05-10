from django.http import HttpResponse, Http404


def open_file(request, *args, **kwargs):
    file_path = "Test01"

    response = HttpResponse("Hello", content_type="text/plain")
    response["Content-Disposition"] = "inline; filename=" + os.path.basename(file_path)
