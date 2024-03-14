from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from project.settings import MEDIA_ROOT

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        COMPANY = "COMPANY", "Company"

    base_role = Role.EMPLOYEE

    is_staff = None 
    is_superuser = None 
    groups_id = None 
    user_permissions_id = None 
    user_permissions = None
    groups = None

    email = models.EmailField(unique=True)
    # access_token = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True) 

    is_deleted = models.BooleanField(null=False, default=False)
    is_employee = models.BooleanField(null=False, default=False)
    is_company = models.BooleanField(null=False, default=False)

    extenstion = models.CharField(max_length=50, unique=True, null=True, blank=True)
    company = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='employees', null=True, blank=True)
    photo = models.FileField(upload_to=MEDIA_ROOT, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class CompanyManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.COMPANY)


# Proxy model
class Company(User):
    base_role = User.Role.COMPANY

    Company = CompanyManager()

    class Meta:
        proxy = True


class EmployeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEE)


# Proxy model
class Employee(User):
    base_role = User.Role.EMPLOYEE

    Employee = EmployeeManager()

    class Meta:
        proxy = True


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField(User, related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    starred = models.BooleanField(default=False, blank=True)
    deleted = models.BooleanField(default=False, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.sender.first_name + " " + self.sender.last_name,
            "sender": self.sender.email,
            "recipients": [user.first_name + " " + user.last_name for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d-%Y-%H:%M %p"),
            "read": self.read,
            "archived": self.archived,
            "starred": self.starred,
            "deleted": self.deleted,
        }


class Drive_File(models.Model):
    file = models.FileField(upload_to=MEDIA_ROOT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    starred = models.BooleanField(default=False, blank=True)
    deleted = models.BooleanField(default=False, blank=True)

    def serialize(self):
        return {
            "file": self.file,
            "timestamp": self.timestamp.strftime("%b %d-%Y-%H:%M %p"),
            "archived": self.archived,
            "starred": self.starred,
            "deleted": self.deleted,
        }


class Email_File(models.Model):
    file = models.FileField(upload_to=MEDIA_ROOT)
    email = models.ManyToManyField(Email, related_name="files")

    def serialize(self):
        return {
            "file": self.file,
        }


