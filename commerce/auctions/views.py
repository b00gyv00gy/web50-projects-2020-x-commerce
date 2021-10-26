from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Watchlist, Category

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

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

    form = CategoryForm(request.POST)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST['starting_bid']
        imgURL = request.POST["imgURL"]
        creator = request.user
        last_bidder = request.user
        if form.is_valid():
            category = form.cleaned_data['category']
        
        try:
            listing = Listing(title=title, description=description, bid=bid, imgURL=imgURL, creator=creator, category=category)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "smth is wrong"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html",{
        "form": form
    })

def listing_page(request, title):
    
    watchlist_button_message = None
    closed_auction_message = None
    listing = get_object_or_404(Listing, title=title)
    required_min_bid = listing.bid + 1
    is_creator = False
    comments = Comment.objects.filter(listing=listing)

    if request.user.is_authenticated:

        is_on_watchlist = Watchlist.objects.filter(listing=listing, user=request.user).exists()
        
        if is_on_watchlist:
            watchlist_button_message = "Remove from watchlist"
        else:
            watchlist_button_message = "Add to watchlist"    

        if request.method == "POST":
            
            if "watchlist" in request.POST:
            
                try:
                    entry = Watchlist(listing=listing, user=request.user)
                    entry.save()
                    watchlist_button_message = "Added to watchlist"
            
                except IntegrityError:
                    pass
            
                if is_on_watchlist:
                    Watchlist.objects.filter(listing=listing, user=request.user).delete()
                    watchlist_button_message = "Removed from watchlist"
            
            if "bid" in request.POST:
                
                if request.POST["bid_value"]:

                    bid = float(request.POST["bid_value"])
                
                    if bid > listing.bid:
                        listing.bid = bid
                        listing.last_bidder = request.user
                        listing.save()
                        required_min_bid = bid + 1
            
            if "comment" in request.POST:
                
                #if request.POST["comment"]:

                    comment = Comment(comment=request.POST["content"], listing=listing, user=request.user)
                    comment.save()
        
        if request.user == listing.creator:
            is_creator = True

            if request.method == "POST":
            
                if "close_listing" in request.POST:
                    listing.status = False
                    listing.save()
            
        if listing.status == False:
            
            closed_auction_message = "Auction is closed"

            if  request.user == listing.last_bidder:
                closed_auction_message = "Auction is closed. You are the winner."      

    return render(request, "auctions/listing_page.html",{
        "listing": listing,
        "watchlist_button_message": watchlist_button_message,
        "required_min_bid": required_min_bid,
        "is_creator": is_creator,
        "closed_auction_message": closed_auction_message,
        "comments": comments
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "watchlists": Watchlist.objects.filter(user=request.user)
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": Category.objects.all()
    })

def active_listings_in_category(request, title):
    
    category = get_object_or_404(Category, name=title)
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/index.html",{
        "listings": listings
    })
        
