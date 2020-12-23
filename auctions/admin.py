from django.contrib import admin
from . models import Listing,Bid,Comment,Watchlist,Closedbid,Alllisting,User

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Closedbid)
admin.site.register(Alllisting)
admin.site.register(User)