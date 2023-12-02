from theater.models import Theater


def theater_get(**kwargs) -> Theater:
    return Theater.objects.get(**kwargs)
