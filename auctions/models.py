from django.contrib.auth.models import AbstractUser
from django.db import models


# This class extends Django's built-in AbstractUser model
# and adds no additional functionality
class User(AbstractUser):
    pass

# This class defines a Category model with a single CharField
# to store the category name
class Category(models.Model):
    # CharField to store the name of the category
    # with a max length of 50 characters
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        # Returns the category name when the object is printed
        return self.categoryName

# This class defines a Bid model with a single FloatField
# to store the bid amount
class Bid(models.Model):
    # FloatField to store the bid amount
    # with a default value of 0
    bid = models.FloatField(default=0)
    # ForeignKey to a User object, with the option to delete the object
    # if the user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Userbid")
    

# This class defines a Listing model with several fields:
# - CharField for the listing title (max length of 100 characters)
# - CharField for the listing description (max length of 1000 characters)
# - CharField for the listing image URL (max length of 200 characters)
# - ForeignKey to a Bid object to store the price of the listing
# - BooleanField to store whether the listing is active or not
# - ForeignKey to a User object to store the owner of the listing
# - ForeignKey to a Category object to store the category of the listing
# - ManyToManyField to a User object to store the users who have added the listing to their watchlist
class Listing(models.Model):
    # CharField to store the listing title
    # with a max length of 100 characters
    title = models.CharField(max_length=100)
    # CharField to store the listing description
    # with a max length of 1000 characters
    description = models.CharField(max_length=1000)
    # CharField to store the URL of the listing's image
    # with a max length of 200 characters
    imageUrl = models.CharField(max_length=200)
    # ForeignKey to a Bid object to store the price of the listing
    # with the option to delete the object if the bid is deleted
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    # BooleanField to store whether the listing is active or not
    # with a default value of True
    isActive = models.BooleanField(default=True)
    # ForeignKey to a User object to store the owner of the listing
    # with the option to delete the object if the user is deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    # ForeignKey to a Category object to store the category of the listing
    # with the option to delete the object if the category is deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    # ManyToManyField to a User object to store the users who have added the listing to their watchlist
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
     
    def __str__(self):
        # Returns the title of the listing when the object is printed
        return self.title

# This class defines a Comment model with three fields:
# - ForeignKey to a User object to store the author of the comment
# - ForeignKey to a Listing object to store the listing that the comment is for
# - CharField to store the message of the comment (max length of 500 characters)
class Comment(models.Model):
    # ForeignKey to a User object to store the author of the comment
    # with the option to delete the object if the user is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    # ForeignKey to a Listing object to store the listing that the comment is for
    # with the option to delete the object if the listing is deleted
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    # CharField to store the message of the comment
    # with a max length of 500 characters
    message = models.CharField(max_length=500)

    def __str__(self):
        # Returns a string representation of the comment in the form:
        # "{author} commented on {listing}"
        f"{self.author} commented on {self.listing}"



