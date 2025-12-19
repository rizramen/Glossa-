from django.views.generic import TemplateView

class FriendsView(TemplateView):
    template_name = "friends/list.html"
