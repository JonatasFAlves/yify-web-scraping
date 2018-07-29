import requests
from bs4 import BeautifulSoup


# Get the imdb rating and count in the yify detail page
def get_imdb_rating(yify_detail_url):
    response = requests.get(yify_detail_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rating_div = soup.find('div', class_='rating-row', itemprop='aggregateRating')
    rating = rating_div.find('span', itemprop='ratingValue')
    rating_count = rating_div.find('span', itemprop='ratingCount')
    return [rating.string, rating_count.string]
    
# IMDB ratings are accepted if there are at least 10000 votes
def acceptable_imdb_rating(imdb):
    ratingCount = int(imdb[1])
    return ratingCount > 10000

main_page_response = requests.get('https://yts.am/browse-movies/0/all/sci-fi/7/year')
main_soup = BeautifulSoup(main_page_response.text, 'html.parser')

movies_in_page = main_soup.find_all('div', class_='browse-movie-wrap')

for movie in movies_in_page:
    movie_bottom = movie.div
    name_year = movie_bottom.a.string + ' - ' + movie_bottom.div.string

    movie_link = movie.a
    attributes = [attr.string for attr in movie_link.figure.figcaption.find_all('h4') if not attr.get('class')]
    str_attributes = ', '.join(attributes)

    try:
        imdb = get_imdb_rating(movie_link['href'])
    except AttributeError:
        print('Detail page not found for movie %s.' % name_year, '\n')
        continue

    if acceptable_imdb_rating(imdb):
        print('Film: ', name_year)
        print('Genre: ', str_attributes)
        print('Imdb: [Rating: %s, RatingCount: %s]' % (imdb[0], imdb[1]))
        print()
