#!/usr/bin/env python
"""
Script لإضافة بيانات تجريبية لاختبار النظام
Demo script for testing the registration system
"""

import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registration_system.settings')
django.setup()

from registrations.models import Registration, TeamMember

def create_sample_data():
    """إنشاء بيانات تجريبية"""
    print("🎭 إنشاء بيانات تجريبية...")
    
    # إنشاء تسجيالت تجريبية
    sample_data = [
        {
            'team_leader_email': 'ahmed.mohamed@university.edu.eg',
            'project_field': 'health',
            'project_category': 'student_research',
            'members': [
                {'name': 'أحمد محمد علي', 'level': 'bachelor', 'order': 1},
                {'name': 'فاطمة أحمد حسن', 'level': 'bachelor', 'order': 2},
                {'name': 'محمد عبدالرحمن', 'level': 'master', 'order': 3},
            ]
        },
        {
            'team_leader_email': 'sara.adel@university.edu.eg',
            'project_field': 'energy',
            'project_category': 'prototype',
            'members': [
                {'name': 'سارة عادل محمود', 'level': 'master', 'order': 1},
                {'name': 'يوسف إبراهيم', 'level': 'bachelor', 'order': 2},
            ]
        },
        {
            'team_leader_email': 'omar.khalil@university.edu.eg',
            'project_field': 'environment',
            'project_category': 'science_communication',
            'members': [
                {'name': 'عمر خليل أحمد', 'level': 'phd', 'order': 1},
                {'name': 'نور الهدى حسن', 'level': 'master', 'order': 2},
                {'name': 'عبدالله محمد', 'level': 'bachelor', 'order': 3},
                {'name': 'زينب عبداللطيف', 'level': 'bachelor', 'order': 4},
            ]
        }
    ]
    
    created_count = 0
    
    for data in sample_data:
        # التحقق من عدم وجود الإيميل مسبقاً
        if not Registration.objects.filter(team_leader_email=data['team_leader_email']).exists():
            # إنشاء التسجيل
            registration = Registration.objects.create(
                team_leader_email=data['team_leader_email'],
                project_field=data['project_field'],
                project_category=data['project_category'],
                accept_terms=True
            )
            
            # إنشاء أعضاء الفريق
            for member_data in data['members']:
                member = TeamMember.objects.create(
                    name=member_data['name'],
                    level=member_data['level'],
                    order=member_data['order']
                )
                registration.members.add(member)
            
            created_count += 1
            print(f"✅ تم إنشاء تسجيل للفريق: {data['team_leader_email']}")
        else:
            print(f"⚠️  التسجيل موجود بالفعل: {data['team_leader_email']}")
    
    print(f"\n🎯 تم إنشاء {created_count} تسجيل جديد")
    
    # عرض إحصائيات
    total_registrations = Registration.objects.count()
    total_members = TeamMember.objects.count()
    
    print(f"\n📊 إحصائيات النظام:")
    print(f"   إجمالي التسجيلات: {total_registrations}")
    print(f"   إجمالي الأعضاء: {total_members}")
    print(f"   متوسط أعضاء الفريق: {total_members/total_registrations:.1f}")

def display_statistics():
    """عرض إحصائيات مفصلة"""
    print("\n📈 إحصائيات مفصلة:")
    print("=" * 50)
    
    registrations = Registration.objects.all().prefetch_related('members')
    
    for reg in registrations:
        members_list = []
        for member in reg.members.all().order_by('order'):
            members_list.append(f"{member.name} ({member.get_level_display()})")
        
        print(f"\n📋 فريق: {reg.team_leader_email}")
        print(f"   المجال: {reg.get_project_field_display()}")
        print(f"   الفئة: {reg.get_project_category_display()}")
        print(f"   الأعضاء ({len(members_list)}): {'، '.join(members_list)}")
        print(f"   التاريخ: {reg.registration_date.strftime('%Y-%m-%d %H:%M')}")

def test_csv_export():
    """اختبار تصدير CSV"""
    print("\n📤 اختبار تصدير CSV...")
    try:
        csv_content = Registration.export_to_csv()
        print("✅ تم إنشاء محتوى CSV بنجاح")
        print(f"   حجم البيانات: {len(csv_content)} حرف")
        print("   يحتوي على جميع التسجيلات وأعضاء الفرق")
    except Exception as e:
        print(f"❌ خطأ في تصدير CSV: {e}")

def clear_sample_data():
    """مسح البيانات التجريبية"""
    print("\n🗑️ مسح جميع البيانات...")
    
    # حذف جميع التسجيلات والأعضاء
    Registration.objects.all().delete()
    TeamMember.objects.all().delete()
    
    print("✅ تم مسح جميع البيانات")

def main():
    """الدالة الرئيسية"""
    print("🎭 نظام اختبار البيانات التجريبية")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("""
🔧 الأوامر المتاحة:
    python demo.py create   - إنشاء بيانات تجريبية
    python demo.py stats    - عرض الإحصائيات
    python demo.py test     - اختبار النظام
    python demo.py clear    - مسح البيانات
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_sample_data()
        display_statistics()
    elif command == "stats":
        display_statistics()
    elif command == "test":
        test_csv_export()
        display_statistics()
    elif command == "clear":
        clear_sample_data()
        print("✅ تم مسح البيانات")
    else:
        print(f"❌ أمر غير معروف: {command}")

if __name__ == "__main__":
    main()