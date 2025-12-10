from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField

# Create your models here.

class Destination(models.Model):
    # Country
    # City
    # Dates visited

    country = CountryField()
    city = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    visited = models.BooleanField()
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return f"{self.id}: {self.country}, {self.city} visited from {self.start_date} to {self.end_date}"
    
class JournalEntry(models.Model):
    # Foreign key = Destination.city
    # Rating
    # Notes
    # Image ?
    city = models.ForeignKey(Destination, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f"{self.id}: {self.city} rated {self.rating}/5"