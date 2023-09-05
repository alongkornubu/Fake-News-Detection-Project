from django.core.management.base import BaseCommand
import csv
from news.models import *

# import pandas
# t = pandas.read_csv('data/Data-covid.csv')
# print(t)

class Command(BaseCommand):
    help=('import news from a local csv file')
    
    def handle(self, *args, **options):
        # csv_file = options['Data_news.csv']
        
        with open('data/Data.csv',encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) 
            
            News.objects.all().create()
            for row in reader:
                category,created  = Category.objects.get_or_create(name=row[3])
                news = News(title=row[0] , 
                        text=row[1] ,
                        label=row[2] ,
                        # category=row[3],
                        category=category
                        )
                # print(news)
                news.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully csv2db ')) 
    
