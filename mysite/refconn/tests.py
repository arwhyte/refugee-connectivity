from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import Camp


class IndexViewTest(TestCase):

	def test_view_route_redirection(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/refconn/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_name(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'refconn/home.html')


class AboutViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/refconn/about/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/about/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'refconn/about.html')


# class CampModelTest(TestCase):

	# def setUp(self):
	# 	CampAdmin.objects.create(camp_admin_name='Military')
	# 	admin = CampAdmin.objects.get(pk=1)
	# 	Camp.objects.create(
	# 		# TODO restore missing properties and values
	# 		camp_name='Cultural Landscape and Archaeological Remains of the Bamiyan Valley',
	# 		heritage_site_category_id=category.category_id,
	# 		description='The cultural landscape and archaeological remains ...',
	# 		justification='The Buddha statues and the cave art in Bamiyan Valley are ...',
	# 		date_inscribed='2003',
	# 		longitude='67.82525000',
	# 		latitude='34.84694000',
	# 		area_hectares='158.9265',
	# 		transboundary=0)

	# def test_camp_name(self):
	# 	camp = Camp.objects.get(pk=1)
	# 	expected_object_name = f'{camp.camp_name}'
	# 	self.assertEqual(expected_object_name, 'Alexandria')


class CampListViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/refconn/camps/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/camps/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('camps'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('camps'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'refconn/camps.html')
