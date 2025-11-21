# Django Registration System - Ready for Render Deployment

A complete Django web application for competition team registration with PostgreSQL database support, CSV export functionality, and email field for admin contact.

## 🚀 DEPLOYMENT READY - Render.com

This application is **completely prepared** for free deployment on Render.com with:

- ✅ **Free PostgreSQL database** included
- ✅ **HTTPS and SSL certificates** automatic
- ✅ **Git-based deployment** from GitHub
- ✅ **Production-ready security settings**
- ✅ **Environment variable configuration**
- ✅ **Static file optimization with WhiteNoise**

### 📚 Complete Deployment Guide
See `RENDER_DEPLOYMENT_GUIDE.md` for step-by-step deployment instructions.

---

## نظام تسجيل مسابقة جامعة القاهرة في علوم الجيل下一代

نظام تسجيل إلكتروني متكامل لإدارة تسجيلات الفرق في مسابقة جامعة القاهرة في علوم الجيل下一代، مع دعم كامل للقاعدة البيانات وتصدير البيانات بصيغة CSV.

## المميزات الرئيسية

### ✅ **الميزات الأساسية**
- **حقل البريد الإلكتروني**: حقل بريد إلكتروني عريض للتواصل مع الإداريين
- **قاعدة بيانات**: دعم SQLite للتطوير و PostgreSQL للإنتاج
- **تصدير CSV**: تصدير جميع التسجيلات إلى ملف Excel
- **التحقق من صحة البيانات**: منع التسجيلات المكررة والبيانات غير الصحيحة
- **التحقق من اللغة الإنجليزية**: قبول الأحرف الإنجليزية فقط في الأسماء
- **واجهة عربية**: تصميم محسن للغة العربية مع اتجاه RTL

### 🔧 **المميزات التقنية**
- **Django 5.2.8**: أحدث إصدار من Django
- **PostgreSQL Support**: قاعدة بيانات PostgreSQL للإنتاج
- **Production Ready**: إعدادات الإنتاج والأمان
- **Whitenoise Integration**: تحسين ملفات CSS و JavaScript
- **Environment Variables**: إدارة الإعدادات عبر متغيرات البيئة
- **Gunicorn WSGI**: خادم WSGI للإنتاج

## متطلبات النظام

### للتطوير المحلي
- Python 3.11+
- Django 5.2.8
- متصفح حديث يدعم JavaScript

### للنشر على Render
- GitHub repository
- حساب Render.com (مجاني)

## التثبيت والإعداد

### 1. إعداد البيئة المحلية
```bash
# Clone repository
git clone <your-repo-url>
cd registration_system

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run tests
python test_deployment.py

# Start development server
python manage.py runserver
```

### 2. النشر على Render (مجاني)
```bash
# Test deployment preparation
./prepare_deployment.sh

# Push to GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main

# Follow RENDER_DEPLOYMENT_GUIDE.md for step-by-step instructions
```

## استخدام النظام

### التسجيل في المسابقة
1. اذهب إلى الصفحة الرئيسية: http://localhost:8000/
2. املأ معلومات الفريق:
   - **البريد الإلكتروني لقائد الفريق** (حقل عريض)
   - أسماء ومستويات أعضاء الفريق (2-5 أعضاء)
   - مجال وفئة المشروع
   - الموافقة على الشروط
3. اضغط "تسجيل المشاركة"

### إدارة التسجيلات
1. اذهب إلى لوحة الإدارة: http://localhost:8000/admin/
2. سجل الدخول باستخدام بيانات المدير
3. عرض التسجيلات في قسم "تسجيلات الفرق"

### تصدير البيانات
1. اذهب إلى: http://localhost:8000/export-csv/
2. تحميل ملف CSV بجميع التسجيلات

## هيكل المشروع

```
registration_system/
├── manage.py                    # Django management
├── requirements.txt            # ✅ Dependencies for deployment
├── Procfile                    # ✅ Render deployment config
├── runtime.txt                 # ✅ Python version
├── .env.example                # ✅ Environment template
├── RENDER_DEPLOYMENT_GUIDE.md  # ✅ Complete deployment guide
├── test_deployment.py          # ✅ Pre-deployment testing
├── prepare_deployment.sh       # ✅ Setup script
├── registration_system/        # Django project
│   ├── settings.py            # ✅ Production-ready settings
│   ├── wsgi.py               # ✅ Enhanced WSGI
│   └── urls.py               # Main URLs
├── db.sqlite3                 # SQLite database (development)
└── registrations/             # Main application
    ├── models.py             # Registration & TeamMember
    ├── forms.py              # Form with email validation
    ├── views.py              # Registration handling
    ├── urls.py               # App URLs
    ├── templates/
    │   └── registrations/
    │       └── index.html    # ✅ Wide email field
    └── migrations/
```

## قاعدة البيانات

### نموذج Registration (التسجيل)
- `team_leader_email`: إيميل قائد الفريق (فريد)
- `project_field`: مجال المشروع (الصحة/الطاقة/البيئة)
- `project_category`: فئة المشروع
- `accept_terms`: موافقة على الشروط
- `registration_date`: تاريخ التسجيل
- `members`: أعضاء الفريق (علاقة Many-to-Many)

### نموذج TeamMember (عضو الفريق)
- `name`: اسم الطالب (الإنجليزية فقط)
- `level`: المستوى الدراسي (بكالوريوس/ماجستير/دكتوراه)
- `order`: ترتيب العضو
- `registrations`: التسجيلات المرتبطة

## الميزات التقنية

### الأمان
- ✅ حماية CSRF
- ✅ التحقق من صحة البيانات
- ✅ منع التسجيلات المكررة
- ✅ تنظيف المدخلات
- ✅ إعدادات HTTPS للإنتاج
- ✅ Headers أمنية (HSTS, CSP, X-Frame-Options)

### الأداء
- ✅ استخدام Django ORM
- ✅ Pagination للنتائج
- ✅ تحميل الملفات الثابتة بكفاءة
- ✅ تحسين استعلامات قاعدة البيانات
- ✅ Whitenoise للملفات الثابتة

### قابلية الاستخدام
- ✅ رسائل خطأ واضحة
- ✅ حقل بريد إلكتروني عريض
- ✅ تحميل تفاعلي أثناء الإرسال
- ✅ واجهة سهلة ومفهومة
- ✅ تصميم متجاوب

## النشر المجاني على Render

### المميزات المجانية
- **750 ساعة شهرياً** من وقت التشغيل
- **قاعدة بيانات PostgreSQL مجانية**
- **شهادات SSL تلقائية**
- **النشر التلقائي من GitHub**
- **CDN عالمي** للملفات الثابتة

### الخطوات السريعة
1. أنشئ حساب على [Render.com](https://render.com)
2. اربط مستودع GitHub
3. أنشئ قاعدة بيانات PostgreSQL
4. أنشئ Web Service
5. حدد متغيرات البيئة
6. انشر تلقائياً

### تفاصيل أكثر
راجع `RENDER_DEPLOYMENT_GUIDE.md` للحصول على تعليمات مفصلة خطوة بخطوة.

## استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### 1. خطأ "ModuleNotFoundError: No module named 'django'"
**الحل**: تأكد من تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

#### 2. خطأ في متغيرات البيئة
**الحل**: تأكد من إعداد ملف .env
```bash
cp .env.example .env
# Edit .env with your values
```

#### 3. أخطاء النشر على Render
**الحل**: تأكد من إعداد متغيرات البيئة
- SECRET_KEY=your-secret-key
- DEBUG=False
- ALLOWED_HOSTS=your-app.onrender.com
- DATABASE_URL=postgresql://user:pass@host:port/database

## الملفات الجديدة

### ملفات النشر
- `requirements.txt` - متطلبات Python للنشر
- `Procfile` - إعداد النشر على Render
- `runtime.txt` - إصدار Python
- `.env.example` - قالب متغيرات البيئة
- `RENDER_DEPLOYMENT_GUIDE.md` - دليل النشر الكامل
- `test_deployment.py` - اختبار ما قبل النشر
- `prepare_deployment.sh` - سكريبت الإعداد

### ملفات محدثة
- `settings.py` - إعدادات الإنتاج
- `wsgi.py` - إعداد WSGI محسن
- `index.html` - حقل بريد إلكتروني عريض

## الدعم والصيانة

### إضافة ميزات جديدة
1. أنشئ migration جديدة: `python manage.py makemigrations`
2. طبق التغييرات: `python manage.py migrate`
3. اختبر النظام: `python test_deployment.py`

### النسخ الاحتياطي
لنسخ قاعدة البيانات:
```bash
# Local
cp db.sqlite3 db.sqlite3.backup

# Render (via admin)
# Export from Django admin panel
```

### التحديث
```bash
pip install --upgrade django
python manage.py migrate
```

---

## معلومات الاتصال

تم تطوير هذا النظام باستخدام:
- Django 5.2.8
- Python 3.11.0
- PostgreSQL (Production)
- WhiteNoise (Static files)
- Gunicorn (WSGI Server)

**جاهز للنشر المجاني على Render.com!** 🚀

---
*نظام تسجيل مسابقة جامعة القاهرة في علوم الجيل下一代*