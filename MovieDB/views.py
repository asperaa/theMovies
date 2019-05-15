#!/usr/bin/env python
#


""" The views for the Simple MOvie Database  """
from django.shortcuts import render_to_response, render
from .forms import SearchForm
# from .models import Movie


import json
import requests


my_api_key='97eecb31def7da5dea54678339f2cfa9'

SEARCH_PATTERN='https://api.themoviedb.org/3/search/movie?api_key={key}&query={your_query}'
MOVIE_INFO_PATTERN='https://api.themoviedb.org/3/movie/{id}?api_key={key}&language=en-US'
MOVIE_ALT_PATTERN='https://api.themoviedb.org/3/movie/{id}/alternative_titles?api_key={key}'
MOVIE_RELEASE_PATTERN='https://api.themoviedb.org/3/movie/{id}/release_dates?api_key={key}'
MOVIE_KEYWORD_PATTERN='https://api.themoviedb.org/3/movie/{id}/keywords?api_key={key}'
MOVIE_REVIEW_PATTERN='https://api.themoviedb.org/3/movie/{id}/reviews?api_key={key}&language=en-US&page=1'
MOVIE_CAST_PATTERN='https://api.themoviedb.org/3/movie/{id}/credits?api_key={key}'
MOVIE_CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
MOVIE_IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{id}/images?api_key={key}'
MOVIE_YOUTUBE_PATTERN='https://www.youtube.com/watch?v={youtube_key}'
MOVIE_TRAILER_PATTERN='https://api.themoviedb.org/3/movie/{id}/videos?api_key={key}&language=en-US'
# movie_name=input('name of movie: ')


def _get_json(url):
    r = requests.get(url)
    return r.json()


def get_movie_list(movie_name):

    movie_search_json=_get_json(SEARCH_PATTERN.format(key=my_api_key,your_query=movie_name))
    movie_results=movie_search_json['results']

    obtained_titles=[]
    obtained_ids=[]

    for index in range(len(movie_results)):
        obtained_titles.append(movie_results[index]['title'])
        obtained_ids.append(movie_results[index]['id'])

    print(obtained_titles)

    return obtained_titles,obtained_ids


def home(request):
    """ Module that returns the default home page"""
    return render(request, 'index.html')


def index(request):
    """Module that returns the index.html page"""
    return render_to_response('index.html')

#
# def add_movie_form(request):
#     """
#     Module that adds the data from the page /addmovieform/
#         if a movie with the same title does not exist
#
#     :param request: request, HTML Template, movie_listing = the list of Movie objects
#     :return:
#     """
#     if request.POST:
#         form = MovieForm(request.POST)
#         if form.is_valid():
#             # Check if the movie already exists in the database
#             check_db = Movie.objects.filter(title=request.POST['title'])
#             if len(check_db) > 0:
#                 # If a movie with same name exists the do not enter to DB
#                 return render(request, 'movie_exists.html',
#                               {'movie_title': request.POST['title']})
#             else:
#                 # Save form and redirect to the success page
#                 form.save()
#                 return render_to_response('add_success.html',
#                                           {'movie_title': request.POST['title']})
#     else:
#         form = MovieForm()
#     return render(request, 'add_movie_form.html',
#                   {'form': form})


# def search(request):
#     """
#     Module to search the database with the title, genre, or director. Called from the /searchmovie/
#     :param request: page request
#     :return: request, HTML Template, movie_listing = the list of Movie objects
#     """
#     if request.GET:
#         movie_listing = []
#         search_string = ""
#         # Check for each entry in the search form.
#         # Find all the movies that match either one of the search entries
#         if request.GET['title']:
#             for movie_object in Movie.objects.filter(title__contains=request.GET['title']):
#                 movie_dict = {'movie_object': movie_object}
#                 movie_listing.append(movie_dict)
#             search_string = request.GET['title']
#         if request.GET['genre']:
#             for movie_object in Movie.objects.filter(genre__contains=request.GET['genre']):
#                 movie_dict = {'movie_object': movie_object}
#                 movie_listing.append(movie_dict)
#             search_string = " ".join((search_string, request.GET['genre']))
#         if request.GET['director']:
#             for movie_object in Movie.objects.filter(director__contains=request.GET['director']):
#                 movie_dict = {'movie_object': movie_object}
#                 movie_listing.append(movie_dict)
#             search_string = " ".join((search_string, request.GET['director']))
#         if request.GET['language']:
#             for movie_object in Movie.objects.filter(language__contains=request.GET['language']):
#                 movie_dict = {'movie_object': movie_object}
#                 movie_listing.append(movie_dict)
#             search_string = " ".join((search_string, request.GET['language']))
#         # Redirect to the results.html page if atleast one movie is found basedon the search strings
#         if len(movie_listing) > 0:
#             return render_to_response('results.html', {'search_string': search_string,
#                                                        'movie_listing': movie_listing})
#     form = MovieForm()
#     return render(request, 'search.html', {'form': form})

def search_movies(request):

    if request.method == 'POST':
        form=SearchForm(request.POST)

        if form.is_valid():
            movie_name=form.cleaned_data['movie_name']
            obtained_movie_titles,obtained_movie_ids = get_movie_list(movie_name)
            zipped_movies=zip(obtained_movie_titles,obtained_movie_ids)
            return render_to_response('results.html',{'movie_name':movie_name,'zipped_movies':zipped_movies})

    else:
        form=SearchForm()
        return render(request,'search.html',{'form':form})

# def list_all(request):
#     """ Module to list all the movies in the database"""
#     # sort_by = request.GET.get('sort', 'title')
#     # print ("Ordering by", sort_by)
#     # movie_listing = []
#     # for movie_object in Movie.objects.all().order_by(sort_by):
#     #     movie_dict = {'movie_object': movie_object}
#     #     movie_listing.append(movie_dict)
#
#     return render_to_response('list_all.html', {'movie_listing': movie_listing})


def get_movie_details(request,value):
    movie_details_json=_get_json(MOVIE_INFO_PATTERN.format(id=value,key=my_api_key))
    name=movie_details_json['original_title']
    language=movie_details_json['original_language']
    runtime=movie_details_json['runtime']
    genre=movie_details_json['genres'][0]['name']

    alt_title_list=get_alternate_titles(request,value)
    alt_title_string=" , ".join(alt_title_list)

    final_release_string=get_release_info(request,value)

    keyword_string=get_keywords(request,value)
    zipped_movies_reviews=get_movie_reviews(request,value)
    movie_cast,movie_crew=get_movie_cast(request,value)

    poster_url,backdrop_url=get_moview_images(request,value)

    video_url_list=get_movie_trailer(request,value)

    return render(request,'list_all.html',{'name':name,'language':language,'runtime':runtime,'genre':genre,'alt_title_string':alt_title_string,'final_release_string':final_release_string,'keyword_string':keyword_string,'zipped_movies_reviews':zipped_movies_reviews,'movie_cast':movie_cast,'movie_crew':movie_crew,'poster_url':poster_url,'backdrop_url':backdrop_url,'video_url_list':video_url_list})

def get_alternate_titles(request,value):
    movie_alt_titles=_get_json(MOVIE_ALT_PATTERN.format(id=value,key=my_api_key))
    alt_title_list=[value for d in movie_alt_titles['titles'] for key,value in d.items() if key == 'title']
    return alt_title_list

def get_release_info(request,value):
    movie_rel_info=_get_json(MOVIE_RELEASE_PATTERN.format(id=value,key=my_api_key))
    movie_country_list=[country_code for d in movie_rel_info['results'] for key,country_code in d.items() if key == 'iso_3166_1'][:4]
    movie_release_date=[release_date_info[0]['release_date'][:10] for d in movie_rel_info['results'] for key,release_date_info in d.items() if key == 'release_dates']
    final_release_list=[":".join(pair) for pair in zip(movie_country_list, movie_release_date)]
    final_release_string=" , ".join(final_release_list)

    return final_release_string

def get_keywords(request,value):
    keywords=_get_json(MOVIE_KEYWORD_PATTERN.format(id=value,key=my_api_key))
    keywords_list=[keyword for d in keywords['keywords'] for key,keyword in d.items() if key == 'name']
    keyword_string=','.join(keywords_list)
    print(keyword_string)

    return keyword_string

def get_movie_reviews(request,value):
    movie_reviews = _get_json(MOVIE_REVIEW_PATTERN.format(id=value,key=my_api_key))
    movie_reviews_author = [author for d in movie_reviews['results'] for key,author in d.items() if key == 'author']
    movie_reviews_url = [url for d in movie_reviews['results'] for key,url in d.items() if key == 'url']
    zipped_movies_reviews=zip(movie_reviews_author,movie_reviews_url)
    print(movie_reviews_url)

    return zipped_movies_reviews


def get_movie_cast(request,value):
    movie_people=_get_json(MOVIE_CAST_PATTERN.format(id=value,key=my_api_key))
    movie_cast=[cast_person for d in movie_people['cast'] for key,cast_person in d.items() if key == 'name']
    movie_crew=[crew_person for d in movie_people['crew'] for key,crew_person in d.items() if key == 'name']
    return movie_cast,movie_crew

def get_moview_images(request,value):
    base_config=_get_json(MOVIE_CONFIG_PATTERN.format(key=my_api_key))
    base_url=base_config['images']['base_url']
    poster_size=base_config['images']['poster_sizes'][1]
    backdrop_size=base_config['images']['backdrop_sizes'][1]

    images_json=_get_json(MOVIE_IMG_PATTERN.format(id=value,key=my_api_key))

    poster_path=""
    backdrop_path=""

    if len(images_json['posters']) != 0:
        poster_path=images_json['posters'][0]['file_path']

    if len(images_json['backdrops']) != 0:
        backdrop_path=images_json['backdrops'][0]['file_path']

    poster_url="{0}{1}{2}".format(base_url,poster_size,poster_path)
    backdrop_url="{0}{1}{2}".format(base_url,backdrop_size,backdrop_path)

    return poster_url,backdrop_url

def get_movie_trailer(request,value):
    video_json=_get_json(MOVIE_TRAILER_PATTERN.format(id=value,key=my_api_key))
    video_keys=[youtube_key for d in video_json['results'] for key,youtube_key in d.items() if key=='key']
    video_url=[MOVIE_YOUTUBE_PATTERN.format(youtube_key=key) for key in video_keys]
    return video_url



