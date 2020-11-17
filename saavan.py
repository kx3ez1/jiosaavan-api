from app_functions import ap_fun, add_tags, console_colors
import time
from itertools import count

console_colors.prGreen("""@@@@@@@@@@@@@@@@@@#*.,/%@@@@@@@@@@@@@@@@@@@@@@@@#*,..................,*#@@@@@@@@
@@@@@@@@@@@...................,@@@@@@@@@@@,..... *((################((, .....*@@
@@@@@@@*..........................%@@@@@*...@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@...&
@@@@@................................@@@../@@%.....@@@@@@@@@@@@...........@@@ ..
@@@...............#@@.................(@@#@@@.......@@@@@@@@@@@............@@@..
@@.........#@@@%.#@@@@................. @@@@@........@@@@@@@@@@............@@@..
@..........@@@@@.............**.........,@@@@.........@@@@@@@@@............@@@..
&..........@@@@@.%@@@@ ..@@@@@@@@@@......@@@@@@&.......@@@@@@@@..........,@@@@..
...........@@@@@.%@@@@ ,@@@@....@@@@,....&@@@@@@@@.....%@@@@@@%.......@@@@@@@@..
#....,*....@@@@@.%@@@@ ,@@@@....%@@@(....@@@@@@@@@@@....@@@@@@.....@@@@@@@@@@@..
@...#@@@@@@@@@@..%@@@@ ./@@@@@@@@@@#.....@@@@@@@@@@@@%..,@@@@#...@@@@@@@@@@@@@..
@&.....&@@@@#...../&&......(@@@@(.......@@@@@@@@@@@@@@@..@@@@..@@@@@@@@@@@@@@@..
@@@....................................@@@@@@.. @@@@@@@@./@@..@@@@@@@......@@@..
@@@@................................./@@@.&@@........@@@,.@.,@@@&........./@@(..
@@@@@@,............................#@@@@...@@@@/.......@@...@@..........%@@@@...
@@@@@@@@@,......................(@@@@@@@@,...,@@@@@@@@@@@@@@@@@@@@@@@@@@@@....#@
@@@@@@@@@@@@@@.............(@@@@@@@@@@@@@@@@,..............................(@@@@        Jio Saavn 
""")
console_colors.prCyan('Only High Quality songs - 320kbps')
console_colors.prCyan('\'Unofficial jio-saavan Music Downloader!\'')


def download_song():
    song = ap_fun.search_song(input('Enter song name : '))  # json
    url = ap_fun.extract_encrypted_url(song)
    url = ap_fun.get_song_url(url)
    print('downloading..', song['title'])
    name = song['title'] + '.m4a'
    ap_fun.create_folder('songs')
    name1 = 'songs/' + song['title'] + '.m4a'
    ap_fun.download_song(name1, url)  # download
    add_tags.add_tags(name1, song)


def download_album():
    album = ap_fun.search_album(input('search Album : '))
    # print(album)
    songs_list_json = ap_fun.get_album_songs_list(album['id'])
    if songs_list_json:
        # console_colors.prCyan('album language {}'.format(album['more_info']['language']))
        console_colors.prCyan('songs list ===> ')
    for i in songs_list_json:
        a1 = str(songs_list_json.index(i)) + '-' + i['title']
        console_colors.prGreen(a1)
    inp3 = list(map(str, input('Enter Index (Ex: 1 2 3 4) or ENTER to all: ').split()))
    if len(inp3) == 0:
        inp3 = range(len(songs_list_json))
    else:
        inp3 = [int(i) for i in inp3]
    folder_name = album['title']
    ap_fun.create_folder(folder_name)
    for i in inp3:
        songs = songs_list_json[i]
        url = ap_fun.get_song_url(ap_fun.extract_encrypted_url(songs))
        name = folder_name + '/' + songs['title'] + '.m4a'
        print('downloading song..', songs['title'])
        ap_fun.download_song(name, url)  # download
        add_tags.add_tags(name, songs)


def download_playlist():
    global folder_name1
    playlist = ap_fun.search_playlist(input('search Playlist : '))
    if playlist:
        folder_name1 = playlist['title']
        print('playlist : ', folder_name1, ' --> ', 'language :', playlist['more_info']['language'])
    token_id = (playlist['perma_url']).split('/')  # token extracting from url
    # print(token_id[-1])
    playlist = ap_fun.get_playlist_songs_list(token_id[-1], playlist['id'])
    for i in playlist:
        desc = str(playlist.index(i)) + ' - ' + i['title']
        console_colors.prCyan(desc)
    console_colors.prRed('total songs in playlist : {}'.format(len(playlist)))
    inp4 = list(map(str, input('Enter Index (Ex: 1 2 3 4) or ENTER to all: ').split()))
    if len(inp4) == 0:
        ap_fun.create_folder(folder_name1)
        for i in playlist:
            song_json = i
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            # name = song_json['title'] + '.m4a'
            name1 = folder_name1 + '/' + song_json['title'] + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)
    else:
        inp4 = [int(i) for i in inp4]
        if len(inp4) > 0:
            ap_fun.create_folder(folder_name1)
        for i in inp4:
            song_json = playlist[i]
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            # name = song_json['title'] + '.m4a'
            name1 = folder_name1 + '/' + song_json['title'] + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)


def download_trending_playlist():
    global folder_name1
    playlist = ap_fun.get_trending_playlist()
    if playlist:
        folder_name1 = playlist['title']
        print('playlist : ', folder_name1, ' --> ', 'language :', playlist['language'])
    token_id = (playlist['perma_url']).split('/')  # token extracting from url
    # print(token_id[-1])
    playlist = ap_fun.get_playlist_songs_list(token_id[-1], playlist['id'])
    for i in playlist:
        desc = str(playlist.index(i)) + ' - ' + i['title']
        console_colors.prCyan(desc)
    console_colors.prRed('total songs in playlist : {}'.format(len(playlist)))
    inp4 = list(map(str, input('Enter Index (Ex: 1 2 3 4) or ENTER to all: ').split()))
    if len(inp4) == 0:
        ap_fun.create_folder(folder_name1)
        for i in playlist:
            song_json = i
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            # name = song_json['title'] + '.m4a'
            name1 = folder_name1 + '/' + song_json['title'] + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)
    else:
        inp4 = [int(i) for i in inp4]
        if len(inp4) > 0:
            ap_fun.create_folder(folder_name1)
        for i in inp4:
            song_json = playlist[i]
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            # name = song_json['title'] + '.m4a'
            name1 = folder_name1 + '/' + song_json['title'] + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)


def download_artist():
    global folder_name1
    while True:
        search_string = input('Enter ArtistName : ')
        if len(search_string) > 2:
            break
    artist = ap_fun.search_artist(search_string)
    print('fetching songs..')
    if artist:
        folder_name1 = artist['name']
    token_id = (artist['perma_url']).split('/')
    token_id = token_id[-1]
    artist = ap_fun.get_artist_songs_list(token_id)
    #print(artist)
    """"""
    for i in artist:
        desc = str(artist.index(i)) + ' - ' + i['title']
        console_colors.prCyan(desc)
    console_colors.prRed('total songs in artist  [not accurate] : {}'.format(len(artist)))
    inp4 = list(map(str, input(f'Enter Index (Ex: 1 2 3 4...{len(artist)-1}) or ENTER to all: ').split()))
    if len(inp4) == 0:
        ap_fun.create_folder(folder_name1)
        for i in artist:
            song_json = i
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            name = song_json['title']
            name = name.replace('&quot;', '')
            name1 = folder_name1 + '/' + name + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)
    else:
        inp4 = [int(i) for i in inp4]
        if len(inp4) > 0:
            ap_fun.create_folder(folder_name1)
        for i in inp4:
            song_json = artist[i]
            e_url = ap_fun.extract_encrypted_url(song_json)
            url = ap_fun.get_song_url(e_url)
            print('downloading..', song_json['title'])
            name = song_json['title']
            name = name.replace('&quot;', '')
            name1 = folder_name1 + '/' + name + '.m4a'
            ap_fun.download_song(name1, url)  # download
            add_tags.add_tags(name1, song_json)


def iter1():
    global folder_name1
    try:
        print()
        console_colors.prYellow("1-download song")
        console_colors.prYellow('2-download album')
        console_colors.prYellow('3-download playlist')
        console_colors.prYellow('4-download Artist')
        #console_colors.prYellow('5-download Trending')
        inp2 = input('\nEnter your choice : ')
        if inp2 == '1':
            download_song()
        elif inp2 == '2':
            download_album()
        elif inp2 == '3':
            download_playlist()
        elif inp2 == '4':
            download_artist()
        else:
            print('you entered an incorrect option')
    except Exception as e:
        print('error occured - ', e)


if __name__ == '__main__':
    for i in count(0):
        iter1()
        print('\nprocess completed', '\n', '-'*40)
        inpz = input('Download more to press ENTER to continue! q to exit')
        if inpz == '':
            continue
        else:
            exit()
