from __future__ import unicode_literals

from datetime import date, timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.template.loader import render_to_string


# Create your models here.
class Agency(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        pass


class AgencyOffice(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    agency = models.ForeignKey(
        Agency,
        blank=False,
        null=False,
    )

    def __str__(self):
        return "{0} - {1}".format(self.agency.name, self.name)

    class Meta:
        unique_together = ('name', 'agency')


class IAA(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        blank=False,
        null=False,
    )
    client = models.ForeignKey(
        AgencyOffice,
        blank=False,
        null=False,
    )
    signed_on = models.DateField(
        blank=True,
        null=True,
    )
    expires_on = models.DateField(
        blank=True,
        null=True,
    )
    dollars = models.IntegerField(
        blank=True,
        null=True,
    )
    color_of_money = models.CharField(
        choices=(
            ('No-Year Money', 'No-Year Money'),
            ('1-Year Money', '1-Year Money'),
            ('2-Year Money', '2-Year Money'),
        ),
        max_length=100,
        blank=True,
        null=True,
    ),
    authority = models.CharField(
        choices=(
            ('ASF', 'Alternating Services Fund'),
            ('Economy', 'Economy Act'),
        ),
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{0} | {1}".format(self.client, self.id)

    def is_signed(self):
        return self.signed_on != null

    def clean(self):
        if self.signed_on > date.today():
            raise ValidationError({
                'signed_on': 'Date may not be in the future.'
            })

    class Meta:
        verbose_name = 'IAA'


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    iaa = models.ForeignKey(
        IAA,
        on_delete=models.SET_NULL,
        blank=False,
        # TODO: should null=False?
        null=True,
    )
    project_type = models.CharField(
        choices=(
            ('Internal Buy', 'Internal Buy'),
            ('External Buy', 'External Buy'),
            ('Consulting', 'Consulting'),
        ),
        max_length=100,
        blank=False,
        null=False,
    )
    dollars = models.IntegerField(
        blank=True,
        null=True,
    )
    public = models.BooleanField(
        default=False,
    )
    # TODO: should active status be determined by IAA status?
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return "/projects/{0}/".format(self.id)

    def is_private(self):
        return not self.public

    def clean(self):
        if self.dollars:
            if self.dollars > self.iaa.dollars:
                raise ValidationError({
                    'dollars': 'Value can\'t exceed value of authorizing IAA'
                })

    class Meta:
        permissions = (
            ('view_private', 'Can view non-public projects'),
        )


class ContractingOffice(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    program_manager = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        pass


class ContractingSpecialist(models.Model):
    user = models.OneToOneField(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        ContractingOffice,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{0} - {1}".format(self.user.get_full_name(), self.office.name)

    def name(self):
        return self.user.get_full_name()

    class Meta:
        pass


class ContractingOfficer(models.Model):
    user = models.OneToOneField(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        ContractingOffice,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{0} - {1}".format(self.user.get_full_name(), self.office.name)

    def name(self):
        return self.user.get_full_name()

    class Meta:
        pass


class ContractingOfficerRepresentative(models.Model):
    user = models.OneToOneField(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        ContractingOffice,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{0} - {1}".format(self.user.get_full_name(), self.office.name)

    def name(self):
        return self.user.get_full_name()

    class Meta:
        pass


class Buy(models.Model):
    PROCUREMENT_METHOD_CHOICES = (
        ('Agile BPA', 'Agile BPA'),
        ('Micro-Purchase', 'Micro-Purchase'),
    )
    SET_ASIDE_CHOICES = (
        ("AbilityOne", "AbilityOne"),
        ("HUBZone Small Business", "HUBZone Small Business"),
        ("Multiple Small Business Categories",
            "Multiple Small Business Categories"),
        ("Other Than Small", "Other Than Small"),
        ("Service Disabled Veteran-owned Small Business",
            "Service Disabled Veteran-owned Small Business"),
        ("Small Business", "Small Business"),
        ("Small Disadvantaged Business (includes Section 8a)",
            "Small Disadvantaged Business (includes Section 8a)"),
        ("Veteran-Owned Small Business", "Veteran-Owned Small Business"),
        ("Woman-Owned Small Business", "Woman-Owned Small Business"),
    )

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    contractual_history = models.TextField(
        blank=False,
        null=False,
        default="This is the first contract for this functionality.",
    )
    project = models.ForeignKey(
        Project,
        related_name='buys',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    dollars = models.PositiveIntegerField(
        blank=False,
        null=True
    )
    public = models.BooleanField(
        default=False,
    )
    base_period_length = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    option_periods = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=0,
    )
    option_period_length = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    procurement_method = models.CharField(
        max_length=200,
        choices=PROCUREMENT_METHOD_CHOICES,
        blank=True,
        null=True,
    )
    set_aside_status = models.CharField(
        max_length=200,
        choices=SET_ASIDE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Set-aside Status'
    )
    rfq_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name='RFQ ID'
    )
    contracting_office = models.ForeignKey(
        ContractingOffice,
        blank=True,
        null=True,
    )
    contracting_specialist = models.ForeignKey(
        ContractingSpecialist,
        blank=True,
        null=True,
    )
    contracting_officer = models.ForeignKey(
        ContractingOfficer,
        blank=True,
        null=True,
    )
    contracting_officer_representative = models.ForeignKey(
        ContractingOfficerRepresentative,
        blank=True,
        null=True,
    )
    github_repository = models.URLField(
        blank=True,
        null=True,
    )

    # Documents for the buy
    # TODO: Consider using a MarkdownField() of some sort for in-app editing
    qasp = models.TextField(
        blank=True,
        null=True,
        verbose_name='QASP',
    )
    acquisition_plan = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return "/buys/{0}/".format(self.id)

    def is_private(self):
        return not self.public

    def _get_time_from_string(self, length):
        try:
            amount, units = length.split(' ')
            amount = int(amount)
            if units == 'days':
                duration = timedelta(days=amount)
            elif units == 'weeks':
                duration = timedelta(weeks=amount)
            else:
                raise ValueError('Couldn\'t parse input length')
            return duration
        except Exception:
            return None

    def period_of_performance(self):
        # TODO: Come back and see if this makes sense
        # The goal of this is to turn our string-based period of performance
        # into something that can be manipulated and displayed in different
        # ways. But for now, the strings are what's needed for templating
        # and such.
        try:
            base = self._get_time_from_string(self.base_period_length)
            option = self._get_time_from_string(self.option_period_length)
            return base + (self.option_periods * option)
        except Exception:
            return None

    def create_qasp(self):
        # TODO: This may need mark_safe from django.utils.safestring
        self.qasp = render_to_string(
                'projects/markdown/qasp.md',
                {'buy': self}
            )
        self.save(update_fields=['qasp'])

    def create_acquisition_plan(self):
        # TODO: This may need mark_safe from django.utils.safestring
        self.acquisition_plan = render_to_string(
                'projects/markdown/acquisition_plan.md',
                {'buy': self}
            )
        self.save(update_fields=['acquisition_plan'])
        print('acq plan updated')

    def acquistition_plan_status(self):
        # TODO: This could return the status of the acquisitions plan based on
        # the fields that have been completed.
        # Additionally, the acquisition plan page can display the remaining
        # unset fields at the top of the acquisition plan page
        if not self.acquisition_plan:
            return 'Not yet generated'
        else:
            # TODO: Finish the acquisition plan template so that we can add
            # a 'Complete' setting
            return 'Incomplete'

    def qasp_status(self):
        if self.name and not self.qasp:
            return 'Not yet generated'
        elif self.name and self.qasp:
            return 'Complete'
        else:
            return 'Incomplete'

    def clean(self):
        # Check that buy is not public without associated project being public
        if (self.project.public is not True) and (self.public is True):
            raise ValidationError({
                'public': 'May not be public if the associated project is not.'
            })

        # Confirm option period existence if option period length is set
        if (self.option_period_length) and (self.option_periods == 0):
            raise ValidationError({
                'option_period_length': 'The number of option periods must be '
                'greater than 0 to set a length'
            })

        # Confirm that buy cost doesn't exceed project value
        if self.dollars:
            if self.dollars > self.project.dollars:
                raise ValidationError({
                    'dollars': 'Value can\'t exceed value of overall project'
                })

    class Meta:
        pass
