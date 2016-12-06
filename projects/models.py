from __future__ import unicode_literals

from datetime import date, timedelta
from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
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
        verbose_name = 'Agencies'


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
    team_members = models.ManyToManyField(
        User,
        help_text='You may select from users who have signed the blanket NDA.',
        blank=False,
        limit_choices_to=models.Q(groups__name='NDA Signed'),
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
    # TODO: should active status be determined by IAA status? Probably not
    # directly, but it would make sense to check that projects don't outlast
    # the underlying IAA
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse('projects:project', args=[self.id])

    def is_private(self):
        return not self.public

    def budget_remaining(self):
        budget = self.dollars
        for buy in self.buys.all():
            budget -= buy.dollars
        return budget

    def clean(self):
        if self.dollars:
            if self.dollars > self.iaa.dollars:
                raise ValidationError({
                    'dollars': 'Value can\'t exceed value of authorizing IAA'
                })

    class Meta:
        permissions = (
            ('view_project', 'Can view non-public projects'),
            ('sign_nda', 'Can sign an NDA, either blanket or specific')
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

    technical_evaluation_panel = models.ManyToManyField(
        User,
        blank=True,
        related_name='panels',
    )
    nda_signed = models.ManyToManyField(
        User,
        blank=True,
        related_name='ndas',
    )

    # Locking doesn't do anything on its own, but should be used as an
    # indicator of when the user shouldn't be able to edit the data. Initially,
    # this was tied to award_date, but using a separate field should allow the
    # entry to be unlocked for editing if necessary.
    locked = models.BooleanField(
        default=False
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
    market_research = models.TextField(
        blank=True,
        null=True,
    )

    # Milestone dates
    issue_date = models.DateField(
        blank=True,
        null=True,
    )
    award_date = models.DateField(
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

    # TODO: this document generation seems to involve repeated logic
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
                {'buy': self, 'date': date.today()}
            )
        self.save(update_fields=['acquisition_plan'])

    def acquisition_plan_status(self):
        # TODO: find a way to display the incomplete fields on the page
        required_fields = [
            self.name,
            self.description,
            self.contractual_history,
            self.project,
            self.contracting_office,
            self.contracting_officer,
            self.contracting_specialist,
            self.base_period_length,
            self.option_periods,
            self.option_period_length,
            self.dollars,
            self.rfq_id,
            self.procurement_method,
            self.set_aside_status,
        ]
        if not self.acquisition_plan:
            return 'Not yet generated'
        else:
            incomplete_fields = []
            for field in required_fields:
                if field is None:
                    incomplete_fields.append(field)
            percentage = (len(incomplete_fields) / len(required_fields)) * 100
            return '{0:.2f}% Complete'.format(percentage)

    def qasp_status(self):
        if self.name and not self.qasp:
            return 'Not yet generated'
        elif self.name and self.qasp:
            return 'Complete'
        else:
            return 'Incomplete'

    def create_market_research(self):
        # TODO: This may need mark_safe from django.utils.safestring
        self.market_research = render_to_string(
            'projects/markdown/market_research.md',
            {'buy': self}
        )
        self.save(update_fields=['market_research'])

    def all_nda_signed(self):
        panelists = self.technical_evaluation_panel.all()
        signers = self.nda_signed.all()
        unsigned = [i for i in panelists if i not in signers]
        # TODO: Could also return the names of those who need to sign
        if len(unsigned) > 0:
            return False
        else:
            return True

    def required_fields(self):
        required_fields = [
            self.name,
            self.description,
            self.contractual_history,
            self.project,
            self.contracting_office,
            self.contracting_officer,
            self.contracting_specialist,
            self.contracting_officer_representative,
            self.base_period_length,
            self.option_periods,
            self.option_period_length,
            self.acquisition_plan,
            self.qasp,
            self.dollars,
            self.public,
            self.rfq_id,
            self.procurement_method,
            self.set_aside_status,
            self.github_repository,
        ]
        return required_fields

    def ready_to_issue(self):
        if None in self.required_fields() or not self.all_nda_signed():
            return False
        else:
            return True

    def locked_fields(self):
        if self.locked:
            fields = [
                'project',
                'public',
                'qasp',
                'acquisition_plan',
                'contractual_history',
                'rfq_id',
                'contracting_office',
                'contracting_officer',
                'contracting_specialist',
                'contracting_officer_representative',
                'set_aside_status',
                'procurement_method',
                'base_period_length',
                'option_periods',
                'option_period_length',
                'dollars'
            ]
        else:
            fields = []
        return fields

    def market_research_status(self):
        if self.name and not self.market_research:
            return 'Not yet generated'
        elif self.name and self.market_research:
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

        # Don't allow issue date without a lot of other stuff
        if self.issue_date and not self.ready_to_issue():
            raise ValidationError({
                'issue_date': 'This buy is not yet ready to be issued'
            })

        # Don't allow award date without issue date
        if self.award_date and not self.issue_date:
            raise ValidationError({
                'award_date': 'Please set an issue date first'
            })

    class Meta:
        pass
