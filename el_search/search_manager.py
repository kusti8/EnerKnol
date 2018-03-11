from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Integer, Keyword, Text, Search, Boolean
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.utils import AttrList
from mongoengine import *
import os


class MovieItem(DocType):
    title = Text()
    year = Text()
    directors = Text()
    genres = Keyword()
    stars = Text()
    description = Text()
    mpaa_rating = Text()
    imdb_rating = Integer()
    metascore = Integer()
    image = Text()

    class Meta:
        index = 'movies'

class MovieItemDB(Document):
    title = StringField()
    year = StringField()
    directors = ListField(StringField())
    genres = ListField(StringField())
    stars = ListField(StringField())
    description = StringField()
    mpaa_rating = StringField()
    imdb_rating = IntField()
    metascore = IntField()
    image = StringField()

class MovieItemManager():
    def __init__(self):
        connections.create_connection(hosts=[os.environ['ELASTIC_URL']])
        connect('movies', host="ds263988.mlab.com", port=63988, username=os.environ['MONGO_USERNAME'], password=os.environ['MONGO_PASSWORD'])

    def copy_attributes(self, old, new):
        attributes = ['title', 'year', 'directors', 'genres', 'stars', 'description', 'mpaa_rating', 'imdb_rating', 'metascore', 'image']
        for att in attributes:
            if type(getattr(old, att)) is AttrList:
                a = list(getattr(old, att)) # ElasticSearch_DSL uses a special type of list
            else:
                a = getattr(old, att)
            setattr(new, att, a)
        return new

    def add(self, movie_info): # Add a movie item. Expects a MovieItem type
        movie_info_db = MovieItemDB()
        movie_info_db = self.copy_attributes(movie_info, movie_info_db)

        movie_info_db.save()
        movie_info._id = movie_info_db.id # Sync the IDs
        movie_info.save()

    def search(self, general, filters=None, page=1, PAGE_SIZE=5): # Search, using pagination
        search_fields = ['title', 'directors', 'stars', 'description']
        if filters:
            pass

        results = MovieItem.search().query('multi_match', query=general, fields=search_fields)
        min_range = (page-1)*PAGE_SIZE
        max_range = page*PAGE_SIZE
        results = results[min_range:max_range].execute()
        return results

    def get_movie(self, i): # Return a movie from MongoDB
        results = MovieItemDB.objects(id=i)
        if results:
            return results[0].to_mongo().to_dict()
        else:
            return None
        

if __name__ == '__main__': # Need to create Elasticsearch mappings
    connections.create_connection(hosts=[os.environ['ELASTIC_URL']])
    MovieItem.init()