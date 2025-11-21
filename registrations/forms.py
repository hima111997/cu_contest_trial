import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Registration, TeamMember

def validate_english_only(value):
    """Validate that the value contains only English letters, numbers, and common characters"""
    if not value:
        return
    
    # Allow English letters, spaces, hyphens, apostrophes, dots, commas, and common name characters
    if not re.match(r"^[a-zA-Z\s\-\.'`,`]+$", value):
        raise ValidationError(
            'Name must contain only English letters, spaces, hyphens, apostrophes, dots, and commas. '
            'Please enter your name in English.',
            code='english_only'
        )

def validate_english_email(value):
    """Validate that email is properly formatted for English usage"""
    if not value:
        return
    
    # Basic email validation with English requirement
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError(
            'Please enter a valid email address using English characters.',
            code='english_email'
        )

class RegistrationForm(forms.ModelForm):
    """Form for team registration with static 5-member structure"""
    LEVEL_CHOICES = [
        ('', 'Academic Level'),
        ('bachelor', 'Bachelor'),
        ('master', 'Graduate Studies (Master)'),
        ('phd', 'Graduate Studies (PhD)'),
    ]
    
    PROJECT_FIELD_CHOICES = [
        ('', 'Choose Project Field'),
        ('health', 'Health'),
        ('energy', 'Energy'),
        ('environment', 'Environment'),
    ]
    
    PROJECT_CATEGORY_CHOICES = [
        ('', 'Choose Project Category'),
        ('student_research', 'Student Research Project'),
        ('published_research', 'Published Scientific Research'),
        ('prototype', 'Prototype'),
        ('science_communication', 'Science Translation and Simplification'),
    ]
    
    # Team leader info
    team_leader_email = forms.EmailField(
        label='Team Leader Email (Enter in English)',
        validators=[validate_english_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email address in English',
            'required': True,
            'title': 'Please enter your email address using English characters only'
        })
    )
    
    # Static 5-member structure
    member1_name = forms.CharField(
        label='Member One (Team Leader) Name',
        validators=[validate_english_only],
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your full name in English (e.g., John Smith)',
            'required': True,
            'title': 'Please enter your full name using English letters only'
        })
    )
    
    member1_level = forms.ChoiceField(
        label='Member One Academic Level',
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    member2_name = forms.CharField(
        label='Member Two Name',
        validators=[validate_english_only],
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter full name in English (e.g., Jane Doe)',
            'required': True,
            'title': 'Please enter full name using English letters only'
        })
    )
    
    member2_level = forms.ChoiceField(
        label='Member Two Academic Level',
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    # Optional members (3, 4, 5)
    member3_name = forms.CharField(
        label='Member Three Name (Optional)',
        validators=[validate_english_only],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter full name in English (optional)',
            'title': 'Please enter full name using English letters only'
        })
    )
    
    member3_level = forms.ChoiceField(
        label='Member Three Academic Level',
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    member4_name = forms.CharField(
        label='Member Four Name (Optional)',
        validators=[validate_english_only],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter full name in English (optional)',
            'title': 'Please enter full name using English letters only'
        })
    )
    
    member4_level = forms.ChoiceField(
        label='Member Four Academic Level',
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    member5_name = forms.CharField(
        label='Member Five Name (Optional)',
        validators=[validate_english_only],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter full name in English (optional)',
            'title': 'Please enter full name using English letters only'
        })
    )
    
    member5_level = forms.ChoiceField(
        label='Member Five Academic Level',
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    project_field = forms.ChoiceField(
        label='Project Field',
        choices=PROJECT_FIELD_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'radio-card'
        })
    )
    
    project_category = forms.ChoiceField(
        label='Project Category',
        choices=PROJECT_CATEGORY_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'radio-card'
        })
    )
    
    accept_terms = forms.BooleanField(
        label='I agree to the competition rules and all related terms and conditions',
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-container',
            'required': True
        })
    )
    
    class Meta:
        model = Registration
        fields = ['team_leader_email', 'project_field', 'project_category', 'accept_terms']
        widgets = {
            'team_leader_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'project_field': forms.RadioSelect(attrs={'class': 'radio-card'}),
            'project_category': forms.RadioSelect(attrs={'class': 'radio-card'}),
            'accept_terms': forms.CheckboxInput(attrs={'class': 'checkbox-container'}),
        }
    
    def clean_team_leader_email(self):
        """Validate that email is unique and in English"""
        email = self.cleaned_data['team_leader_email']
        
        # Check uniqueness
        if Registration.objects.filter(team_leader_email=email).exists():
            raise forms.ValidationError('This email is already registered in the system')
        
        return email
    
    def clean_member1_name(self):
        """Validate first member name is in English"""
        name = self.cleaned_data.get('member1_name')
        if name:
            validate_english_only(name)
        return name
    
    def clean_member2_name(self):
        """Validate second member name is in English"""
        name = self.cleaned_data.get('member2_name')
        if name:
            validate_english_only(name)
        return name
    
    def clean_member3_name(self):
        """Validate third member name is in English"""
        name = self.cleaned_data.get('member3_name')
        if name:
            validate_english_only(name)
        return name
    
    def clean_member4_name(self):
        """Validate fourth member name is in English"""
        name = self.cleaned_data.get('member4_name')
        if name:
            validate_english_only(name)
        return name
    
    def clean_member5_name(self):
        """Validate fifth member name is in English"""
        name = self.cleaned_data.get('member5_name')
        if name:
            validate_english_only(name)
        return name
    
    def clean_accept_terms(self):
        """Ensure terms are accepted"""
        accept_terms = self.cleaned_data['accept_terms']
        if not accept_terms:
            raise forms.ValidationError('You must agree to the competition rules')
        return accept_terms
    
    def clean(self):
        """Custom validation for the form"""
        cleaned_data = super().clean()
        
        # Count total members with names
        total_members = 0
        members_with_data = []
        
        # Check required members
        member1_name = cleaned_data.get('member1_name', '').strip()
        member2_name = cleaned_data.get('member2_name', '').strip()
        
        if not member1_name:
            self.add_error('member1_name', 'Member One name is required')
        else:
            total_members += 1
            members_with_data.append({
                'name': member1_name,
                'level': cleaned_data.get('member1_level'),
                'order': 1
            })
        
        if not member2_name:
            self.add_error('member2_name', 'Member Two name is required')
        else:
            total_members += 1
            members_with_data.append({
                'name': member2_name,
                'level': cleaned_data.get('member2_level'),
                'order': 2
            })
        
        # Check optional members
        for i in range(3, 6):
            member_name = cleaned_data.get(f'member{i}_name', '').strip()
            member_level = cleaned_data.get(f'member{i}_level')
            
            if member_name:
                total_members += 1
                if not member_level:
                    self.add_error(f'member{i}_level', 
                        f'Member {i} academic level is required when name is entered')
                else:
                    members_with_data.append({
                        'name': member_name,
                        'level': member_level,
                        'order': i
                    })
        
        # Validate team size
        if total_members < 2:
            self.add_error(None, 'At least 2 team members are required')
        elif total_members > 5:
            self.add_error(None, 'Maximum 5 team members allowed')
        
        return cleaned_data