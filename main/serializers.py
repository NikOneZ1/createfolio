from rest_framework import serializers
from .models import Portfolio, Project, Contact


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'image',
            'project_link'
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'social_network',
            'link',
            'logo'
        )


class PortfolioSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = (
            'image',
            'header',
            'about_me',
            'projects',
            'contacts'
        )
