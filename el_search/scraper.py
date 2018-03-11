from requests import get
from search_manager import MovieItem, MovieItemManager
from bs4 import BeautifulSoup
import base64

def get_directors(s):
    directors = []
    stars = []
    reached_line = False
    for i in s:
        if i.text.strip() == '|': # We reached the director/star separator
            reached_line = True
            continue
        if reached_line: # We are onto stars now
            stars.append(i.text.strip())
        else:
            directors.append(i.text.strip())
        
    if not reached_line: # We never reached the line, which means that we never had a director
        stars = directors[:]
        directors = []
    return (directors, stars)

items = []
years = range(1940, 2019)
pages = range(1, 5)

manager = MovieItemManager()

for year in years:
    for page in pages:
        response = get('http://www.imdb.com/search/title?release_date=' + str(year) + 
        '&sort=num_votes,desc&page=' + str(page))

        if response.status_code != 200:
            print 'Error on {} {}, status: {}'.format(year, page, response.status_code)

        html = BeautifulSoup(response.text, 'html.parser')

        movies = html.find_all('div', class_ = 'lister-item mode-advanced')

        for movie in movies:
            movie_info = MovieItem()
            title =  movie.h3.a.text.strip()
            if len(movie.h3.find_all('a')) == 2: # TV show episode
                title += ' Episode: ' + movie.h3.find_all('a')[1].text.strip()
            movie_info.title = title
            movie_info.year = movie.h3.find('span', class_ = 'lister-item-year').text.strip()
            movie_info.imdb_rating = int(float(movie.strong.text.strip())*10)
            metascore = movie.find('span', class_ = 'metascore')
            if metascore:
                movie_info.metascore = int(metascore.text.strip())
            mpaa_rating = movie.find('span', class_='certificate')
            if mpaa_rating:
                movie_info.mpaa_rating = mpaa_rating.text.strip()
            genres = movie.find('span', class_='genre')
            if genres:
                movie_info.genres = genres.text.strip().split(', ')
            movie_info.description = movie.find_all('p', class_='text-muted')[-1].contents[0].strip()
            movie_info.directors, movie_info.stars = get_directors(movie.find_all('p', class_='')[-1].find_all(['a', 'span']))

            movie_info.image = movie.find('img')['loadlate']

            manager.add(movie_info)
    print year