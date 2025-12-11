from django.shortcuts import render, redirect
from django.http import FileResponse
from .models import Destination, JournalEntry
from .forms import DestinationForm, JournalEntryForm
import requests
import pandas as pd


# Create your views here.
def home(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # Trip form submitted
        if form_type == "destination":
            trip_form = DestinationForm(request.POST)
            journal_form = JournalEntryForm()  # empty

            if trip_form.is_valid():
                dest = trip_form.save(commit=False)

                lat, lng = get_lat_lng(dest.city, dest.country)
                dest.latitude = lat
                dest.longitude = lng

                dest.save()
                return redirect("home")

        # Journal form submitted
        elif form_type == "journal":
            trip_form = DestinationForm()
            journal_form = JournalEntryForm(request.POST, request.FILES)

            if journal_form.is_valid():
                journal_form.save()
                return redirect("home")

        else:
            # Just re-render with blank forms
            trip_form = DestinationForm()
            journal_form = JournalEntryForm()

    else:
        # GET request: show blank forms
        trip_form = DestinationForm()
        journal_form = JournalEntryForm()

    destinations = Destination.objects.all()
    journal_entries = (
        JournalEntry.objects.select_related("city").all().order_by("-id")
    )

    total_countries = Destination.objects.values("country").distinct().count()
    total_trips = destinations.count()
    upcoming_trips = destinations.filter(visited=False).count()

    context = {
        "trip_form": trip_form,
        "journal_form": journal_form,
        "destinations": destinations,
        "journal_entries": journal_entries,
        "total_countries": total_countries,
        "total_trips": total_trips,
        "upcoming_trips": upcoming_trips,
    }

    return render(request, "home.html", context)


def get_lat_lng(city: str, country: str):
    """
    Return (lat, lng) for a 'City, Country' string using OpenStreetMap Nominatim.
    """
    if not city or not country:
        return None, None

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{city}, {country}",
        "format": "json",
        "limit": 1,
    }
    headers = {
        # Nominatim requires a User-Agent that identifies your app
        "User-Agent": "passport-travellog/1.0 (erika_ramirez@icloud.com)",
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None, None
    
def export_to_xlsx(request):
    data = Destination.objects.all().values(
        "country",
        "city",
        "visited",
        "start_date",
        "end_date",
        "latitude",
        "longitude",
    )

    df = pd.DataFrame.from_records(data)

    file_path = "passport_trips.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="passport_trips.xlsx",
    )