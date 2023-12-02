from django.contrib.gis.geos import Point
from theater.models import Theater

def theater_create(
    *,
    name: str,
    address: str,
    short_address: str,
    location: Point,
    zip_code: str,
    technologies: list,
    cuisines: list,
    shows: list,
    no_of_rows: int,
    no_of_cols: int
) -> Theater:
    theater = Theater.objects.create(
        name=name,
        address=address,
        short_address=short_address,
        location=location,
        zip_code=zip_code,
        technologies=technologies,
        cuisines=cuisines,
        shows=shows,
        no_of_rows=no_of_rows,
        no_of_cols=no_of_cols
    )
    return theater
