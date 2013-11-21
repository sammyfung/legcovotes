from django.contrib import admin
from legcovotes.models import Vote, IndividualVote

admin.site.register(Vote)
admin.site.register(IndividualVote)
