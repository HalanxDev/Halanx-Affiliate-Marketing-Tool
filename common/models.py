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


class BankDetail(models.Model):
    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_type = models.CharField(max_length=10, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    bank_branch = models.CharField(max_length=300, blank=True, null=True)
    bank_branch_address = models.CharField(max_length=300, blank=True, null=True)
    ifsc_code = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

