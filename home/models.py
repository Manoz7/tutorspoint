from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.status
    
class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=250, blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, default="")
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.name


class Subject(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    sub_desc = models.TextField()
    
    def __str__(self) -> str:
        return self.sub_name
    
    def get_num_tutors(self):
        return Tutor.objects.filter(subject=self).count()
    
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='customer/', null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Tutor(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='tutor/', null=True)
    cert = models.FileField(upload_to='tutor/', null=True, default='tutor/certificate.png')
    
    address = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=100, null=True)
    # subject = models.ManyToManyField(Subject, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    experience = models.IntegerField(default=0)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Booking(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=50, null=True)
    book_hours = models.IntegerField(default="")
    book_days = models.IntegerField(default="")
    
    def __str__(self) -> str:
        return self.customer.user.first_name+" books "+self.user.user.first_name


class BookUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField(default="")
    
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:30] + "...." 