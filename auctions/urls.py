# Import the path function from Django's URLconf module
from django.urls import path

# Import the views defined in the auctions app
from . import views

# Define the URL patterns for the auctions app
urlpatterns = [
    # The root URL maps to the index view
    path("", views.index, name="index"),
    # URL for the login view
    path("login", views.login_view, name="login"),
    # URL for the logout view
    path("logout", views.logout_view, name="logout"),
    # URL for the register view
    path("register", views.register, name="register"),
    # URL for the create listing view
    path("create", views.create_listing, name="create"),
    # URL for the view to display listings in a selected category
    path("displayCategory", views.displayCategory, name="displayCategory"),
    # URL for the listing detail view
    path("listing/<int:id>", views.listing, name="listing"),
    # URL for the view to remove a listing from the user's watchlist
    path("removeWatchList/<int:id>", views.removeWatchList, name="removeWatchList"),
    # URL for the view to add a listing to the user's watchlist
    path("addWatchList/<int:id>", views.addWatchList, name="addWatchList"),
    # URL for the view to display the user's watchlist
    path("watchlist", views.displayWatchList, name="watchlist"),
    # URL for the view to add a comment to a listing
    path("addComment/<int:id>", views.addComment, name="addComment"),
    # URL for the view to add a bid to a listing
    path("addBid/<int:id>", views.addBid, name="addBid"),
    # URL for the view to close an auction and select a winner
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("closedDetails/<int:id>", views.closedDetails, name="closedDetails")
]
