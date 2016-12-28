from __future__ import unicode_literals

from datetime import date, timedelta
from django.db import models
from django.contrib.postgres.fields import ArrayField
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
        verbose_name_plural = 'Agencies'
        ordering = ['name']


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
        ordering = ['agency', 'name']


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
        return self.signed_on is not None

    def budget_remaining(self):
        budget = self.dollars
        for project in self.project_set.all():
            budget -= project.dollars
        return budget

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
        for buy in self.agilebpa.all():
            budget -= buy.dollars
        for buy in self.micropurchase.all():
            budget -= buy.dollars
        return budget

    def clean(self):
        if self.dollars:
            if self.dollars > self.iaa.budget_remaining():
                raise ValidationError({
                    'dollars': 'Value can\'t exceed remaining budget of'
                               'authorizing IAA'
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


class ContractingPersonnel(models.Model):
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
        abstract = True


class ContractingSpecialist(ContractingPersonnel):
    pass


class ContractingOfficer(ContractingPersonnel):
    pass


class ContractingOfficerRepresentative(ContractingPersonnel):
    pass


class AlternateContractingOfficerRepresentative(ContractingPersonnel):
    pass


class Vendor(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    class Meta:
        pass


COMPETITION_STRATEGY_CHOICES = (
    ("A/E Procedures", "A/E Procedures"),
    ("Competed under SAP", "Competed under SAP"),
    ("Competitive Delivery Order Fair Opportunity Provided",
        "Competitive Delivery Order Fair Opportunity Provided"),
    ("Competitive Schedule Buy", "Competitive Schedule Buy"),
    ("Fair Opportunity", "Fair Opportunity"),
    ("Follow On to Competed Action (FAR 6.302-1)",
        "Follow On to Competed Action (FAR 6.302-1)"),
    ("Follow On to Competed Action", "Follow On to Competed Action"),
    ("Full and Open after exclusion of sources (competitive small business \
        set-asides, competitive 8a)",
        "Full and Open after exclusion of sources (competitive small \
        business set-asides, competitive 8a)"),
    ("Full and Open Competition Unrestricted",
        "Full and Open Competition Unrestricted"),
    ("Full and Open Competition", "Full and Open Competition"),
    ("Limited Sources FSS Order", "Limited Sources FSS Order"),
    ("Limited Sources", "Limited Sources"),
    ("Non-Competitive Delivery Order", "Non-Competitive Delivery Order"),
    ("Not Available for Competition (e.g., 8a sole source, HUBZone & \
        SDVOSB sole source, Ability One, all > SAT)",
        "Not Available for Competition (e.g., 8a sole source, HUBZone & \
        SDVOSB sole source, Ability One, all > SAT)"),
    ("Not Competed (e.g., sole source, urgency, etc., all > SAT)",
        "Not Competed (e.g., sole source, urgency, etc., all > SAT)"),
    ("Not Competed under SAP (e.g., Urgent, Sole source, Logical \
        Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)",
        "Not Competed under SAP (e.g., Urgent, Sole source, Logical \
        Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)"),
    ("Partial Small Business Set-Aside",
        "Partial Small Business Set-Aside"),
    ("Set-Aside", "Set-Aside"),
    ("Sole Source", "Sole Source"),
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

CONTRACT_TYPE_CHOICES = (
    ("Labor Hours", "Labor Hours"),
    ("Time and Materials", "Time and Materials"),
)


class Buy(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    project = models.ForeignKey(
        Project,
        related_name='%(class)s',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    dollars = models.PositiveIntegerField(
        blank=False,
        null=True,
    )
    requirements = ArrayField(
        # https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#arrayfield
        models.CharField(max_length=200, blank=True, null=True),
        default=list,
        blank=True,
        null=True,
    )
    skills_needed = ArrayField(
        # https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#arrayfield
        models.CharField(max_length=200, blank=True, null=True),
        default=list,
        blank=True,
        null=True,
    )
    product_owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
    )
    public = models.BooleanField(
        default=False,
    )
    amount_of_competition = models.IntegerField(
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
    delivery_date = models.DateField(
        blank=True,
        null=True,
    )
    vendor = models.ForeignKey(
        Vendor,
        blank=True,
        null=True,
    )

    def status(self):
        if self.delivery_date:
            status = "Delivered"
        elif self.award_date:
            status = "Awarded"
        elif self.issue_date:
            status = "Out for Bid"
        else:
            status = "Planning"
        return status

    def clean_dollars(self):
        # Confirm that buy cost doesn't exceed project value
        dollars = self.cleaned_data['dollars']
        project = self.cleaned_data['project']
        if dollars > project.budget_remaining():
            raise ValidationError({
                'dollars': 'Value can\'t exceed project\'s remaining budget.'
            })
        return dollars

    def clean_public(self):
        # Check that buy is not public without associated project being public
        public = cleaned_data['public']
        project = cleaned_data['project']
        if (project.public is not True) and (public is True):
            raise ValidationError({
                'public': 'May not be public if the associated project is not.'
            })
        return public

    def clean_delivery_date(self):
        # Check that delivery doesn't occur before award
        delivery_date = cleaned_data['delivery_date']
        award_date = cleaned_data['award_date']
        vendor = cleaned_data['vendor']
        if delivery_date and not award_date or not vendor:
            raise ValidationError({
                'delivery_date': 'An award date and vendor are required to '
                                 'add the delivery date.'
            })

    class Meta:
        abstract = True


class AgileBPA(Buy):
    contractual_history = models.TextField(
        blank=False,
        null=False,
        default="This is the first contract for this functionality.",
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
    naics_code = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="NAICS Code"
    )
    procurement_method = models.CharField(
        max_length=200,
        default="Agile Development Services BPA Order",
        editable=False,
        blank=False,
        null=False,
    )
    set_aside_status = models.CharField(
        max_length=200,
        choices=SET_ASIDE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Set-aside Status'
    )
    competition_strategy = models.CharField(
        max_length=200,
        choices=COMPETITION_STRATEGY_CHOICES,
        blank=True,
        null=True,
    )
    contract_type = models.CharField(
        max_length=200,
        choices=CONTRACT_TYPE_CHOICES,
        blank=True,
        null=True,
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
    alternate_contracting_officer_representative = models.ForeignKey(
        AlternateContractingOfficerRepresentative,
        blank=True,
        null=True,
    )
    github_repository = models.URLField(
        blank=True,
        null=True,
    )
    google_drive_folder = models.URLField(
        blank=True,
        null=True,
    )
    security_clearance_required = models.BooleanField(
        default=False,
    )

    product_lead = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='product_lead',
    )
    acquisition_lead = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='acquisition_lead',
    )
    technical_lead = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='technical_lead',
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
        # TODO: Find a way to display more than just days
        try:
            base = self._get_time_from_string(self.base_period_length)
            option = self._get_time_from_string(self.option_period_length)
            total = base + (self.option_periods * option)
            return "{0} days".format(str(total.days))
        except Exception:
            return None

    def create_document(self, doc_type):
        available_docs = {
            'qasp': self.qasp,
            'acquisition_plan': self.acquisition_plan,
            'market_research': self.market_research,
        }
        doc_content = render_to_string(
            'acq_templates/{0}/{1}.md'.format("agile_bpa", doc_type),
            {'buy': self, 'date': date.today()}
        )
        setattr(self, doc_type, doc_content)
        self.save(update_fields=[doc_type])

    def acquisition_plan_status(self):
        # TODO: find a way to display the incomplete fields on the page
        required_fields = [
            self.base_period_length,
            self.contracting_office,
            self.contracting_officer,
            self.contracting_specialist,
            self.contractual_history,
            self.description,
            self.dollars,
            self.name,
            self.option_period_length,
            self.option_periods,
            self.procurement_method,
            self.project,
            self.rfq_id,
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
        return 'Not yet generated' if self.qasp is None else 'Complete'

    def market_research_status(self):
        return 'Not yet generated' if self.market_research is None else 'Complete'

    def tasks(self):
        # A version of responsibilities for use in a logicless template
        bulleted = ['- {0}'.format(req) for req in self.requirements]
        return '\n'.join(bulleted)

    def skills(self):
        # A version of responsibilities for use in a logicless template
        bulleted = ['- {0}'.format(req) for req in self.skills_needed]
        return '\n'.join(bulleted)

    def needs_clearance(self):
        # Security clearance requirement for use in a logicless template
        if self.security_clearance_required:
            return "- Secret Clearance (for at least the Technical Lead)"
        else:
            return None

    def all_nda_signed(self):
        panelists = self.technical_evaluation_panel.all()
        signers = self.nda_signed.all()
        unsigned = [i for i in panelists if i not in signers]
        # TODO: Could also return the names of those who need to sign
        if len(unsigned) > 0:
            return False
        else:
            return True

    def ready_to_issue(self):
        required_fields = [
            self.acquisition_plan,
            self.base_period_length,
            self.competition_strategy,
            self.contract_type,
            self.contracting_office,
            self.contracting_officer_representative,
            self.contracting_officer,
            self.contracting_specialist,
            self.contractual_history,
            self.description,
            self.dollars,
            self.naics_code,
            self.name,
            self.option_period_length,
            self.option_periods,
            self.procurement_method,
            self.product_owner,
            self.project,
            self.public,
            self.qasp,
            self.rfq_id,
            self.set_aside_status,
        ]
        if None in required_fields or not self.all_nda_signed():
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

    def clean(self):
        # Confirm option period existence if option period length is set
        if (self.option_period_length) and (self.option_periods == 0):
            raise ValidationError({
                'option_period_length': 'The number of option periods must be '
                'greater than 0 to set a length'
            })

        # Don't allow issue date without a lot of other stuff
        if self.issue_date and not self.ready_to_issue():
            raise ValidationError({
                'issue_date': 'This buy is not yet ready to be issued'
            })

        # No vendors before issuing, at least
        if self.vendor and not self.issue_date:
            raise ValidationError({
                'vendor': 'There shouldn\'t be a vendor before issuing'
            })

        # Don't allow award date without issue date
        if self.award_date and not self.issue_date:
            raise ValidationError({
                'award_date': 'Please set an issue date first'
            })

        # Check NAICS Code
        if self.naics_code:
            if len(str(self.naics_code)) != 6:
                raise ValidationError({
                    'naics_code': 'NAICS Code must be six digits'
                })

    class Meta:
        verbose_name = 'Agile BPA Order'


class Micropurchase(Buy):
    procurement_method = models.CharField(
        max_length=200,
        default="Micro-purchase",
        editable=False,
        blank=False,
        null=False,
    )

    def clean(self):
        # Confirm that buy isn't over micro-purchase threshold
        if self.dollars > 3500:
            raise ValidationError({
                'dollars': 'Value can\'t exceed the micro-purchase '
                           'threshold of $3500'
            })

        # Don't allow award date without issue date
        if self.award_date and not self.issue_date:
            raise ValidationError({
                'award_date': 'Please set an issue date first'
            })

    class Meta:
        verbose_name = 'Micro-purchase'


class OpenMarket(Buy):
    pass


class Software(Buy):
    pass
