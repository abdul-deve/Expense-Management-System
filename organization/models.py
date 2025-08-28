from django.db import models
from django.contrib.auth import  get_user_model
from django.core.validators import ValidationError
from uuid import uuid4



class TimeStampUniqueId(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,db_index=True)
    created_at  =models.DateTimeField(auto_now_add=True)
    updated_at  =models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class TimeStampUniqueId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampUniqueId):
    id = models.UUIDField(primary_key=True,default=uuid4,db_index=True)
    ORG_TYPES = [
        ("IT", "Information Technology"),
        ("FIN", "Finance"),
        ("HR", "Human Resources"),
        ("MKT", "Marketing"),
        ("EDU", "Education"),
        ("HEALTH", "Healthcare"),
        ("LOG", "Logistics"),
        ("MANUF", "Manufacturing"),
        ("SALES", "Sales"),
        ("OTH", "Other")
    ]
    owner = models.OneToOneField(User,on_delete=models.CASCADE,db_index=True,related_name="organization_owner")
    name  = models.CharField(max_length=255)
    type = models.CharField(max_length=25,choices=ORG_TYPES)
    address = models.CharField(max_length=50)
    num_of_employee = models.IntegerField(default=0,null=True)
    max_employee = models.IntegerField()

    def current_employee_count(self):
        return self.employees.count()

    def can_add_employee(self):
        return self.current_employee_count() < self.max_employee

    def increment_employee_count(self):
        self.num_of_employee = self.current_employee_count() + 1
        self.save(update_fields=['num_of_employee'])

    def decrement_employee_count(self):
        self.num_of_employee = max(0, self.current_employee_count() - 1)
        self.save(update_fields=['num_of_employee'])



class Employee(TimeStampUniqueId):
    POSITION = [
        ("E", "Employee"),
        ("P", "Project Manager"),
        ("T", "Team Leader"),

    ]
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,db_index=True,related_name="employees")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_profile", db_index=True)
    position = models.CharField(max_length=255, choices=POSITION, db_index=True)
    salary = models.IntegerField()

    class Meta:
        unique_together = ("organization", "user")

    def __str__(self):
        return f"{self.user.username} - {self.get_position_display()}"

