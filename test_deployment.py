#!/usr/bin/env python3
"""
Django Registration System - Pre-Deployment Test
This script tests your Django application before deployment to ensure everything is working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_system.settings')
django.setup()

def test_django_settings():
    """Test Django settings and configuration"""
    print("🔧 Testing Django Settings...")
    
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        print(f"✅ Django version: {django.__version__}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        print(f"✅ Secret key length: {len(settings.SECRET_KEY)}")
        print(f"✅ Allowed hosts: {settings.ALLOWED_HOSTS}")
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        return True
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False

def test_models():
    """Test Django models"""
    print("\n📊 Testing Models...")
    
    try:
        from registrations.models import Registration, TeamMember
        
        print(f"✅ Registration model loaded")
        print(f"✅ TeamMember model loaded")
        
        # Check model fields
        reg_fields = [field.name for field in Registration._meta.fields]
        print(f"✅ Registration fields: {reg_fields}")
        
        member_fields = [field.name for field in TeamMember._meta.fields]
        print(f"✅ TeamMember fields: {member_fields}")
        
        return True
    except Exception as e:
        print(f"❌ Models error: {e}")
        return False

def test_forms():
    """Test Django forms"""
    print("\n📝 Testing Forms...")
    
    try:
        from registrations.forms import RegistrationForm
        
        form = RegistrationForm()
        print(f"✅ RegistrationForm loaded")
        print(f"✅ Form fields: {list(form.fields.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ Forms error: {e}")
        return False

def test_views():
    """Test Django views"""
    print("\n🔍 Testing Views...")
    
    try:
        from registrations.views import index, export_csv
        
        print(f"✅ index view: {index}")
        print(f"✅ export_csv view: {export_csv}")
        
        return True
    except Exception as e:
        print(f"❌ Views error: {e}")
        return False

def test_url_patterns():
    """Test URL patterns"""
    print("\n🛣️ Testing URLs...")
    
    try:
        from django.urls import reverse
        
        # Test URL reversal
        index_url = reverse('registration_index')
        export_url = reverse('export_csv')
        
        print(f"✅ Index URL: {index_url}")
        print(f"✅ Export CSV URL: {export_url}")
        
        return True
    except Exception as e:
        print(f"❌ URLs error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing Dependencies...")
    
    required_packages = [
        'django',
        'gunicorn',
        'whitenoise',
        'psycopg2',
        'python_dotenv',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing!")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {missing_packages}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_static_files():
    """Test static files configuration"""
    print("\n📁 Testing Static Files...")
    
    try:
        from django.conf import settings
        
        static_url = settings.STATIC_URL
        static_root = settings.STATIC_ROOT
        static_dirs = settings.STATICFILES_DIRS
        
        print(f"✅ Static URL: {static_url}")
        print(f"✅ Static root: {static_root}")
        print(f"✅ Static dirs: {static_dirs}")
        
        return True
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Django Registration System - Pre-Deployment Tests")
    print("=" * 60)
    
    tests = [
        test_dependencies,
        test_django_settings,
        test_models,
        test_forms,
        test_views,
        test_url_patterns,
        test_static_files,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your app is ready for deployment!")
        print("\n🚀 Next steps:")
        print("1. Run: python manage.py runserver (test locally)")
        print("2. Push to GitHub")
        print("3. Follow RENDER_DEPLOYMENT_GUIDE.md")
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        print("\n🔧 Common fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check .env file configuration")
        print("- Run migrations: python manage.py migrate")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)