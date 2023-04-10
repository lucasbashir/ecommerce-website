from django.test import TestCase
from auctions.models import User 
from .models import Category, Bid, Listing, Comment

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a User object
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a Category object
        self.category = Category.objects.create(categoryName='Test Category')
        # Create a Bid object
        self.bid = Bid.objects.create(bid=10.0, user=self.user)
        # Create a Listing object
        self.listing = Listing.objects.create(title='Test Listing', description='Test Description', price=self.bid,
                                             owner=self.user, category=self.category)
        # Create a Comment object
        self.comment = Comment.objects.create(author=self.user, listing=self.listing, message='Test Comment')

    def test_user_model(self):
        # Test User model fields
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))

    def test_category_model(self):
        # Test Category model fields
        self.assertEqual(self.category.categoryName, 'Test Category')

    def test_bid_model(self):
        # Test Bid model fields
        self.assertEqual(self.bid.bid, 10.0)
        self.assertEqual(self.bid.user, self.user)

    def test_listing_model(self):
        # Test Listing model fields
        self.assertEqual(self.listing.title, 'Test Listing')
        self.assertEqual(self.listing.description, 'Test Description')
        self.assertEqual(self.listing.price, self.bid)
        self.assertEqual(self.listing.owner, self.user)
        self.assertEqual(self.listing.category, self.category)

    def test_comment_model(self):
        # Test Comment model fields
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.listing, self.listing)
        self.assertEqual(self.comment.message, 'Test Comment')


class ViewTestCase(TestCase):
    def setUp(self):
        # Create a User object
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a Category object
        self.category = Category.objects.create(categoryName='Test Category')
        # Create a Bid object
        self.bid = Bid.objects.create(bid=10.0, user=self.user)
        # Create a Listing object
        self.listing = Listing.objects.create(title='Test Listing', description='Test Description', price=self.bid,
                                             owner=self.user, category=self.category)
        # Create a Comment object
        self.comment = Comment.objects.create(author=self.user, listing=self.listing, message='Test Comment')

    def test_listing_detail_view(self):
        response = self.client.get('/listing/2/')  # Replace with the appropriate URL for your view
        self.assertEqual(response.status_code, 200)  # Replace with the appropriate status code for your view
        self.assertContains(response, 'Test Listing')  # Replace with the appropriate content for your view

    def test_listing_create_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/listing/create/', {'title': 'New Listing',
                                                         'description': 'New Description',
                                                         'price': 20.0,
                                                         'owner': self.user.pk,
                                                         'category': self.category.pk})  # Replace with the appropriate URL for your view and form data
        self.assertEqual(response.status_code, 200)  # Replace with the appropriate status code for your view
        self.assertTrue(Listing.objects.filter(title='New Listing').exists())
