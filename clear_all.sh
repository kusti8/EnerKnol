curl -XDELETE 'localhost:9200/movies?pretty'
mongo --eval "db.getSiblingDB('movies').dropDatabase()"