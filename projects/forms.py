from django import forms
from projects.models import Buy
from form_utils.forms import BetterModelForm
from form_utils.widgets import AutoResizeTextarea


class CreateBuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = [
            'name',
            'description',
            'project',
            'dollars',
            'procurement_method'
        ]


class EditBuyForm(BetterModelForm):
    class Meta:
        model = Buy
        # fields = '__all__'
        fieldsets = [
            ('General Details', {
                'fields': [
                    'name',
                    'description',
                    'dollars',
                    'project',
                    'public',
                    'procurement_method',
                    'github_repository',
                    'google_drive_folder',
                ]
                }
            ),
            ('Staffing', {
                'fields': [
                    'product_owner',
                    'product_lead',
                    'technical_lead',
                    'acquisition_lead',
                    'technical_evaluation_panel',
                ]
                }
            ),
            ('Contracting Office', {
                'fields': [
                    'contracting_office',
                    'contracting_specialist',
                    'contracting_officer',
                    'contracting_officer_representative',
                    'alternate_contracting_officer_representative',
                ]
                }
            ),
            ('Contract Pieces', {
                'fields': [
                    'contractual_history',
                    'requirements',
                    'skills_needed',
                    'base_period_length',
                    # (
                    'option_periods',
                    'option_period_length',
                    # ),
                    'naics_code',
                    'set_aside_status',
                    'competition_strategy',
                    'contract_type',
                    'security_clearance_required',
                    'rfq_id',
                ]
                }
            ),
            ('Milestone Dates', {
                'fields': [
                    'issue_date',
                    'award_date',
                    'delivery_date',
                ]
                }
            ),
            ('Award', {
                'fields': [
                    'vendor',
                    'amount_of_competition',
                ]
                }
            ),
            ('Documents', {
                'fields': [
                    'acquisition_plan',
                    'market_research',
                    'qasp',
                    'pws',
                    'rfq',
                    'interview_questions',
                ]
                }
            ),
        ]
        widgets = {
            # 'description': AutoResizeTextarea()
        }
