from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    is_candidate = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate')
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)  
    address = models.TextField()
    resume = models.FileField(upload_to='resumes/') 

    @property
    def age(self):
        today = datetime.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return self.full_name

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    address = models.TextField()
    is_agency = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Agency(models.Model):
    name = models.CharField(max_length=255)  # Required
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    employers = models.ManyToManyField(Employer, related_name='agencies')

    def __str__(self):
        return self.name

class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    plan_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text='Duration in days')
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_name
