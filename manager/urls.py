from django.urls import path

from . import views

urlpatterns = [
    path("partners", views.partners, name="partners"),
    path("partners/add", views.addPartner, name="addPartner"),
    path("partners/<int:partner_id>/update", views.updatePartner, name="updatePartner"),
    path("partners/<int:partner_id>/deactivate", views.deactivatePartner, name="deactivatePartner"),
    path("partners/<int:partner_id>/activate", views.activatePartner, name="activatePartner"),

]
