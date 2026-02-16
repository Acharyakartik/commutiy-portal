from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
User = get_user_model() 
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    member_no = models.AutoField(primary_key=True)  # Auto-increment primary key
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    occupation = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.EmailField(max_length=254, blank=True, null=True)
    profile_image = models.ImageField(upload_to="member/profile/", blank=True, null=True)
    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
    ]
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    education = models.CharField(max_length=120, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # store hashed password
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
      
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='member_created',
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='member_updated',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # If the password is not hashed yet, hash it
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.member_no} - {self.first_name} {self.surname}"
    
    
    
User1 = get_user_model()  # For created_by / updated_by references

class MemberDetail(models.Model):
    member_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    member_no = models.ForeignKey(
        'member.Member',  # Reference to your Member table
        on_delete=models.CASCADE,
        related_name='details'
    )
    
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField()
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    occupation = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.EmailField(max_length=254, blank=True, null=True)
    profile_image = models.ImageField(upload_to="member/profile/", blank=True, null=True)
    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
    ]
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    education = models.CharField(max_length=120, blank=True, null=True)
    
    # Audit fields
    created_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        related_name='memberdetail_created',
        blank=True,
        null=True
    )
    updated_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        related_name='memberdetail_updated',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)      # timestamp of last update


    def __str__(self):
        return f"Detail of {self.member_no}"
