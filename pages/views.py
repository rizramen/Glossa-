from django.views.generic import TemplateView

class LandingView(TemplateView):
    template_name = "pages/landing.html"

class DashboardView(TemplateView):
    template_name = "pages/dashboard.html"
