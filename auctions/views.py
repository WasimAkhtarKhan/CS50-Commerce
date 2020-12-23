from django.contrib.auth import authenticate , login, logout 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Bid,Listing,Comment,Watchlist,Closedbid,Alllisting
from datetime import datetime



def create(request):
    return render(request,"auctions/create.html")

def submit(request):
    if request.method == "POST":
        listtable = Listing()
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        listtable.owner = request.user.username
        listtable.title = request.POST.get('title')
        listtable.description = request.POST.get('description')
        listtable.basebid = request.POST.get('basebid')
        listtable.currentbid = request.POST.get('basebid')
        listtable.category = request.POST.get('category')
        if request.POST.get('imglink'):
            listtable.imglink = request.POST.get('imglink')
        else :
            listtable.imglink = "https://i.pinimg.com/originals/a8/f0/46/a8f0466ce216b13a730e4ef6d4279e90.jpg"
        listtable.time = dt
        listtable.save()
        all = Alllisting()
        items = Listing.objects.all()
        
        for i in items:
            try:
                if Alllisting.objects.get(listingid=i.id):
                    pass
            except:
                all.listingid=i.id
                all.title = i.title
                all.description = i.description
                all.link = i.imglink
                all.save()
        
        return redirect('index')
    else:
        return redirect('index')


def index(request):
    items=Listing.objects.all()
    
    try:
        w = Watchlist.objects.filter(user=request.user.username)
    except:
        pass

    return render(request, "auctions/index.html",{
        "items":items,
    })



def listingpage(request,id):
    try:
        item = Listing.objects.get(id=id)
    except:
        return redirect('index')
    
    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None
    
    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username,listingid=id):
                added=True
        except:
            added = False
        try:
            l = Listing.objects.get(id=id)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False
    
    return render(request,"auctions/listingpage.html",{
        "i":item,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "comments":comments,
        "added":added,
        "owner":owner,
        
    })


def bidsubmit(request,listingid):
    current_bid = Listing.objects.get(id=listingid)
    current_bid1=current_bid.currentbid 
    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))
        if user_bid > current_bid1:
            listing_items = Listing.objects.get(id=listingid)
            listing_items.currentbid = user_bid
            listing_items.save()
            try:
                if Bid.objects.filter(listingid=listingid):
                    bidrow = Bid.objects.filter(listingid=listingid)
                    bidrow.delete()
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.listingid = listingid
                bidtable.currentbid = user_bid
                bidtable.save()
                
            except:
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.listingid = listingid
                bidtable.currentbid = user_bid
                bidtable.save()
            response = redirect('listingpage',id=listingid)
            response.set_cookie('errorgreen','You Bidded!!!',max_age=3)
            return response
        else :
            response = redirect('listingpage',id=listingid)
            response.set_cookie('error','Your Bid is less than Current Bid',max_age=3)
            return response
    else:
        return redirect('index')

def closebid(request,listingid):
    if request.user.username:
        try:
            listingrow = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        cb = Closedbid()
        title = listingrow.title
        cb.owner = listingrow.owner
        cb.listingid = listingid
        '''
        try:
        '''    
        bidrow = Bid.objects.get(listingid=listingid,currentbid=listingrow.currentbid)
        cb.winner = bidrow.user
        cb.winprice = bidrow.currentbid
        cb.save()
        bidrow.delete()
        '''    
        except:
            
            cb.winner = listingrow.owner
            cb.winprice = listingrow.currentbid
            cb.save()
            
            pass
        '''
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watchrow = Watchlist.objects.filter(listingid=listingid)
                watchrow.delete()
            else:
                pass
        except:
            pass
        
        try:
            crow = Comment.objects.filter(listingid=listingid)
            crow.delete()
        except:
            pass
        '''
        try:
            brow = Bid.objects.filter(listingid=listingid)
            brow.delete()
        except:
            pass
        '''

        '''
        try:
            cblist=Closedbid.objects.get(listingid=listingid)
        except:
            cb.owner = listingrow.owner
            cb.winner = bidrow.user
            cb.listingid = listingid
            cb.winprice = listingrow.currentbid
            cb.save()
            cblist=Closedbid.objects.get(listingid=listingid)
        '''
        cblist=Closedbid.objects.get(listingid=listingid)
        listingrow.delete()
        
        return render(request,"auctions/winningpage.html",{
            "cb":cblist,
            "title":title,
        })   

    else:
        return redirect('index')     


def cmntsubmit(request,listingid):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listingid = listingid
        c.save()
        return redirect('listingpage',id=listingid)
    else :
        return redirect('index')


def mywinnings(request):
    if request.user.username:
        items=[]
        try:
            wonitems = Closedbid.objects.filter(winner=request.user.username)
            for w in wonitems:
                items.append(Alllisting.objects.filter(listingid=w.listingid))
        except:
            wonitems = None
            items = None
        try:
            w = Watchlist.objects.filter(user=request.user.username)
        except:
            pass
        return render(request,'auctions/mywinnings.html',{
            "items":items,
            "wonitems":wonitems
        })
    else:
        return redirect('index')



def addwatchlist(request,listingid):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listingid = listingid
        w.save()
        return redirect('listingpage',id=listingid)
    else:
        return redirect('index')


def removewatchlist(request,listingid):
    if request.user.username:
        try:
            w = Watchlist.objects.get(user=request.user.username,listingid=listingid)
            w.delete()
            return redirect('listingpage',id=listingid)
        except:
            return redirect('listingpage',id=listingid)
    else:
        return redirect('index')


def watchlistpage(request,username):
    if request.user.username:
        try:
            w = Watchlist.objects.filter(user=username)
            items = []
            for i in w:
                items.append(Listing.objects.filter(id=i.listingid))
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                
            except:
                pass
                
            return render(request,"auctions/watchlistpage.html",{
                "items":items,
                
            })
        except:
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                
            except:
                pass
            return render(request,"auctions/watchlistpage.html",{
                "items":None,
                
            })
    else:
        return redirect('index')

def categories(request):
    items=Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
    
    return render(request,"auctions/categpage.html",{
        "items": items,
    })

def category(request,category):
    catitems = Listing.objects.filter(category=category)
    
    return render(request,"auctions/category.html",{
        "items":catitems,
        "cat":category,
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
