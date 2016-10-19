from django.db import models



class Regions(models.Model):
    region_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class CountriesValues(models.Model):
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)

    country = models.CharField(max_length=60)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.country
