import html
import urllib.request
from mutagen.mp4 import MP4, MP4Cover

unicode = str


def add_tags(song_file, json_data):
    #print(json_data)
    audio = MP4(song_file)
    try:
        audio['\xa9nam'] = html.unescape(unicode(json_data['title']))
    except:
        pass
    try:
        audio['\xa9wrt'] = html.unescape(unicode(json_data['music']))
    except:
        pass
    try:
        audio['desc'] = html.unescape(unicode(json_data['subtitle']))
        # audio['\xa9day'] = html.unescape(unicode(json_data['more_info']['year']))
        # audio['\xa9gen'] = html.unescape(unicode(playlist_name))
        # audio['cprt'] = track['copyright'].encode('utf-8')
        # audio['disk'] = [(1, 1)]
        # audio['trkn'] = [(int(track['track']), int(track['maxtracks']))]
        # audio['cprt'] = html.unescape(unicode(json_data['label']))
        # if track['explicit']:
        # audio['rtng'] = [(str(4))]
    except:
        pass
    try:
        audio['\xa9alb'] = html.unescape(unicode(json_data['more_info']['album']))
    except:
        pass
    try:
        artists = json_data['subtitle']
        audio['\xa9ART'] = html.unescape(unicode(artists))
        artists = artists.replace('album', '')
        audio['\xa9ART'] = html.unescape(unicode(artists))
    except:
        pass
    try:
        artists = json_data['subtitle']
        audio['aART'] = html.unescape(unicode(artists))
        artists = artists.replace('album', '')
        audio['aART'] = html.unescape(unicode(artists))
    except:
        pass
    try:
        cover_url = json_data['image'][:-11] + '500x500.jpg'
        fd = urllib.request.urlopen(cover_url)
        cover = MP4Cover(fd.read(), getattr(
            MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audio['covr'] = [cover]
        audio.save()
    except:
        pass