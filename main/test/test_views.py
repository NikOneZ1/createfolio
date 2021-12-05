from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from ..models import Portfolio, Project, Contact
from ..serializers import PortfolioSerializer, ProjectSerializer, ContactSerializer
import json


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        username_1 = 'test1'
        username_2 = 'test2'
        password = 'testtesttest'
        cls.user_1 = User.objects.create_user(username=username_1, password=password)
        data = {'username': username_1, 'password': password}
        cls.user1_token = cls.client.post('/auth/jwt/create/', data=data).data['access']
        cls.user_2 = User.objects.create_user(username=username_2, password=password)
        data = {'username': username_2, 'password': password}
        cls.user2_token = cls.client.post('/auth/jwt/create/', data=data).data['access']

    def setUp(self):
        """Creating first portfolio"""
        self.portfolio_1 = Portfolio.objects.create(
            image=None,
            header='Portfolio 1 test header',
            about_me='Some text in portfolio 1 about me part.',
            link='portfolio1',
            user=self.user_1
        )
        Project.objects.create(
            name='Google',
            description='Some information about google.',
            image=None,
            project_link='https://www.google.com',
            portfolio=self.portfolio_1
        )
        Project.objects.create(
            name='Bing',
            description='Some information about bing.',
            image=None,
            project_link='https://www.bing.com',
            portfolio=self.portfolio_1
        )
        Contact.objects.create(
            social_network='GitHub',
            link='https://www.github.com',
            logo=None,
            portfolio=self.portfolio_1
        )
        Contact.objects.create(
            social_network='Linkedin',
            link='https://www.linkedin.com',
            logo=None,
            portfolio=self.portfolio_1
        )

        """Creating second portfolio"""
        self.portfolio_2 = Portfolio.objects.create(
            image=None,
            header='Portfolio 2 test header',
            about_me='Some text in portfolio 2 about me part.',
            link='portfolio2',
            user=self.user_1
        )
        Project.objects.create(
            name='YouTube',
            description='Some information about youtube.',
            image=None,
            project_link='https://www.youtube.com',
            portfolio=self.portfolio_2
        )
        Project.objects.create(
            name='RealPython',
            description='Some information about realpython.',
            image=None,
            project_link='https://www.realpython.com',
            portfolio=self.portfolio_2
        )
        Contact.objects.create(
            social_network='Facebook',
            link='https://www.facebook.com',
            logo=None,
            portfolio=self.portfolio_2
        )
        Contact.objects.create(
            social_network='Instagram',
            link='https://www.instagram.com',
            logo=None,
            portfolio=self.portfolio_2
        )

        """Creating portfolio for second user"""
        self.portfolio_3 = Portfolio.objects.create(
            image=None,
            header='Portfolio 3 test header',
            about_me='Some text in portfolio 3 about me part.',
            link='portfolio3',
            user=self.user_2
        )
        Project.objects.create(
            name='Wikipedia',
            description='Some information about wikipedia.',
            image=None,
            project_link='https://www.wikipedia.org',
            portfolio=self.portfolio_3
        )
        Project.objects.create(
            name='Ebay',
            description='Some information about ebay.',
            image=None,
            project_link='https://www.ebay.com',
            portfolio=self.portfolio_3
        )
        Contact.objects.create(
            social_network='Twitter',
            link='https://www.twitter.com',
            logo=None,
            portfolio=self.portfolio_3
        )
        Contact.objects.create(
            social_network='Reddit',
            link='https://www.reddit.com',
            logo=None,
            portfolio=self.portfolio_3
        )

    def test_get_portfolio_without_auth(self):
        """
        Try to get portfolio without authorization
        :return: Portfolio with the corresponding link
        """
        resp = self.client.get(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}))
        portfolio = Portfolio.objects.get(pk=self.portfolio_1.pk)
        serializer = PortfolioSerializer(portfolio)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_portfolio_with_auth(self):
        """
        Try to get portfolio without authorization
        :return: Portfolio with the corresponding link
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.get(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}), **headers)
        portfolio = Portfolio.objects.get(pk=self.portfolio_1.pk)
        serializer = PortfolioSerializer(portfolio)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_portfolio_create_without_auth(self):
        """
        Try to create portfolio without authorization
        :return: 401 ERROR
        """
        data = {
            "header": "Created portfolio",
            "about_me": "Created portfolio about me.",
            "link": "created_portfolio2",
            "projects": [
                {
                    "name": "Created project 1",
                    "description": "Description of created project 1",
                    "project_link": "https://www.google.com"
                },
                {
                    "name": "Created project 2",
                    "description": "Description of created project 2",
                    "project_link": "https://www.google.com"
                }
            ],
            "contacts": [
                {
                    "social_network": "Created contact 1",
                    "link": "https://www.google.com"
                },
                {
                    "social_network": "Created contact 2",
                    "link": "https://www.github.com"
                }
            ]
        }
        resp = self.client.post(
            reverse('api_create_portfolio'),
            content_type='application/json',
            data=json.dumps(data)
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_portfolio_create_with_auth(self):
        """
        Try to create portfolio with authorized user
        :return: Status 201 CREATED
        """
        data = {
            "header": "Created portfolio",
            "about_me": "Created portfolio about me.",
            "link": "created_portfolio2",
            "projects": [
                {
                    "name": "Created project 1",
                    "description": "Description of created project 1",
                    "project_link": "https://www.google.com"
                },
                {
                    "name": "Created project 2",
                    "description": "Description of created project 2",
                    "project_link": "https://www.google.com"
                }
            ],
            "contacts": [
                {
                    "social_network": "Created contact 1",
                    "link": "https://www.google.com"
                },
                {
                    "social_network": "Created contact 2",
                    "link": "https://www.github.com"
                }
            ],
            "user": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.post(
            reverse('api_create_portfolio'),
            content_type='application/json',
            data=json.dumps(data),
            **headers
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_user_portfolio_with_auth(self):
        """
        Try to GET portfolio with authorized user
        :return: All portfolios of authorized user
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.get(reverse('api_user_portfolio'), **headers)
        portfolios = Portfolio.objects.filter(user=self.user_1)
        serializer = PortfolioSerializer(portfolios, many=True)
        self.assertEqual(serializer.data, resp.data)

    def test_get_user_portfolio_without_auth(self):
        """
        Try to get user portfolio without authorization
        :return: 401 ERROR
        """
        resp = self.client.get(reverse('api_user_portfolio'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_portfolio_without_auth(self):
        """
        Try to PATCH portfolio without authorization
        :return: 401 ERROR
        """
        data = {
            "id": 1,
            "header": "Updated portfolio",
            "about_me": "Updated portfolio about me.",
            "link": "created_portfolio2_upd",
            "projects": [
                {
                    "id": 1,
                    "name": "Updated project 1",
                    "description": "Description of updated project 1",
                    "project_link": "https://www.google.com"
                },
                {
                    "id": 2,
                    "name": "Updated project 2_upd",
                    "description": "Description of updated project 2",
                    "project_link": "https://www.google.com"
                }
            ],
            "contacts": [
                {
                    "id": 1,
                    "social_network": "Updated contact 1",
                    "link": "https://www.google.com"
                },
                {
                    "id": 2,
                    "social_network": "Updated contact 2",
                    "link": "https://www.github.com"
                }
            ]
        }
        resp = self.client.patch(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}),
                                 content_type='application/json',
                                 data=json.dumps(data))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_portfolio_with_other_user(self):
        """
        Change user in updated portfolio (user should not be changed)
        :return: Updated portfolio with not changed user
        """
        data = {
            "id": 1,
            "header": "Updated portfolio",
            "about_me": "Updated portfolio about me.",
            "link": "created_portfolio2_upd",
            "projects": [
                {
                    "id": 1,
                    "name": "Updated project 1",
                    "description": "Description of updated project 1",
                    "project_link": "https://www.google.com"
                },
                {
                    "id": 2,
                    "name": "Updated project 2",
                    "description": "Description of updated project 2",
                    "project_link": "https://www.google.com"
                }
            ],
            "contacts": [
                {
                    "id": 1,
                    "social_network": "Updated contact 1",
                    "link": "https://www.google.com"
                },
                {
                    "id": 2,
                    "social_network": "Updated contact 2",
                    "link": "https://www.github.com"
                }
            ],
            "user": 2
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers
                                 )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(resp.data["user"], data["user"])

    def test_patch_portfolio_with_auth(self):
        """
        PATCH portfolio of authorized user
        :return: Status 200 OK and Updated portfolio
        """
        data = {
            "id": 1,
            "image": None,
            "header": "Updated portfolio",
            "about_me": "Updated portfolio about me.",
            "link": "created_portfolio2_upd",
            "projects": [
                {
                    "id": 1,
                    "name": "Updated project 1",
                    "description": "Description of updated project 1",
                    "image": None,
                    "project_link": "https://www.google.com",
                    "portfolio": 1
                },
                {
                    "id": 2,
                    "name": "Updated project 2",
                    "description": "Description of updated project 2",
                    "image": None,
                    "project_link": "https://www.google.com",
                    "portfolio": 1
                }
            ],
            "contacts": [
                {
                    "id": 1,
                    "social_network": "Updated contact 1",
                    "link": "https://www.google.com",
                    "logo": None,
                    "portfolio": 1,
                },
                {
                    "id": 2,
                    "social_network": "Updated contact 2",
                    "link": "https://www.github.com",
                    "logo": None,
                    "portfolio": 1
                }
            ],
            "user": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers
                                 )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.dumps(resp.data), json.dumps(data))

    def test_patch_portfolio_other_user(self):
        """
        PATCH portfolio of other user
        :return: Status 403
        """
        data = {
            "id": 3,
            "header": "Updated portfolio",
            "about_me": "Updated portfolio about me.",
            "link": "created_portfolio2_upd",
            "projects": [
                {
                    "id": 5,
                    "name": "Updated project 1",
                    "description": "Description of updated project 1",
                    "project_link": "https://www.google.com"
                },
                {
                    "id": 6,
                    "name": "Updated project 2",
                    "description": "Description of updated project 2",
                    "project_link": "https://www.google.com"
                }
            ],
            "contacts": [
                {
                    "id": 5,
                    "social_network": "Updated contact 1",
                    "link": "https://www.google.com",
                },
                {
                    "id": 6,
                    "social_network": "Updated contact 2",
                    "link": "https://www.github.com",
                }
            ]
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_portfolio', kwargs={'link': self.portfolio_3.link}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers
                                 )

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_portfolio_without_auth(self):
        """
        Try to delete portfolio without authorization
        :return: Status 401
        """
        resp = self.client.delete(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_portfolio_with_auth(self):
        """
        Try to delete portfolio of authorized user
        :return: Status 204
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_portfolio', kwargs={'link': self.portfolio_1.link}),
                                  **headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_portfolio_other_user(self):
        """
        Try to delete portfolio of other user
        :return: Status 403
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_portfolio', kwargs={'link': self.portfolio_3.link}),
                                  **headers)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project_without_auth(self):
        """
        Try to create project without authorization
        :return: Status 401
        """
        data = {
            "name": "Created project",
            "description": "Description of created project",
            "portfolio": 1
        }
        resp = self.client.post(reverse('api_create_project'),
                                content_type='application/json',
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_other_user(self):
        """
        Try to create project to portfolio of other user
        :return: Status 400
        """
        data = {
            "name": "Created project",
            "description": "Description of created project",
            "project_link": "https://www.google.com",
            "portfolio": 3
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.post(reverse('api_create_project'),
                                content_type='application/json',
                                data=json.dumps(data),
                                **headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_with_auth(self):
        """
        Try to create project with auth
        :return: Status 201
        """
        data = {
            "name": "Created project",
            "description": "Description of created project",
            "project_link": "https://www.google.com",
            "portfolio": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.post(reverse('api_create_project'),
                                content_type='application/json',
                                data=json.dumps(data),
                                **headers)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_update_project_without_auth(self):
        """
        Try to update project without authentication
        :return: Status 401
        """
        data = {
            "id": 1,
            "name": "Updated project",
            "description": "Description of updated project",
            "project_link": "https://www.google.com",
        }
        resp = self.client.patch(reverse('api_update_project', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project_other_user(self):
        """
        Try to update project of other user
        :return: Status 403
        """
        data = {
            "name": "Updated project",
            "description": "Description of updated project"
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_project', kwargs={'pk': 5}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_portfolio_in_project(self):
        """
        Try to change portfolio in project
        :return: Status 400
        """
        data = {
            "name": "Updated project",
            "description": "Description of updated project",
            "portfolio": 3
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_project', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project_with_auth(self):
        """
        Try to update project with authorization
        :return: Status 200
        """
        data = {
            "name": "Updated project",
            "description": "Description of updated project"
        }
        returned_data = {
            "id": 1,
            "name": "Updated project",
            "description": "Description of updated project",
            "image": None,
            "project_link": "https://www.google.com",
            "portfolio": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_project', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(json.dumps(resp.data), json.dumps(returned_data))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_project_without_auth(self):
        """
        Try to delete project without authorization
        :return: Status 401
        """
        resp = self.client.delete(reverse('api_update_project', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_project_with_auth(self):
        """
        Try to delete project with authorization
        :return: Status 204
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_update_project', kwargs={'pk': 1}), **headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_other_user(self):
        """
        Try to delete project of other user
        :return: Status 403
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_update_project', kwargs={'pk': 5}), **headers)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_contact_without_auth(self):
        """
        Try to create contact without authorization
        :return: Status 401
        """
        data = {
            "social_network": "Created network",
            "link": "https://www.facebook.com",
            "logo": None,
            "portfolio": 1
        }
        resp = self.client.post(reverse('api_create_contact'),
                                content_type='application/json',
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contact_other_user(self):
        """
        Try to create contact to portfolio of other user
        :return: Status 400
        """
        data = {
            "social_network": "Created network",
            "link": "https://www.facebook.com",
            "logo": None,
            "portfolio": 3
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.post(reverse('api_create_contact'),
                                content_type='application/json',
                                data=json.dumps(data),
                                **headers)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_with_auth(self):
        """
        Try to create contact with authorization
        :return: Status 201
        """
        data = {
            "social_network": "Created network",
            "link": "https://www.facebook.com",
            "logo": None,
            "portfolio": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.post(reverse('api_create_contact'),
                                content_type='application/json',
                                data=json.dumps(data),
                                **headers)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_update_contact_without_auth(self):
        """
        Try to update contact without authentication
        :return: Status 401
        """
        data = {
            "social_network": "Updated network",
            "link": "https://www.facebook.com",
        }
        resp = self.client.patch(reverse('api_update_contact', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_contact_other_user(self):
        """
        Try to update contact of other user
        :return: Status 403
        """
        data = {
            "social_network": "Updated network",
            "link": "https://www.facebook.com",
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_contact', kwargs={'pk': 5}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_portfolio_in_contact(self):
        """
        Try to change portfolio in contact
        :return: Status 400
        """
        data = {
            "social_network": "Updated network",
            "link": "https://www.facebook.com",
            "portfolio": 3
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_contact', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_contact_with_auth(self):
        """
        Try to update contact with authentication
        :return: Status 200
        """
        data = {
            "social_network": "Updated network",
            "link": "https://www.facebook.com",
        }
        returned_data = {
            "id": 1,
            "social_network": "Updated network",
            "link": "https://www.facebook.com",
            "logo": None,
            "portfolio": 1
        }
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.patch(reverse('api_update_contact', kwargs={'pk': 1}),
                                 content_type='application/json',
                                 data=json.dumps(data),
                                 **headers)

        self.assertEqual(json.dumps(resp.data), json.dumps(returned_data))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_contact_without_auth(self):
        """
        Try to delete contact without authorization
        :return: Status 401
        """
        resp = self.client.delete(reverse('api_update_contact', kwargs={'pk': 1}))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_contact_with_auth(self):
        """
        Try to delete contact with authorization
        :return: Status 204
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_update_contact', kwargs={'pk': 1}), **headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_contact_other_user(self):
        """
        Try to delete contact of other user
        :return: Status 403
        """
        headers = {"HTTP_AUTHORIZATION": "JWT " + self.user1_token}
        resp = self.client.delete(reverse('api_update_contact', kwargs={'pk': 5}), **headers)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
