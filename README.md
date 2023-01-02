# web50-projects-2020-x-commerce

Introduction
This Django project is an online auction platform that allows users to create, list, and bid on auctions for various items.

Features

User registration and authentication
Creating, viewing, and closing auctions
Placing bids on auctions
Adding auctions to a watchlist
Commenting on auctions
Setup

Install Django using pip install django

Clone this repository and navigate to the root directory
Run the command python manage.py runserver to start the server
Navigate to http://127.0.0.1:8000/ in your web browser to view the app

File Structure

auctions/ - Django app containing the core functionality of the project
auctions/templates/auctions/ - HTML templates for the app
auctions/static/auctions/css - CSS files for styling the app
auctions/views.py - Contains the functions that handle requests and render templates
auctions/models.py - Contains the Django models for the app
db.sqlite3 - SQLite database file
manage.py - Django command-line utility for interacting with the project

Models

The app uses the following Django models:

Listing - Stores data for an auction listing, including the name, description, owner, current bid, and whether the auction is active or closed.
Category - Stores data for a category that a listing can belong to.
Bid - Stores data for a bid on a listing, including the bidder and the amount of the bid.
Comment - Stores data for a comment on a listing, including the commenter and the comment text.

Views

The app has the following views:

index - Renders the homepage with a list of all active auctions and all categories.
closedDetails - Renders the details page for a specific closed auction.
closed_listings - Renders the closed auctions page with a list of all closed auctions.
closeAuction - Closes an active auction and renders the updated details page for the auction.
removeWatchList - Removes an auction from the current user's watchlist and redirects to the auction details page.
addWatchList - Adds an auction to the current user's watchlist and redirects to the auction details page.
createListing - Renders the form for creating a new auction and saves the new auction to the database if the form is submitted.
listing - Renders the details page for an active auction.
watchlist - Renders the watchlist page with a list of all auctions in the current user's watchlist.
bid - Processes a bid on an active auction and renders the updated auction details page.
comment - Saves a comment on an auction and renders the updated auction details page.

Template Inheritance

The app uses Django's template inheritance feature, which allows templates to extend a base template and override specific blocks of content. The base template is base.html, which contains the HTML structure and common elements for all pages in the app. The other templates extend base.html and override the content block to add specific content for each page.
