from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime, timedelta
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from tinymce.models import HTMLField
import uuid

User = get_user_model()


class ArmorType(models.Model):
    name = models.CharField(_('name'), max_length=200, help_text=_('Enter name of the armor'))

    def __str__(self) -> str:
        return self.name

    def link_filtered_armors(self):
        link = reverse('blacksmiths')+'?armor_type_id='+str(self.id)
        return format_html('<a class="armor_type" href="{link}">{name}</a>', link=link, name=self.name)

    class Meta:
        ordering = ['name']


class Blacksmith(models.Model):
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length =100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display_armors(self):
        return ', '.join(armor.title for armor in self.armors.all())
    display_armors.short_description = _('armors')

    def link(self) -> str:
        link = reverse('blacksmith', kwargs={'blacksmith_id':self.id})
        return format_html('<a href="{link}">{blacksmith}</a>', link=link, author=self.__str__())

    class Meta:
        ordering = ['last_name', 'first_name']


class Armor(models.Model):
    title = models.CharField(_('title'), max_length=255)
    summary = HTMLField(_('summary'))
    blacksmith = models.ForeignKey(
        Blacksmith, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='armors'
    )
    armor_type = models.ManyToManyField(
        ArmorType,
        help_text=_('Choose armors from this blacksmith'),
        verbose_name=_('armor(s)')
    )
    photo = models.ImageField(
        _('photo'), 
        upload_to='photos', 
        blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.title} {self.blacksmith}"

    def display_armor_type(self) -> str:
        return ', '.join(armor_type.name for armor_type in self.armor_type.all()[:5])
    display_armor_type.short_description = _('type')


class Buyer(models.Model):
    phone = models.CharField(_('phone'), max_length=30)
    user = models.OneToOneField(
        User, 
        verbose_name=_('user'), 
        on_delete=models.CASCADE, 
        related_name='buyer'
    )


class ArmorOrder(models.Model):
    ORDER_CHOICES =(
        ('m', _('manufacturing')),
        ('r', _('repairing')),
        ('c', _('cancelled')),
        ('t', _('taken')),
        ('a', _('assembled')),
        ('p', _('paid')),
        ('n', _('not paid')),
        ('s', _('sent')),
    )
    status = models.CharField(
        _('status'), 
        max_length=1, choices=ORDER_CHOICES, default='m'
    )
    buyer = models.ForeignKey(
        Buyer, 
        verbose_name=_('buyer'), 
        on_delete=models.CASCADE
    )
    date =models.DateField(_('order date'), auto_now_add=True)
    due_date = models.DateField(_('due_date'))
    price = models.DecimalField(
        _('price'), 
        max_digits=18, decimal_places=2, 
        default=0
    )

    def get_due_date(self):
        return self.date + timedelta(days=60)

    def save(self, *args, **kwargs):
        self.due_date = self.get_due_date()
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.due_date and self.due_date < datetime.date(datetime.now()):
            return True
        return False

    class Meta:
        ordering = ['due_date']

    def __str__(self) -> str:
        return f"{self.due_date} - {self.buyer}: {self.price}"


class OrderLine(models.Model):
    unique_id = models.UUIDField(
        _('unique ID'), 
        default=uuid.uuid4, editable=False
    )
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(
        _('price'), 
        max_digits=18, decimal_places=2, 
        default=0
    )
    order = models.ForeignKey(
        ArmorOrder, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE, related_name="order_lines"
    )
    armor = models.ForeignKey(
        Armor, 
        verbose_name=_("armor"), 
        on_delete=models.CASCADE, related_name="order_lines"
    )
    armor_type = models.ManyToManyField(ArmorType, verbose_name=_('armor type(s)'))
    buyer_wishes =HTMLField(
        _('buyer wishes'), 
        max_length=10000, blank=True, null=True, 
        help_text=_('Please, write all your wishes here')
    )

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f"{self.armor} {self.quantity} {self.price}"


class ArmorReview(models.Model):
    buyer = models.ForeignKey(
        get_user_model(), 
        verbose_name=_('buyer'), on_delete=models.CASCADE, 
        related_name='armor_reviews'
    )
    armor = models.ForeignKey(
        Armor, 
        verbose_name=_('armor'), on_delete=models.CASCADE, 
        related_name='reviews'
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    content = models.TextField(_('content'), max_length=10000)

    def __str__(self):
        return f"{self.buyer} on {self.armor} at {self.created_at}"

    class Meta:
        ordering = ('-created_at', )
