import pytest
from django.urls import reverse
from travellog.models import Destination, JournalEntry
from travellog.views import get_lat_lng
import datetime


@pytest.mark.django_db
def test_destination_model_creation():
    dest = Destination.objects.create(
        country="US",
        city="Pittsburgh",
        visited=False,
        start_date=datetime.date(2023, 5, 1),
        end_date=datetime.date(2023, 5, 7),
    )

    assert Destination.objects.count() == 1
    assert dest.city == "Pittsburgh"
    assert dest.visited is False


@pytest.mark.django_db
def test_journal_entry_creation():
    dest = Destination.objects.create(
        country="US",
        city="New York",
        visited=True,
        start_date=datetime.date(2024, 1, 1),
        end_date=datetime.date(2024, 1, 10),
    )

    entry = JournalEntry.objects.create(
        city=dest,
        rating=4,
        notes="Great trip!",
    )

    assert JournalEntry.objects.count() == 1
    assert entry.rating == 4
    assert entry.city.city == "New York"


def test_get_lat_lng():
    lat, lng = get_lat_lng("Paris", "France")
    assert round(lat) == round(48.8534951)
    assert round(lng) == round(2.3483915)


@pytest.mark.django_db
def test_homepage_loads(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
