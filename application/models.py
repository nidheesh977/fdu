from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta

class ImportdantDates(models.Model):
    class Meta:
        abstract=True
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True, null=True, blank=True)

class MetaDetails(models.Model):
    class Meta:
        abstract=True
    meta_title = models.CharField(_("Meta Title"), max_length=50, blank=True, null=True)
    meta_description = models.CharField(_("Meta Description"), max_length=50, blank=True, null=True)
    meta_keywords = models.TextField(_("Meta Keywords"), blank=True, null=True)


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, first_name, email, mobile_number, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(first_name, email, mobile_number, password, **other_fields)

    def create_user(self, first_name, email, mobile_number, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, mobile_number=mobile_number, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'Users'
        verbose_name = 'User'

    first_name = models.CharField(max_length=20, null=True, blank=False)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=150, null=True, blank=False)
    mobile_number = PhoneNumberField(null=True, unique=True, blank=True)
    parent_name = models.CharField(max_length=50, null=True, blank=True)

    class_name = models.CharField(max_length=50, null=True, blank=True)
    school_name = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    password = models.CharField(max_length=200, null=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    profile_pic = models.ImageField(upload_to="ProfilePictures/", blank=True, default='ProfilePictures/default_user.png')

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'mobile_number']

    def __str__(self):
        return self.email


class Blogs(MetaDetails):
    title = models.CharField(_("Title"), max_length=250, blank=False, null=True)
    description = models.TextField(_("Description"),blank=True, null=True)
    url = models.TextField(_("URL"), blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to="blog_images/",blank=True, null=True)
    image_alt_name = models.CharField(_("Image Alt Name"), max_length=50, blank=True, null=True)
    overall_description = models.TextField(_("Overall Description"),blank=True, null=True)

    class Meta:
        verbose_name = _("Blogs")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Blogs_detail", kwargs={"pk": self.pk})

class Events(models.Model):
    title = models.CharField(_("Title"), max_length=250, blank=False, null=True)
    label = models.CharField(_("Label"), max_length=250, blank=False, null=True)
    event_date = models.DateField(_("Event Date"), auto_now=False, auto_now_add=False,blank=False, null=True)
    event_meeting_link = models.URLField(_("Event Meeting Link"), max_length=200,blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to="event_images/",blank=True, null=True)
    image_alt_name = models.CharField(_("Image Alt Name"), max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _("Events")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Events_detail", kwargs={"pk": self.pk})

class RegisterdEvents(models.Model):
    student = models.ForeignKey("application.CustomUser", verbose_name=_("Student"), on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey("application.Events", verbose_name=_("Event"), on_delete=models.CASCADE, blank=True, null=True)
    registered_date = models.DateField(_("Registered Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    is_finished = models.BooleanField(_("Is Finished"), default=False)

    class Meta:
        verbose_name = _("RegisterdEvents")
        verbose_name_plural = _("RegisterdEvents")

    def get_absolute_url(self):
        return reverse("RegisterdEvents_detail", kwargs={"pk": self.pk})

class News(models.Model):
    event_date = models.DateField(_("Event Date"), auto_now=False, auto_now_add=False,blank=False, null=True)
    image = models.ImageField(_("Image"), upload_to="news_images/",blank=True, null=True)
    image_alt_name = models.CharField(_("Image Alt Name"), max_length=50, blank=True, null=True)
    description = models.TextField(_("Description"),blank=True, null=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("News_detail", kwargs={"pk": self.pk})

class Testimonials(models.Model):
    client_name = models.CharField(_("Client Name"), max_length=50, null=True, blank=True)
    client_role = models.CharField(_("Client Role"), max_length=50, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="event_images/",blank=True, null=True)
    image_alt_name = models.CharField(_("Image Alt Name"), max_length=50, blank=True, null=True)
    description = models.TextField(_("Description"),blank=True, null=True)
    # assigned_pages = 
    class Meta:
        verbose_name = _("Testimonials")
        verbose_name_plural = _("Testimonials")

  

    def get_absolute_url(self):
        return reverse("Testimonials_detail", kwargs={"pk": self.pk})

class ResultAnnouncements(models.Model):
    title = models.CharField(_("Title"), max_length=250, blank=False, null=True)
    winner_name = models.CharField(_("Winner Name"), max_length=250, blank=False, null=True)
    winner_martk= models.PositiveSmallIntegerField(_("Winner Mark"), blank=False, null=True)
    winner_image = models.ImageField(_("Image"), upload_to="winner_images/",blank=True, null=True)
    winner_image_alt_name = models.CharField(_("Winner Image Alt Name"), max_length=50, blank=True, null=True)
    winner_description = models.TextField(_("Winner Description"),blank=True, null=True)

    class Meta:
        verbose_name = _("ResultAnnouncements")
        verbose_name_plural = _("ResultAnnouncements")

   

    def get_absolute_url(self):
        return reverse("ResultAnnouncement_detail", kwargs={"pk": self.pk})

class ContactUs(ImportdantDates):
    full_name = models.CharField(_("Full Name"), max_length=28, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=254,blank=True, null=True)
    mobile_number = PhoneNumberField(null=True, unique=True, blank=True)
    message = models.TextField(_("Message"),blank=True, null=True)
    
    class Meta:
        verbose_name = _("ContactUs")
        verbose_name_plural = _("ContactUs")

    def __str__(self):
        if self.email:
            return self.email

    def get_absolute_url(self):
        return reverse("ContactUs_detail", kwargs={"pk": self.pk})

class HomeBanners(models.Model):
    title = models.CharField(_("Title"), max_length=250, blank=False, null=True)
    main_title = models.CharField(_("Main Title"), max_length=250, blank=False, null=True)
    description = models.TextField(_("Description"),blank=True, null=True)
    button_name = models.CharField(_("Button Name"), max_length=50, blank=True, null=True)
    button_url = models.URLField(_("Button Url"), max_length=200, blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to="banner_images/",blank=True, null=True)

    class Meta:
        verbose_name = _("HomeBanner")
        verbose_name_plural = _("HomeBanners")


    def get_absolute_url(self):
        return reverse("HomeBanner_detail", kwargs={"pk": self.pk})

class MarqueeTexts(models.Model):
    text = models.TextField(_("Text"),blank=True, null=True)
    

    class Meta:
        verbose_name = _("MarqueeTexts")
        verbose_name_plural = _("MarqueeTexts")

    def get_absolute_url(self):
        return reverse("MarqueeTexts_detail", kwargs={"pk": self.pk})

class Questions(models.Model):
    section = models.CharField(_("Section"), max_length=50, blank=True, null=True)
    section_description = models.CharField(_("Section Description"), max_length=50, blank=True, null=True)
    section_time_limit = models.DurationField(_("Section Duration"),default=timedelta, null=True, blank=True)
    question = models.TextField(_("Question"),null=True, blank=True)
    option1 = models.CharField(_("Option 1"), max_length=250, null=True, blank=True)
    option2 = models.CharField(_("Option 2"), max_length=250, null=True, blank=True)
    option3 = models.CharField(_("Option 3"), max_length=250, null=True, blank=True)
    option4 = models.CharField(_("Option 4"), max_length=250, null=True, blank=True)
    correct_answer = models.CharField(_("Correct Answer"), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("Questions")
        verbose_name_plural = _("Questions")


    def get_absolute_url(self):
        return reverse("Questions_detail", kwargs={"pk": self.pk})

class Papers(MetaDetails):
    title = models.CharField(_("Title"), max_length=50, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=250, blank=True, null=True)
    instructions = models.TextField(_("Instructions"), blank=True, null=True)
    assigned_questions = models.ManyToManyField("application.Questions", verbose_name=_("Questions"), blank=True,)

    class Meta:
        verbose_name = _("Papers")
        verbose_name_plural = _("Papers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Papers_detail", kwargs={"pk": self.pk})

class Subjects(MetaDetails):
    title = models.CharField(_("Title"), max_length=50, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=250, blank=True, null=True)
    assigned_papers = models.ManyToManyField("application.Papers", verbose_name=_("Papers"), blank=True,)
    

    class Meta:
        verbose_name = _("Subjects")
        verbose_name_plural = _("Subjects")

    # def __str__(self):
    #     return self.name

    def get_absolute_url(self):
        return reverse("Subjects_detail", kwargs={"pk": self.pk})


class Classes(MetaDetails):
    title = models.CharField(_("Title"), max_length=50, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=250, blank=True, null=True)
    assigned_subjects = models.ManyToManyField("application.Subjects", verbose_name=_("Subjects"), blank=True,)

    class Meta:
        verbose_name = _("Classes")
        verbose_name_plural = _("Classes")

    # def __str__(self):
    #     return self.name

    def get_absolute_url(self):
        return reverse("Classes_detail", kwargs={"pk": self.pk})