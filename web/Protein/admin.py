from django.contrib import admin
from Protein.models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('user_name','email','comment','testfile','date_time')
    def download_csv(self,request,queryset):
        import csv
        from django.http import HttpResponse
        f = open('data.csv','wb')
        writer = csv.writer(f)
        writer.writerow(['user_name','email','comment','testfile','date_time'])
        for s in queryset:
          writer.writerow([s.user_name,s.email,s.comment,s.testfile,s.date_time])
        f.close()

        f = open('data.csv','r')
        response = HttpResponse(f,content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=stat-info.csv'
        return response
    download_csv.short_description='Download CSV file for selected stats.'
admin.site.register(Profile,ProfileAdmin)
