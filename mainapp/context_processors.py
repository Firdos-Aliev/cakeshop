from django.utils.timezone import now


def time(request):
    return {
        "time": now()
    }
