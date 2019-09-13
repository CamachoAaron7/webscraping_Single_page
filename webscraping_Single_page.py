
"""Scrape the Name, year, IMDB Rating, Metascore, and the number of votes from the first page of a the 
   URL http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1. But, first Lets 
   discover where the data we want is located within the URL using the devtools in Google Chrome. 
   To use the dev tools, go to the URL and right click on a movie title and click on inspect.
   This will take you right to the HTML line that corresponds to that particular element."""


from requests import get # Import the get() function from the requests module.
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1' # Assign the address of the web page to a variable named url.
response = get(url, headers = {"Accept-Language": "en-US, en;q=0.5"}) # Request the server the content of the web page by using get(), and store the server’s response in the variable response. # headers = {"Accept-Language": "en-US, en;q=0.5"} requests that we get all the scraped info in english even if we are over seas. 
# print(response.text[:500]) # Print a small part of response‘s content by accessing its .text attribute (response is now a Response object)


from bs4 import BeautifulSoup # Import the BeautifulSoup class creator from the package bs4.
html_soup = BeautifulSoup(response.text, 'html.parser') # Parse response.text by creating a BeautifulSoup object, and assign this object to html_soup. The 'html.parser' argument indicates that we want to do the parsing using Python’s built-in HTML parser.
# type(html_soup)

movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced') # Extract all the div containers that have a class attribute of lister-item mode-advanced
# print(type(movie_containers))
# print(len(movie_containers))

### Movie Name ###
first_movie = movie_containers[0] 
# print(first_movie) # Print first movie from movie_containers
# print(first_movie.div) # content of the first div tag
# print(first_movie.a) # content of the first <a> anchor tag
# print(first_movie.h3) # content of the first <h3> tag
# print(first_movie.h3.a) # content of the first <a> anchor tag within the <h3> tag.
# print(first_movie.h3.a.text) # Movie title - text content of the first <a> anchor tag within the <h3> tag.

### Year of Movie ###
first_year = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')
# print(first_year)
first_year = first_year.text
# print(first_year)


### IMDB Rating ###
first_imdb = float(first_movie.strong.text) # Convert IMDB score from a string to a Float.
# print(first_imdb)

### Metascore ###
first_mscore = first_movie.find('span', class_ = 'metascore favorable') # Below favorable will be deleted ratings include also unfavorable and mixed. Only metasocre will be used to define the class. 
first_mscore = int(first_mscore.text)
# print(first_mscore)

### Number of Votes ###
first_votes = first_movie.find('span', attrs = {'name':'nv'})
# print(first_votes)
first_votes = int(first_votes['data-value'])
# print(first_votes)






### SCRIPT FOR A SINGLE PAGE ###
# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
# Extract data from individual movie container
for container in movie_containers:
# If the movie has Metascore, then extract:
    if container.find('div', class_ = 'ratings-metascore') is not None:
# The name
    	name = container.h3.a.text
    	names.append(name)
# The year
    	year = container.h3.find('span', class_ = 'lister-item-year').text
    	years.append(year)
# The IMDB rating
    	imdb = float(container.strong.text)
    	imdb_ratings.append(imdb)
# The Metascore
    	m_score = container.find('span', class_ = 'metascore').text
    	metascores.append(int(m_score))
# The number of votes
    	vote = container.find('span', attrs = {'name':'nv'})['data-value']
    	votes.append(int(vote))




### VIEW SCRAPED DATA THAT HAS BEEN PULLED SO FAR ###
import pandas as pd
test_df = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes
})
# print(test_df.info())
# print(test_df)