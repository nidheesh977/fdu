from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf.urls.static import static
from application.views import callback, exam_purchase_success, event_purchase_success, eventcallback
from django.views.generic.base import TemplateView

urlpatterns = [
    path('db/', admin.site.urls), # -> default admin panel

    path('summernote/', include('django_summernote.urls')),

    path('',include(('application.urls',"application"), namespace='application')), # -> application 
    path('admin/',include(('admin_dashboard.urls',"admin_dashboard"), namespace='custom_admin')),
    # Razorpay
    path("razorpay/callback/<str:id>/<str:uid>", callback, name="callback"),
    path("razorpay/event-callback/<str:id>/<str:uid>", eventcallback, name="event-callback"),
    # Phonepe
    path("phonepe/exam_purchase_success/<str:type>/<str:id>/<str:uid>/<str:payment_id>", exam_purchase_success, name="exam_purchase_success"),
    path("phonepe/event_purchase_success/<str:id>/<str:uid>/<str:payment_id>", eventcallback, name="event_purchase_success"),
    path("privacy-policy", TemplateView.as_view(template_name="privacy-policy.html"), name="privacy-policy"),
    path("terms-and-conditions", TemplateView.as_view(template_name="terms_conditions.html"), name="terms-and-conditions"),
    path("disclaimer", TemplateView.as_view(template_name="disclaimer.html"), name="disclaimer"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
