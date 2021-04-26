from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Watchlist

def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })


def login_view(request):
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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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

def create_listing(request):

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        imgURL = request.POST["imgURL"]
        creator = request.user
        try:
            listing = Listing(title=title, description=description, bid=bid, imgURL=imgURL, creator=creator)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "smth is wrong"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

def listing_page(request, title):
    
    message = None
    listing = Listing.objects.get(title=title)
    
    is_on_watchlist = Watchlist.objects.filter(listing=listing, user=request.user).exists()
    
    if is_on_watchlist:
        message = "Remove from watchlist"
    else:
        message = "Add to watchlist"    

    if request.method == "POST":
        
        if "watchlist" in request.POST:
        
            try:
                entry = Watchlist(listing=listing, user=request.user)
                entry.save()
                message = "Added to watchlist"
        
            except IntegrityError:
                pass
        
            if is_on_watchlist:
                Watchlist.objects.filter(listing=listing, user=request.user).delete()
                message = "Removed from watchlist"
        
        if "bid" in request.POST:
        
            listing.bid = request.POST["bid_value"]
            listing.last_bidder = request.user
    
    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "message": message,
        "current_bid": listing.bid
    })
    
