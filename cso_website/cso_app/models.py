from django.contrib.auth.hashers import make_password
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django_ckeditor_5.fields import CKEditor5Field

class FeedBackForm(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.full_name} - {self.email}'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class users(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=220, null=True, blank=True)
    username = models.CharField(max_length=220, unique=True)
    password = models.CharField(max_length=220)
    role = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=220)
    CID = models.CharField(max_length=11, null=True, blank=True)
    mobile_no = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    position_title = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(users, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name if self.full_name else self.username

class SignInDetails(models.Model):
    username = models.CharField(max_length=220, null=True, blank=True)
    password = models.CharField(max_length=220, null=True, blank=True)
    sign_in_date = models.DateTimeField(auto_now_add=True)
    sign_out_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.username

class user_roles(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_role = models.CharField(max_length=220, null=True, blank=True)
    user_role_full = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.user_role

class organizations(models.Model):
    organization_id = models.AutoField(primary_key=True)
    organization_name = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.organization_name

class system_process(models.Model):
    id = models.AutoField(primary_key=True)
    process = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.process

class gewog(models.Model):
    gewog_id = models.AutoField(primary_key=True)
    gewog_name = models.CharField(max_length=255, blank=True, null=True)
    dzongkhag = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True, default='Active')
    def __str__(self):
        return self.gewog_name

class dzongkhags(models.Model):
    dzongkhag_id = models.AutoField(primary_key=True)
    dzongkhag_name = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.dzongkhag_name
    
class cso_types(models.Model):
    cso_id = models.AutoField(primary_key=True)
    cso_type_name = models.CharField(max_length=255, blank=True, null=True)
    cso_prefix = models.CharField(max_length=255, blank=True, null=True)
    cso_status = models.CharField(max_length=255, default="Active")
    def __str__(self):
        return self.cso_name

class thematic_area(models.Model):
    cso_id = models.AutoField(primary_key=True)
    cso_name = models.CharField(max_length=255, blank=True, null=True)
    cso_status = models.CharField(max_length=255, default="Active")
    def __str__(self):
        return self.cso_name
    
class profile_attachments(models.Model):
    cso_attachment_id = models.AutoField(primary_key=True)
    cso_attachment_name = models.CharField(max_length=255, blank=True, null=True)
    cso_attachment_description = models.CharField(max_length=200, blank=True, null=True)
    cso_type = models.CharField(max_length=255, blank=True, null=True)
    public_display = models.CharField(max_length=200, blank=True, null=True)
    process = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True, default="Active")
    def __str__(self):
        return self.cso_attachment_name
    
class cso_closing_type(models.Model):
    cso_closing_id = models.AutoField(primary_key=True)
    cso_closing_type = models.CharField(max_length=255, blank=True, null=True)
    cso_closing_description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True, default="Active")
    def __str__(self):
        return self.cso_closing_type

class certificate_application(models.Model):
    application_id = models.AutoField(primary_key=True)
    application_date = models.DateTimeField(auto_now_add=True)
    uploader_cso_name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    certificate_application = models.FileField(upload_to='certificates/')  # Specify the upload directory
    def __str__(self):
        return self.uploader_cso_name

class CSO_lists(models.Model):
    cso_id = models.AutoField(primary_key=True)
    cso_name = models.CharField(max_length=200, blank=True, null=True)
    cso_acronym = models.CharField(max_length=200, blank=True, null=True)
    cso_registered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    cso_validity_date = models.DateField(blank=True, null=True)
    cso_focal = models.CharField(max_length=100, blank=True, null=True)
    cso_contact = models.CharField(max_length=100, blank=True)
    cso_email = models.EmailField(max_length=100, blank=True, null=True)
    cso_url = models.URLField(max_length=200, blank=True, null=True)  # URLField for storing URLs
    cso_link = models.CharField(max_length=200, blank=True, null=True)  # Or another appropriate field type
    cso_logo = models.ImageField(null=True, blank=True, upload_to="images/")
    cso_type = models.CharField(max_length=100, blank=True, null=True)
    thematic_area = models.CharField(max_length=100, blank=True, null=True)
    registration_no = models.CharField(max_length=50,null=True, blank=True)
    reporting_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    renewal_fee_due_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    late_renewal_fee_due_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    application_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fixed_phone_no = models.CharField(max_length=20, null=True, blank=True)
    public_email = models.EmailField(max_length=100, blank=True, null=True)
    po_box = models.CharField(max_length=100,null=True, blank=True)
    public_contact = models.CharField(max_length=20,null=True, blank=True)
    fax = models.BigIntegerField(null=True, blank=True)
    toll_free_no = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    executive_director = models.CharField(max_length=100,null=True, blank=True)
    executive_email = models.CharField(max_length=100, null=True, blank=True)
    executive_ID = models.CharField(max_length=100, null=True, blank=True)
    executive_phone = models.CharField(max_length=20,null=True, blank=True)
    cso_focal_name = models.CharField(max_length=100, null=True, blank=True)
    cso_focal_email = models.EmailField(max_length=100, null=True, blank=True)
    cso_focal_ID = models.CharField(max_length=100, null=True, blank=True)
    cso_focal_phone = models.CharField(max_length=20,null=True, blank=True)
    operation_places = models.TextField(null=True, blank=True)
    remarks = models.CharField(max_length=1000,null=True, blank=True)
    invalid_certificate_fines = models.CharField(max_length=1000, null=True, blank=True, default="0")
    purpose = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.cso_name
    
class Trustee(models.Model):
    cso_id = models.ForeignKey(CSO_lists, on_delete=models.CASCADE, related_name='trustees')
    name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200,blank=True, null=True)
    appointed_date = models.DateField(null=True)
    phone_no = models.CharField(max_length=15,blank=True, null=True)
    email = models.EmailField()
    other_trusteeship = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class cso_attachment_and_fees(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cso_id = models.IntegerField(null=True, blank=True)
    cso_type = models.CharField(max_length=200, null=True, blank=True)
    cso_name = models.CharField(max_length=200, null=True, blank=True)
    bank_type = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.EmailField(max_length=200, blank=True, null=True)
    otp = models.IntegerField(null=True, blank=True)
    journal_number = models.IntegerField(null=True, blank=True)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    amendment_type = models.CharField(max_length=200, blank=True, null=True)
    amendment_fees = models.CharField(max_length=200, blank=True, null=True)
    user_cid = models.CharField(max_length=200, blank=True, null=True)
    fees_payment_type = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)
    renewal_fees = models.CharField(max_length=100, blank=True, null=True)
    late_renewal_fees = models.CharField(max_length=100, blank=True, null=True)
    late_report_fees = models.CharField(max_length=100, blank=True, null=True)
    amount_paid = models.CharField(max_length=150, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    overall_fines = models.CharField(max_length=200, null=True, blank=True) # Add this line
    delayed_days = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    reject_reasons = models.CharField(max_length=500, blank=True, null=True)
    annual_report = models.FileField(upload_to="annual_report/", null=True, blank=True)
    audit_report = models.FileField(upload_to="audit_report/", null=True, blank=True)
    two_yrs_report = models.FileField(upload_to="two_yrs_report/", null=True, blank=True)
    annual_general_report = models.FileField(upload_to="annual_general_report/", null=True, blank=True,default='annual_general_report/bg_astronaut.jpg')
    ref_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    payment_advice_no = models.CharField(max_length=50, null=True, blank=True)
    payment_advice_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.payment_id
    
class cso_rankings(models.Model):
    cso_rankings_id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cso_id = models.ForeignKey('CSO_lists', on_delete=models.CASCADE, null=True, blank=True)
    cso_name = models.CharField(max_length=200, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.cso_rankings_id)

class financial_class(models.Model):
    financial_id = models.AutoField(primary_key=True)
    financial_class = models.CharField(max_length=200, null=True, blank=True)
    financial_description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.financial_class

class financial_group(models.Model):
    financial_group_id = models.AutoField(primary_key=True)
    financial_group_name = models.CharField(max_length=200, null=True, blank=True)
    financial_description = models.CharField(max_length=200, null=True, blank=True)
    financial_group_class = models.CharField(max_length=200, null=True, blank=True)
    financial_group_status = models.CharField(max_length=200, null=True, blank=True, default="Active")
    def __str__(self):
        return self.financial_group_name

class financial_attachments(models.Model):
    financial_attachments_id = models.AutoField(primary_key=True)
    financial_attachments_name = models.CharField(max_length=200, null=True, blank=True)
    financial_description = models.CharField(max_length=200, null=True, blank=True)
    attachment_cso_type = models.CharField(max_length=200, null=True, blank=True)
    attachment_public_display = models.CharField(max_length=200, null=True, blank=True)
    attachment_status = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.financial_attachments_name

class notifications(models.Model):
    notifications_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    notification_title = models.CharField(max_length=200, null=True, blank=True)
    notification_content = models.CharField(max_length=200, null=True, blank=True)
    notification_view = models.CharField(max_length=200, null=True, blank=True)
    notification_orgs = models.CharField(max_length=200, null=True, blank=True)
    notification_genre = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    user_role = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)
    notification_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_title

class post_publish(models.Model):
    post_id = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    post_img = models.ImageField(null=True, blank=True, upload_to="images/posts/")
    post_header = models.CharField(max_length=225, blank=True, null=True)
    activity = models.CharField(max_length=225, blank=True, null=True)
    published_date = models.DateField(auto_now_add=False, null=True, blank=True)
    post_description = CKEditor5Field(null=True, blank=True, config_name='extends')
    status = models.CharField(max_length=225, blank=True, null=True)
    featured = models.CharField(max_length=225, blank=True, null=True)
    attachments = models.CharField(max_length=225, blank=True, null=True, default='No Attachment')
    views = models.IntegerField(default=0)  # Add a views field to track post views

    def __str__(self):
        return self.post_header

class page_contents(models.Model):
    content_id = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    content_img = models.ImageField(null=True, blank=True, upload_to="images/page_content/")
    content_header = models.CharField(max_length=225, blank=True, null=True)
    content_display = models.CharField(max_length=225, blank=True, null=True)
    content_created = models.DateField(auto_now_add=True, null=True, blank=True)
    contents= CKEditor5Field(null=True, blank=True, config_name='extends')
    website_page = models.CharField(max_length=225, blank=True, null=True)
    attachments = models.CharField(max_length=225, blank=True, null=True, default='No Attachment')
    def __str__(self):
        return self.post_header