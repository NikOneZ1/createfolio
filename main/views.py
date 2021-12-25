from .serializers import PortfolioSerializer, ProjectSerializer, ContactSerializer
from .permissions import PortfolioUserPermission, ProjectContactUserPermission
from .models import Portfolio, Project, Contact
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
from django.shortcuts import render


def index(request):
    return render(request, 'build/index.html')


class UserPortfolioListView(generics.ListAPIView):
    """Get list of user portfolios"""
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(user=user.pk)


class PortfolioCreateView(generics.CreateAPIView):
    """
    Create portfolio
    If you`re trying to create portfolio you don't have to send 'id' field in request
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        user = self.request.user
        self.request.data['user'] = str(user.id)
        kwargs['data'] = self.request.data
        return serializer_class(user, *args, **kwargs)


class PortfolioView(generics.RetrieveUpdateDestroyAPIView):
    """Get, Update, Delete portfolio"""
    permission_classes = [IsAuthenticatedOrReadOnly, PortfolioUserPermission]
    serializer_class = PortfolioSerializer
    lookup_field = 'link'
    queryset = Portfolio.objects.all()


class ProjectCreateView(generics.CreateAPIView):
    """Create project"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer


class ProjectUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Update or remove project"""
    permission_classes = [IsAuthenticated, ProjectContactUserPermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ContactCreateView(generics.CreateAPIView):
    """Create contact"""
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer


class ContactUpdateRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """Update or remove contact"""
    permission_classes = [IsAuthenticated, ProjectContactUserPermission]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
