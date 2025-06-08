# Healthcare Management System - Backend API

A comprehensive Django REST API for managing healthcare operations including patient records, doctor information, and patient-doctor mappings with secure authentication. This project was developed as a Django assignment and includes all required features plus several enhancements.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Patient Management**: CRUD operations for patient records with user-specific access
- **Doctor Management**: Complete doctor profiles with specializations and availability
- **Patient-Doctor Mapping**: Assign and manage doctor-patient relationships
- **Permission-based Access**: Secure access control ensuring users can only access their own data
- **API Documentation**: Auto-generated Swagger/ReDoc documentation
- **PostgreSQL Database**: Production-ready database with Supabase integration

## Technology Stack

- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL (Render Database)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **CORS**: django-cors-headers for frontend integration

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (Render PostgreSQL or local)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthcare-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

5. **Database Setup**
   Update the database configuration in `settings.py` with your Render PostgreSQL credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'your_render_host.com',
           'PORT': '5432',
       }
   }
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## Assignment Requirements ✅

This project successfully implements all the required features from the Django Healthcare Backend assignment:

### ✅ Core Requirements Met:
- **Django & DRF**: Built with Django and Django REST Framework
- **PostgreSQL**: Using Render PostgreSQL database
- **JWT Authentication**: Implemented with djangorestframework-simplejwt
- **RESTful APIs**: All required endpoints implemented
- **Django ORM**: Complete database modeling
- **Error Handling**: Comprehensive validation and error handling
- **Environment Variables**: Sensitive configurations properly managed

### ✅ Required API Endpoints:

### Complete API Reference

### Authentication APIs
- `POST /api/auth/register/` - User registration with name, email, password ✅
- `POST /api/auth/login/` - User login with JWT token response ✅

#### Patient Management APIs
- `POST /api/patients/` - Add new patient (authenticated users only) ✅
- `GET /api/patients/` - Retrieve user's patients ✅
- `GET /api/patients/<id>/` - Get specific patient details ✅
- `PUT /api/patients/<id>/` - Update patient details ✅
- `DELETE /api/patients/<id>/` - Delete patient record ✅

#### Doctor Management APIs
- `POST /api/doctors/` - Add new doctor (authenticated users only) ✅
- `GET /api/doctors/` - Retrieve all doctors ✅
- `GET /api/doctors/<id>/` - Get specific doctor details ✅
- `PUT /api/doctors/<id>/` - Update doctor details ✅
- `DELETE /api/doctors/<id>/` - Delete doctor record ✅

#### Patient-Doctor Mapping APIs
- `POST /api/mappings/` - Assign doctor to patient ✅
- `GET /api/mappings/` - Retrieve all patient-doctor mappings ✅
- `GET /api/mappings/<patient_id>/` - Get patient's assigned doctors ✅
- `DELETE /api/mappings/<id>/` - Remove doctor from patient ✅

## 🚀 Additional Features Implemented (Beyond Requirements)

### Enhanced Security & Permissions
- **Custom Permission Classes**: `IsOwnerOrReadOnly` and `IsPatientOwner` for granular access control
- **User-specific Data Isolation**: Users can only access their own patients and mappings
- **JWT Token Refresh**: Automatic token refresh functionality
- **Soft Delete**: Deactivation instead of hard deletion for patient-doctor mappings

### Advanced API Features
- **Query Parameters**: Filter doctors by specialization and availability
- **Pagination**: Built-in pagination for large datasets
- **Detailed Serializers**: Rich data representation with related fields
- **Patient Count**: Automatic calculation of patient count per doctor

### Developer Experience
- **Django Admin Integration**: Full admin interface for all models
- **API Documentation**: Auto-generated Swagger/ReDoc documentation
- **CORS Support**: Ready for frontend integration
- **Comprehensive Models**: Extended fields for real-world healthcare needs

### Data Model Enhancements
- **Patient Model**: Extended with medical history, address, contact details
- **Doctor Model**: Complete professional profile with fees, qualifications, experience
- **Mapping Model**: Enhanced with notes, timestamps, and status tracking
- **Validation**: Age limits, email validation, experience validation

### Production-Ready Features
- **Environment Configuration**: Proper settings management
- **Database Optimization**: Efficient queries and indexing
- **Error Handling**: Comprehensive error responses
- **Security Headers**: CORS and security middleware configured

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Patients
- `GET /api/patients/` - List user's patients
- `POST /api/patients/` - Create new patient
- `GET /api/patients/{id}/` - Get patient details
- `PUT /api/patients/{id}/` - Update patient
- `DELETE /api/patients/{id}/` - Delete patient

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create new doctor
- `GET /api/doctors/{id}/` - Get doctor details
- `PUT /api/doctors/{id}/` - Update doctor
- `DELETE /api/doctors/{id}/` - Delete doctor

Query parameters for doctors:
- `specialization` - Filter by specialization
- `available` - Filter by availability (true/false)

### Patient-Doctor Mappings
- `GET /api/mappings/` - List user's patient-doctor mappings
- `POST /api/mappings/` - Assign doctor to patient
- `GET /api/mappings/{patient_id}/` - Get patient's assigned doctors
- `DELETE /api/mappings/{id}/` - Remove doctor from patient

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## Data Models

### Patient
- Personal information (name, age, gender, contact)
- Medical history
- User association (created_by)
- Timestamps

### Doctor
- Professional information (name, specialization, experience)
- Contact details and consultation fees
- Availability status
- Timestamps

### PatientDoctorMapping
- Links patients with their assigned doctors
- Assignment dates and notes
- Active status for soft deletion

## Authentication & Permissions

- **JWT Authentication**: All endpoints (except registration/login) require valid JWT tokens
- **User-specific Access**: Users can only access their own patients and mappings
- **Role-based Permissions**: Custom permission classes ensure data security

### JWT Token Usage

Include the access token in the Authorization header:
```
Authorization: Bearer <your-access-token>
```

## Security Features

- Password validation and hashing
- JWT token expiration and refresh
- User-specific data isolation
- Input validation and sanitization
- CORS configuration for frontend integration

## Database Schema

The application uses three main models with the following relationships:
- One User can have many Patients
- Many Patients can be assigned to many Doctors (through PatientDoctorMapping)
- PatientDoctorMapping maintains the relationship with additional metadata

## Development

### Project Structure
```
healthcare_backend/
├── api/
│   ├── models.py          # Data models
│   ├── serializers.py     # API serializers
│   ├── views.py          # API views
│   ├── permissions.py    # Custom permissions
│   ├── admin.py          # Django admin config
│   └── urls.py           # API URLs
├── healthcare_backend/
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL config
│   └── wsgi.py          # WSGI config
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

### Running Tests
```bash
python manage.py test
```

### Code Quality
The codebase follows Django best practices:
- Model-View-Serializer pattern
- Custom permissions for security
- Proper error handling and validation
- Clean code structure and documentation

## Deployment

### Environment Variables
For production, set these environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False
- `ALLOWED_HOSTS`: Your domain names

### Production Considerations
- Use environment variables for sensitive data
- Enable HTTPS
- Configure proper CORS settings
- Set up database backups
- Monitor API usage and performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the development team.

---

