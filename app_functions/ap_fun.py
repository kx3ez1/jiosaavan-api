import requests as r
import time
import os
from tqdm import tqdm
from requests_futures.sessions import FuturesSession


def get_song_url(encrypted_url1):
    url = "https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url={}&bitrate=320&api_version=4&_format=json&ctx=web6dot0&_marker=0".format(
        encrypted_url1)
    request1 = r.get(url).json()
    # print("\n json ===> ",request1)
    return request1['auth_url']


def search_song(search_string):
    url = "https://www.jiosaavn.com/api.php?p=1&q={}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=10&__call=search.getResults".format(
        search_string)
    request2 = r.get(url).json()
    print("songs --> ")
    for i in request2['results']:
        print(request2['results'].index(i), '-', i['title'], ' - ', i['more_info']['album'])
    return request2['results'][int(input("Enter (0-9) :"))]


def search_album(search_string):
    url = "https://www.jiosaavn.com/api.php?p=1&q={}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=10&__call=search.getAlbumResults".format(
        search_string)
    request2 = r.get(url).json()
    print("Albums --> ")
    for i in request2['results']:
        print(request2['results'].index(i), '-', i['title'], '-- {}'.format(i['language']))
    return request2['results'][int(input("Enter (0-9) :"))]


def extract_encrypted_url(json_value):
    value = ''
    if "encrypted_media_url" in str(json_value):
        value = json_value['more_info']['encrypted_media_url']
        value = value.replace("+", '%2B')
        value = value.replace("/", '%2F')
        # print("value",value)
    else:
        print("no Encrypted_url")
    return value


def wait():
    print("waiting")


def get_album_songs_list(id):
    url = "https://www.jiosaavn.com/api.php?__call=content.getAlbumDetails&albumid={}&api_version=4&_format=json&_marker=0&ctx=web6dot0".format(
        id)
    request3 = r.get(url).json()
    return request3['list']


def download_song(name, url):
    chunk_size = 1024
    doc = r.get(url, stream=True)
    total_size = int(doc.headers['content-length'])
    with open(name, 'wb') as f:
        for data in tqdm(iterable=doc.iter_content(chunk_size=chunk_size), total=total_size / chunk_size, unit='KB'):
            f.write(data)
    print("\nDownload complete!\n")


def create_folder(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


def search_playlist(search_string):
    url = "https://www.jiosaavn.com/api.php?p=1&q={}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=10&__call=search.getPlaylistResults".format(
        search_string)
    request2 = r.get(url).json()
    print("playlists --> ")
    for i in request2['results']:
        print(request2['results'].index(i), '-', i['title'])
    return request2['results'][int(input("Enter (0-9) :"))]


def get_playlist_songs_list(token, list_id):
    url = "https://www.jiosaavn.com/api.php?__call=webapi.get&token={}&type=playlist&p=2&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0".format(
        token)
    request3 = r.get(url).json()
    if len(request3['list']) == 0:
        url = "https://www.jiosaavn.com/api.php?__call=playlist.getDetails&listid={}&api_version=4&_format=json&_marker=0&ctx=web6dot0".format(
            list_id)
        request3 = r.get(url).json()
    return request3['list']


def get_trending_playlist():
    url = "https://www.jiosaavn.com/api.php?__call=webapi.getLaunchData&api_version=4&_format=json&_marker=0&ctx=web6dot0"
    request2 = r.get(url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"},verify=False).json()
    playlists = request2['new_trending'] + request2['top_playlists'] + request2['promo:vx:data:32'] + request2[
        'promo:vx:data:19'] + request2['promo:vx:data:9']
    print("Trending playlists --> ")
    for i in playlists:
        lang = ''
        try:
            if '' in i['language']:
                lang = ''
            else:
                lang = '--' + i['language']
        except:
            pass
        print(playlists.index(i), '-', i['title'], lang)
    return playlists[int(input("Enter (0-9) :"))]


def search_artist(search_string):
    url = "https://www.jiosaavn.com/api.php?p=1&q={}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n=10&__call=search.getArtistResults".format(
        search_string)
    request2 = r.get(url).json()
    print("Artists --> ")
    session = FuturesSession()
    for i in request2['results']:
        lang = 'not found'
        try:
            token_id = (i['perma_url']).split('/')
            token_id = token_id[-1]
            url = f'https://www.jiosaavn.com/api.php?__call=webapi.get&token={token_id}&type=artist&p=&n_song=50&n_album=50&sub_type=songs&more=true&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0'
            lang = session.get(url).result().json()['dominantLanguage']
        except Exception as e:
            print(e)
        print(request2['results'].index(i), '-', i['name'], '-', lang)
    return request2['results'][int(input("Enter (0-9) :"))]


def get_artist_songs_list(token):
    d = []
    for i in range(20):
        url = f'https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&type=artist&p={i}&n_song=50&n_album=50&sub_type=songs&more=true&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0'
        a = r.get(url).json()
        b = a["topSongs"]
        d = d + b
        if len(b) == 0:
            break
    return d


# print(get_artist_songs_list('Tia567J8WCU_', '791554'))

"""#returns songs list
def download_artist_songs(search_string):
    artist = search_artist(search_string)
    token_id = (artist['perma_url']).split('/')
    token_id = token_id[-1]
    return get_artist_songs_list(token_id)"""
