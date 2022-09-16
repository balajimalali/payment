from django.db import models

# Create your models here.


class Show(models.Model):
    show_no = models.AutoField(primary_key=True)
    show_name = models.CharField(max_length=50, null=False, unique=True)
    speaker = models.CharField(max_length=50)
    date = models.DateTimeField()
    price = models.IntegerField()
    venue = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=500, blank=True)
    avl_tkt = models.IntegerField()
    sold_tkt = models.IntegerField(default=0)

    def __str__(self):
        return self.show_name


class Transaction(models.Model):
    txn_id = models.CharField(max_length=40, unique=True, primary_key=True)
    txn_id_pu = models.CharField(max_length=50, blank=True)
    mode_err = models.CharField(max_length=100, blank=True)
    showname = models.CharField(max_length=50)
    txntime = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.txn_id


