from rest_framework import serializers
from .models import Portfolio, Project, Contact


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

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
        if data['portfolio'].user.pk != self.context['request'].user.pk:
            raise serializers.ValidationError({"detail": "Portfolio belongs to other user"})
        return data


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

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
        if data['portfolio'].user.pk != self.context['request'].user.pk:
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
        if validated_data.get('id', None):
            portfolio = Portfolio.objects.get(pk=validated_data['id'])
            if validated_data.get('image', None):
                portfolio.image = validated_data['image']
            portfolio.header = validated_data['header']
            portfolio.about_me = validated_data['about_me']
            portfolio.link = validated_data['link']
            portfolio.save()

            for project in projects_data:
                proj = Project.objects.get(pk=project['id'])
                proj.name = project['name']
                proj.description = project['description']
                if project.get('image', None):
                    proj.image = project['image']
                proj.project_link = project['project_link']
                proj.save()
            for contact in contacts_data:
                cont = Contact.objects.get(pk=contact['id'])
                cont.social_network = contact['social_network']
                cont.link = contact['link']
                if contact.get('logo', None):
                    cont.logo = contact['logo']
                cont.save()

            return portfolio
        else:
            portfolio = Portfolio.objects.create(**validated_data)
            for project in projects_data:
                Project.objects.create(portfolio=portfolio, **project)
            for contact in contacts_data:
                Contact.objects.create(portfolio=portfolio, **contact)
            return portfolio
