#!/usr/bin/env python
"""
Script for setting up Cairo University Registration System
Setup script for Cairo University Registration System
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run system command and show result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # التحقق من Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]} - compatible")
    
    return True

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing project dependencies...")
    
    # تثبيت Django
    if not run_command("pip install django", "Installing Django"):
        return False
    
    return True

def setup_database():
    """Setup database"""
    print("🗄️ Setting up database...")
    
    # إنشاء migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    # تطبيق migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    # Create admin user
    print("\n👤 Creating admin user...")
    try:
        # Use Django's createsuperuser command with environment variables
        env = os.environ.copy()
        env['DJANGO_SUPERUSER_USERNAME'] = 'admin'
        env['DJANGO_SUPERUSER_EMAIL'] = 'admin@example.com'
        env['DJANGO_SUPERUSER_PASSWORD'] = 'admin123'
        
        subprocess.run(['python', 'manage.py', 'createsuperuser', '--noinput'], 
                      env=env, check=True, capture_output=True)
        
        print("✅ Admin user created successfully (admin / admin123)")
    except subprocess.CalledProcessError as e:
        # If createsuperuser fails, try alternative method
        try:
            # Alternative: Use Python directly with Django setup
            python_script = '''
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_system.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Admin user created: admin / admin123')
    else:
        print('Admin user already exists')
except Exception as e:
    print(f'Error: {e}')
'''
            
            # Create and run temporary script
            with open('temp_admin.py', 'w') as f:
                f.write(python_script)
            
            result = subprocess.run(['python', 'temp_admin.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Admin user created successfully")
                print(f"Output: {result.stdout.strip()}")
            else:
                print(f"❌ Failed to create admin user: {result.stderr}")
                return False
            
            # Clean up
            if os.path.exists('temp_admin.py'):
                os.remove('temp_admin.py')
                
        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
            return False
    
    return True

def start_server():
    """Start the server"""
    print("\n🚀 Starting server...")
    print("🌐 Server will run at: http://localhost:8000")
    print("📝 Admin panel: http://localhost:8000/admin/")
    print("📊 Control panel: http://localhost:8000/registration/admin/dashboard/")
    print("\n⚠️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run("python manage.py runserver", shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

def show_help():
    """Show help message"""
    print("""
🎯 Cairo University Registration System for Next Generation Sciences Competition

📋 Usage:
    python setup.py setup     - Setup complete system
    python setup.py server    - Run server only
    python setup.py help      - Show this message

🔧 Available Commands:
    python manage.py runserver       - Start the server
    python manage.py makemigrations  - Create migrations
    python manage.py migrate         - Apply migrations
    python manage.py createsuperuser - Create admin user
    python manage.py collectstatic   - Collect static files

🌐 Important Links:
    Homepage:                 http://localhost:8000/
    Admin Panel:              http://localhost:8000/admin/
    Control Panel:            http://localhost:8000/registration/admin/dashboard/
    CSV Export:               http://localhost:8000/registration/export-csv/

👤 Login Credentials:
    Username: admin
    Password: admin123
    """)

def main():
    """Main function"""
    print("🎓 Cairo University Registration System for Next Generation Sciences Competition")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        show_help()
    elif command == "setup":
        print("🚀 Starting system setup...")
        
        # Check requirements
        if not check_requirements():
            print("❌ Failed to check requirements")
            return
        
        # Install requirements
        if not install_dependencies():
            print("❌ Failed to install requirements")
            return
        
        # Setup database
        if not setup_database():
            print("❌ Failed to setup database")
            return
        
        print("\n🎉 System setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Go to: http://localhost:8000/")
        print("2. Fill out the registration form")
        print("3. View registrations at: http://localhost:8000/admin/")
        print("4. Export data from: http://localhost:8000/registration/admin/dashboard/")
        
        # تشغيل الخادم
        start_server()
        
    elif command == "server":
        print("🚀 Starting server...")
        start_server()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()