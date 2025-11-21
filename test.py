#!/usr/bin/env python
"""
اختبار سريع للنظام
Quick system test
"""

import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_system.settings')
django.setup()

def test_models():
    """اختبار النماذج"""
    print("🔍 اختبار النماذج...")
    
    try:
        from registrations.models import Registration, TeamMember
        
        # اختبار إنشاء عضو
        member = TeamMember.objects.create(
            name="أحمد محمد",
            level="bachelor",
            order=1
        )
        print(f"✅ تم إنشاء عضو: {member.name}")
        
        # اختبار إنشاء تسجيل
        registration = Registration.objects.create(
            team_leader_email="test@example.com",
            project_field="health",
            project_category="student_research",
            accept_terms=True
        )
        
        # ربط العضو بالتسجيل
        registration.members.add(member)
        print(f"✅ تم إنشاء تسجيل: {registration.team_leader_email}")
        
        # اختبار عرض البيانات
        print(f"   عدد الأعضاء: {registration.get_members_count()}")
        print(f"   المجال: {registration.get_project_field_display()}")
        
        # تنظيف البيانات التجريبية
        registration.delete()
        member.delete()
        print("🧹 تم تنظيف البيانات التجريبية")
        
        print("✅ جميع الاختبارات نجحت!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def test_csv_export():
    """اختبار تصدير CSV"""
    print("\n📤 اختبار تصدير CSV...")
    try:
        # إنشاء بيانات اختبار
        registration = Registration.objects.create(
            team_leader_email="test@example.com",
            project_field="health",
            project_category="student_research",
            accept_terms=True
        )
        
        # اختبار تصدير CSV
        csv_content = Registration.export_to_csv()
        
        print(f"✅ تم إنشاء CSV بحجم {len(csv_content)} حرف")
        
        # تنظيف
        registration.delete()
        
        return True
    except Exception as e:
        print(f"❌ خطأ في تصدير CSV: {e}")
        return False

def main():
    print("🧪 اختبار سريع لنظام التسجيل")
    print("=" * 35)
    
    success = True
    
    # اختبار النماذج
    if not test_models():
        success = False
    
    # اختبار تصدير CSV
    if not test_csv_export():
        success = False
    
    if success:
        print("\n🎉 النظام يعمل بشكل صحيح!")
        print("يمكنك الآن:")
        print("1. تشغيل الخادم: python manage.py runserver")
        print("2. زيارة الصفحة: http://localhost:8000/")
        print("3. استخدام لوحة الإدارة: http://localhost:8000/admin/")
    else:
        print("\n❌ توجد مشاكل في النظام")

if __name__ == "__main__":
    main()