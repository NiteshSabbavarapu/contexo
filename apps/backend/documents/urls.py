from django.urls import path
from .views import create_document, search_documents

urlpatterns = [
    path("", create_document, name="create-document"),
    path("search/", search_documents, name="search-documents"),
]