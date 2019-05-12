from django.db import models


class AddressDetail(models.Model):
    street_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    complete_address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.complete_address

    def save(self, *args, **kwargs):
        self.complete_address = "{}, {}, {}-{}".format(self.street_address, self.city, self.state, self.pincode)
        self.complete_address = self.complete_address.replace('None, ', '').replace('None-', '').replace('-None', '')
        super(AddressDetail, self).save(*args, **kwargs)

    @property
    def coordinates(self):
        return "{},{}".format(self.latitude, self.longitude)
