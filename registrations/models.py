from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email

class TeamMember(models.Model):
    """Model for individual team members"""
    LEVEL_CHOICES = [
        ('bachelor', 'Bachelor'),
        ('master', 'Graduate Studies (Master)'),
        ('phd', 'Graduate Studies (PhD)'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Student Name")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Academic Level")
    order = models.IntegerField(verbose_name="Member Order", default=1)
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
    
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order']

class Registration(models.Model):
    """Model for team registrations"""
    PROJECT_FIELD_CHOICES = [
        ('health', 'Health'),
        ('energy', 'Energy'),
        ('environment', 'Environment'),
    ]
    
    PROJECT_CATEGORY_CHOICES = [
        ('student_research', 'Student Research Project'),
        ('published_research', 'Published Scientific Research'),
        ('prototype', 'Prototype'),
        ('science_communication', 'Science Translation and Simplification'),
    ]
    
    team_leader_email = models.EmailField(verbose_name="Team Leader Email", unique=True)
    project_field = models.CharField(
        max_length=20, 
        choices=PROJECT_FIELD_CHOICES, 
        verbose_name="Project Field"
    )
    project_category = models.CharField(
        max_length=30, 
        choices=PROJECT_CATEGORY_CHOICES, 
        verbose_name="Project Category"
    )
    accept_terms = models.BooleanField(default=False, verbose_name="Accept Terms")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    # Related team members
    members = models.ManyToManyField(TeamMember, related_name='registrations', verbose_name="Team Members")
    
    def __str__(self):
        return f"Team {self.team_leader_email}"
    
    def get_members_count(self):
        return self.members.count()
    
    get_members_count.short_description = "Number of Members"
    
    class Meta:
        verbose_name = "Team Registration"
        verbose_name_plural = "Team Registrations"
        ordering = ['-registration_date']
    
    @classmethod
    def export_to_csv(cls):
        """Export all registrations to CSV format"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Team Leader Email',
            'Team Leader Name',
            'Team Leader Level',
            'Number of Members',
            'All Members',
            'Project Field',
            'Project Category',
            'Registration Date'
        ])
        
        # Write data
        for registration in cls.objects.all():
            leader = registration.members.filter(order=1).first()
            all_members = ', '.join([f"{member.name} ({member.get_level_display()})" for member in registration.members.all()])
            
            writer.writerow([
                registration.team_leader_email,
                leader.name if leader else '',
                leader.get_level_display() if leader else '',
                registration.get_members_count(),
                all_members,
                registration.get_project_field_display(),
                registration.get_project_category_display(),
                registration.registration_date.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output.seek(0)
        return output.getvalue()