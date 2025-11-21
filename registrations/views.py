from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib import messages

from .models import Registration, TeamMember
from .forms import RegistrationForm

def index(request):
    """Main registration page"""
    if request.method == 'POST':
        return handle_registration_submission(request)
    
    form = RegistrationForm()
    return render(request, 'registrations/index.html', {'form': form})

def migrate_database(request):
    """Emergency migration endpoint - remove after setup"""
    if request.method == 'POST':
        try:
            from django.core.management import call_command
            call_command('migrate', '--run-syncdb', verbosity=0)
            return JsonResponse({'status': 'success', 'message': 'Database migrated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'info', 'message': 'POST to this endpoint to run migrations'})

def handle_registration_submission(request):
    """Handle form submission - simplified version"""
    print(f"🔍 Form received: {dict(request.POST)}")
    
    # Manual form validation
    errors = []
    
    # Validate email field
    email = request.POST.get('team_leader_email', '').strip()
    if not email:
        errors.append('Email address is required')
    elif '@' not in email:
        errors.append('Please enter a valid email address')
    elif Registration.objects.filter(team_leader_email=email).exists():
        errors.append('This email is already registered in the system')
    
    # Validate required members (1 & 2)
    if not request.POST.get('member1_name'):
        errors.append('Member 1 name is required')
    if not request.POST.get('member1_level'):
        errors.append('Member 1 academic level is required')
    if not request.POST.get('member2_name'):
        errors.append('Member 2 name is required')
    if not request.POST.get('member2_level'):
        errors.append('Member 2 academic level is required')
    
    # Validate project selections
    if not request.POST.get('project_field'):
        errors.append('Project field is required')
    if not request.POST.get('project_category'):
        errors.append('Project category is required')
    if not request.POST.get('accept_terms'):
        errors.append('You must accept the competition rules')
    
    # Validate English characters in names
    import re
    english_pattern = r"^[a-zA-Z\s\-\.'`,`]+$"
    
    for i in range(1, 6):  # Check all 5 members
        name = request.POST.get(f'member{i}_name', '').strip()
        if name:
            if not re.match(english_pattern, name):
                errors.append(f'Member {i} name must contain only English letters')
    
    # If there are errors, show them
    if errors:
        print(f"❌ Validation errors: {errors}")
        error_message = '<br>'.join(errors)
        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #d32f2f;">Registration Failed</h2>
            <div style="background: #ffebee; border: 1px solid #f8bbd9; padding: 20px; border-radius: 8px; margin: 20px;">
                <h3>Please fix the following errors:</h3>
                <ul style="text-align: left; display: inline-block;">
                    {''.join([f'<li>{error}</li>' for error in errors])}
                </ul>
            </div>
            <button onclick="window.history.back()" style="background: #2196F3; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Go Back</button>
        </body>
        </html>
        """, content_type='text/html')
    
    # If validation passes, save to database
    try:
        with transaction.atomic():
            # Create registration record
            registration = Registration.objects.create(
                team_leader_email=email,
                project_field=request.POST.get('project_field'),
                project_category=request.POST.get('project_category'),
                accept_terms=True
            )
            
            print(f"✅ Registration created with ID: {registration.id}")
            
            # Create team members
            members_created = 0
            for i in range(1, 6):
                name = request.POST.get(f'member{i}_name', '').strip()
                level = request.POST.get(f'member{i}_level')
                
                if name and level:
                    member = TeamMember.objects.create(
                        name=name,
                        level=level,
                        order=i
                    )
                    registration.members.add(member)
                    members_created += 1
                    print(f"✅ Member {i} created: {name} ({level})")
            
            print(f"✅ Total members created: {members_created}")
            
            # Return success page
            return HttpResponse(f"""
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <div style="background: #e8f5e8; border: 1px solid #4caf50; padding: 30px; border-radius: 10px;">
                    <h1 style="color: #2e7d32;">✅ Registration Successful!</h1>
                    <p style="font-size: 18px; margin: 20px 0;">Your team has been successfully registered.</p>
                    <p><strong>Registration ID:</strong> {registration.id}</p>
                    <p><strong>Team Leader Email:</strong> {email}</p>
                    <p><strong>Total Members:</strong> {members_created}</p>
                    <p><strong>Project Field:</strong> {request.POST.get('project_field')}</p>
                    <p><strong>Project Category:</strong> {request.POST.get('project_category')}</p>
                    <button onclick="window.location.href='/'" style="background: #2196F3; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 20px;">Register Another Team</button>
                </div>
            </body>
            </html>
            """, content_type='text/html')
            
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #d32f2f;">Registration Failed</h2>
            <p>Database error: {str(e)}</p>
            <button onclick="window.history.back()" style="background: #2196F3; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Go Back</button>
        </body>
        </html>
        """, content_type='text/html')

def registration_success(request):
    """Success page after registration"""
    return render(request, 'registrations/success.html')

@csrf_exempt
@require_http_methods(["POST"])
def validate_email(request):
    """AJAX endpoint to validate email uniqueness"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'valid': False, 'error': 'Email is required'})
        
        exists = Registration.objects.filter(team_leader_email=email).exists()
        
        return JsonResponse({
            'valid': not exists,
            'exists': exists,
            'error': 'This email is already registered in the system' if exists else None
        })
    except json.JSONDecodeError:
        return JsonResponse({'valid': False, 'error': 'Invalid request'}, status=400)

def export_csv(request):
    """Export all registrations to CSV"""
    try:
        registrations = Registration.objects.all().prefetch_related('members')
        
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Registration ID', 'Team Leader Email', 'Project Field', 'Project Category', 'Registration Date', 'Total Members', 'Member Names', 'Member Levels'])
        
        for reg in registrations:
            member_names = ', '.join([member.name for member in reg.members.all().order_by('order')])
            member_levels = ', '.join([member.level for member in reg.members.all().order_by('order')])
            writer.writerow([
                reg.id,
                reg.team_leader_email,
                reg.project_field,
                reg.project_category,
                reg.registration_date,
                reg.members.count(),
                member_names,
                member_levels
            ])
        
        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('admin:index')

def admin_dashboard(request):
    """Simple admin dashboard to view registrations"""
    if not request.user.is_staff:
        return redirect('admin:login')
    
    registrations = Registration.objects.all().prefetch_related('members')
    
    # Pagination
    paginator = Paginator(registrations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'registrations': page_obj,
        'total_registrations': registrations.count(),
    }
    
    return render(request, 'registrations/admin_dashboard.html', context)