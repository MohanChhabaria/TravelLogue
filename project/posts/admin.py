from django.contrib import admin
from .models import Media, Iternary, Destination, Accomodation

@admin.register(Iternary)
class IternaryAdmin(admin.ModelAdmin):
    readonly_fields = ['registration_timestamp', ]
    list_display = ['__str__', 'travellor', 'no_of_days', 'expenditure', 'registration_timestamp']
    list_filter = ['travellor__profile_name', 'expenditure', ]
    ordering = ['no_of_days',"expenditure" ]
    search_fields = ['travellor__profile_name', 'title',]

    class Meta:
        model = Iternary
        fields = '__all__'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ['name', 'get_name']
    list_filter = ['name', 'iternary__travellor__profile_name']
    search_fields = ["name"]

    class Meta:
        model = Destination
        fields= "__all__"

    def get_name(self, obj):
        return obj.iternary.title
    get_name.admin_short_description = "title"


@admin.register(Accomodation)
class AccomodationAdmin(admin.ModelAdmin):
    readonly_fields = []
    list_display = ["property_name", "price", "get_name"]
    list_filter = ["property_name", "destination__name"]
    search_fields = ["property_name", "destination__name"]

    def get_name(self, obj):
        return obj.destination.name
    get_name.admin_short_description = "place"

    class Meta:
        model = Accomodation
        fields = "__all__"

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["title", "uploaded_at"]
    ordering = ["uploaded_at"]
    
    class Meta:
        model = Media
        fields = "__all__"

