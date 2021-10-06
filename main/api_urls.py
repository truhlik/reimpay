from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from main.apps.companies import views as company_views
from main.apps.users import views as user_views
from main.apps.studies import views as studies_views
from main.apps.revisions import views as revision_views
from main.apps.smartform.views import AddressesSearchView
from main.apps.credit import views as credit_views
from main.apps.core import views as core_views
from main.apps.topups import views as topup_views
from main.apps.invoices import views as invoice_views
from main.apps.ticket import views as ticket_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('companies', company_views.CompanyViewSet, basename='company')
router.register('users', user_views.UserViewSets)
router.register('studies', studies_views.StudyViewSet)
router.register('study-items', studies_views.StudyItemViewSet)
router.register('arms', studies_views.ArmViewSet)
router.register('sites', studies_views.SiteViewSet)
router.register('patients', studies_views.PatientViewSet)
router.register('visits', studies_views.VisitViewSet)
router.register('visit-items', studies_views.VisitItemViewSet)
router.register('patient-visits', studies_views.PatientVisitViewSet)
router.register('patient-visit-items', studies_views.PatientVisitItemViewSet)
router.register('history', revision_views.HistoryViewSet)
router.register('credit', credit_views.CreditBalanceViewSet)
router.register('finance', core_views.StudyCreditInfoViewSet, basename='finance')
router.register('topups', topup_views.TopUpViewSet)
router.register('invoices', invoice_views.InvoiceViewSet)
router.register('tickets', ticket_views.TicketViewSets)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('doctor/login/', csrf_exempt(core_views.DoctorLoginView.as_view()), name='doctor-login'),
    path('addresses/suggestion/', csrf_exempt(AddressesSearchView.as_view()), name='api-address-suggestion'),
    path('topups/<int:pk>/pdf/', topup_views.TopUpPDF.as_view(), name='topup-pdf'),
    path('sites/<int:pk>/instruction/pdf/', studies_views.SitesInstructionPDFView.as_view(), name='sites-instruction-pdf'),
    path('sites/<int:pk>/patient/pdf/', studies_views.SitesPatientFormPDFView.as_view(), name='sites-patient-form-pdf'),
    path('', include(router.urls)),
]
