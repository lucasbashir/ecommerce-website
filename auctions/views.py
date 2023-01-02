from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import *


# This function handles the rendering of the index page with all active listings and categories
def index(request):
    # Get all active listings
    activeListings = Listing.objects.filter(isActive=True)
    # Get all categories
    allCategories = Category.objects.all()
    # Render the index page with the active listings and categories
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "category": allCategories
    })

def closedDetails(request, id):
    """
    Handles the rendering of the details page for a specific listing.
    Parameters:
        request: HTTP request object
        id: primary key of the listing in the database
    Returns:
        An HTTP response with the listing page rendered
    """
    # Get the listing data from the database using the provided primary key
    listingData = Listing.objects.get(pk=id)
    
    # Check if the current user is in the watchlist of the listing
    isListingInWatchList = request.user in listingData.watchlist.all()
    
    # Get all comments for the current listing
    allComments = Comment.objects.filter(listing=listingData)
    
    # Check if the current user is the owner of the listing
    isOwner = request.user.username == listingData.owner.username
    
    # Render the listing page with the relevant data
    return render(request, "auctions/closedDetails.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "isOwner": isOwner
    })

def closed_listings(request):
    closed_listing = Listing.objects.filter(isActive=False)
    context = {
        "listings": closed_listing,
    }
    return render(request, "auctions/closedListing.html", context)

# This function handles the closing of a listing and rendering the updated listing page
def closeAuction(request, id):
    # Get the listing data for the given id
    listingData = Listing.objects.get(pk=id)
    # Set the listing to inactive
    listingData.isActive = False
    # Save the updated listing data
    listingData.save()
    # Check if the user who requested to close the auction is the owner of the listing
    isOwner = request.user.username == listingData.owner.username
    # Check if the listing is in the current user's watchlist
    isListingInWatchList = request.user in listingData.watchlist.all()
    # Get all comments for the listing
    allComments = Comment.objects.filter(listing=listingData)
    # Render the updated listing page
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Close Successful"
    })

# This function handles the removal of a listing from the current user's watchlist
def removeWatchList(request, id):
    # Get the listing data for the given id
    listingData = Listing.objects.get(pk=id)
    # Get the current user
    currentUser = request.user
    # Remove the current user from the listing's watchlist
    listingData.watchlist.remove(currentUser)
    # Redirect to the listing page
    return HttpResponseRedirect(reverse("listing",args=(id, )))

# This function handles the addition of a listing to the current user's watchlist
def addWatchList(request, id):
    # Get the listing data for the given id
    listingData = Listing.objects.get(pk=id)
    # Get the current user
    currentUser = request.user
    # Add the current user to the listing's watchlist
    listingData.watchlist.add(currentUser)
    
    # Redirect to the listing page
    return HttpResponseRedirect(reverse("listing",args=(id, )))

# This function is responsible for displaying the watchlist page for the user
def displayWatchList(request):
    # Get the current user making the request
    currentUser = request.user
    # Get all the listings that are in the user's watchlist
    listings = currentUser.listingWatchlist.all()
    # Render the watchlist page, passing in the listings to display
    return render(request, "auctions/watchlist.html", {
        "listings": listings
        
    })

# This function is responsible for adding a new bid to a listing
def addBid(request, id):
    # Get the new bid amount from the request
    newBid = request.POST['newBid']
    # Get the listing data for the given id
    listingData = Listing.objects.get(pk=id)
    # Check if the current user is the owner of the listing
    isOwner = request.user.username == listingData.owner.username
    # If the new bid is higher than the current highest bid, update the bid
    if int(newBid) > listingData.price.bid:
        # Create a new bid object with the user and bid amount
        updateBid = Bid(user=request.user, bid=int(newBid))
        # Save the bid to the database
        updateBid.save()
        # Update the listing with the new highest bid
        listingData.price = updateBid
        listingData.save()
        # Render the listing page with a success message
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid Successful",
            "update": True,
            "isOwner": isOwner
        })
    else:
        # Render the listing page with a failure message
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid failed",
            "update": False,
            "isOwner": isOwner
        }) 
    
# This function is responsible for adding a new comment to a listing
def addComment(request, id):
    # Get the current user making the request
    currentUser = request.user
    # Get the listing data for the given id
    listingData = Listing.objects.get(pk=id)
    # Get the message for the new comment from the request
    message = request.POST["newComment"]

    # Create a new comment object with the author, listing, and message
    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )
    # Save the comment to the database
    newComment.save()
    # Redirect the user back to the listing page
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def listing(request, id):
    """
    Handles the rendering of the details page for a specific listing.
    Parameters:
        request: HTTP request object
        id: primary key of the listing in the database
    Returns:
        An HTTP response with the listing page rendered
    """
    # Get the listing data from the database using the provided primary key
    listingData = Listing.objects.get(pk=id)
    
    # Check if the current user is in the watchlist of the listing
    isListingInWatchList = request.user in listingData.watchlist.all()
    
    # Get all comments for the current listing
    allComments = Comment.objects.filter(listing=listingData)
    
    # Check if the current user is the owner of the listing
    isOwner = request.user.username == listingData.owner.username
    
    # Render the listing page with the relevant data
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner
    })


def create_listing(request):
    """
    Handles the creation of a new listing.
    Parameters:
        request: HTTP request object
    Returns:
        An HTTP response with the index page rendered
    """
    # If the request method is GET, render the create listing page with a list of all categories
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "category": allCategories
        })
    # If the request method is POST, create a new listing with the provided data
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = request.POST["category"]
        currentUser = request.user
        
        # Get the category data from the database using the provided category name
        categoryData = Category.objects.get(categoryName=category)
        
        # Create a new bid with the provided data and save it to the database
        bid = Bid(bid=float(price), user=currentUser)
        bid.save()
        
        # Create a new listing with the provided data and save it to the database
        newListing = Listing(
            title = title,
            description = description,
            imageUrl = imageUrl,
            price = bid,
            category = categoryData,
            owner = currentUser,
        )
        
        newListing.save()
        
        # Redirect to the index page
        return HttpResponseRedirect(reverse(index))

def displayCategory(request):
    """
    Handles displaying items in a specific category.
    """
    if request.method == "POST":
        # Get the category selected by the user
        formCategory = request.POST["category"]
        category = Category.objects.get(categoryName=formCategory)
        
        # Get all active listings in the selected category
        activeListings = Listing.objects.filter(isActive=True, category=category)
        
        # Get all categories to display in the sidebar
        allCategories = Category.objects.all()
        
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "category": allCategories
        })


def login_view(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

