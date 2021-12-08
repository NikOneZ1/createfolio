from rest_framework import serializers
from .models import Portfolio, Project, Contact
from django.db import transaction


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    portfolio = serializers.PrimaryKeyRelatedField(queryset=Portfolio.objects.all(), required=False)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'image',
            'project_link',
            'portfolio'
        )

    """Check if current user is portfolio owner"""
    def validate(self, data):
        if data.get('portfolio', None) and data['portfolio'].user.pk != self.context['request'].user.pk:
            raise serializers.ValidationError({"detail": "Portfolio belongs to other user"})
        return data


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    portfolio = serializers.PrimaryKeyRelatedField(queryset=Portfolio.objects.all(), required=False)

    class Meta:
        model = Contact
        fields = (
            'id',
            'social_network',
            'link',
            'logo',
            'portfolio'
        )

    def validate(self, data):
        if data.get('portfolio', None) and data['portfolio'].user.pk != self.context['request'].user.pk:
            raise serializers.ValidationError({"detail": "Portfolio belongs to other user"})
        return data


class PortfolioSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)
    contacts = ContactSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Portfolio
        fields = (
            'id',
            'image',
            'header',
            'about_me',
            'link',
            'projects',
            'contacts',
            'user'
        )

    def update(self, instance, validated_data):
        projects_data = validated_data.pop('projects')
        contacts_data = validated_data.pop('contacts')
        if self.context['request'].method == 'PATCH' or self.context['request'].method == 'PUT':
            portfolio = Portfolio.objects.get(link=self.context['view'].kwargs.get("link"))
            if validated_data.get('image', None):
                portfolio.image = validated_data['image']
            portfolio.header = validated_data['header']
            portfolio.about_me = validated_data['about_me']
            portfolio.link = validated_data['link']
            portfolio.save()

            with transaction.atomic():
                project_ids = [project['id'] for project in projects_data]
                project_objects = list(Project.objects.filter(pk__in=project_ids))
                for project, project_data in zip(project_objects, projects_data):
                    project.name = project_data['name']
                    project.description = project_data['description']
                    if project_data.get('image', None):
                        project.image = project_data['image']
                    project.project_link = project_data['project_link']

                contact_ids = [contact['id'] for contact in contacts_data]
                contact_objects = list(Contact.objects.filter(pk__in=contact_ids))
                for contact, contact_data in zip(contact_objects, contacts_data):
                    contact.social_network = contact_data['social_network']
                    contact.link = contact_data['link']
                    if contact_data.get('logo', None):
                        contact.logo = contact_data['logo']

                Project.objects.bulk_update(project_objects, ['name', 'description', 'image', 'project_link'])
                Contact.objects.bulk_update(contact_objects, ['social_network', 'link', 'logo'])

            return portfolio
        elif self.context['request'].method == 'POST':
            with transaction.atomic():
                portfolio = Portfolio.objects.create(**validated_data)
                for project in projects_data:
                    project['portfolio'] = portfolio
                Project.objects.bulk_create([Project(**project) for project in projects_data])
                for contact in contacts_data:
                    contact['portfolio'] = portfolio
                Contact.objects.bulk_create([Contact(**contact) for contact in contacts_data])
            return portfolio
