# Courtney Gard 188620 CISW 128
import requests
from secrets import *
import base64
import json
import webbrowser


# TODO add a dictionary in get playlist function for playlist name and id as a key, value pair
# TODO a requests function
# TODO playlists class?


def auth_implicit_grant():
    auth_url = "https://accounts.spotify.com/authorize"
    response_type = 'response_type=token'
    scope = 'scope=playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public'
    redirect_uri = 'redirect_uri=https://www.csi.edu'
    webwindow = webbrowser.open(auth_url + '?' + response_type + '&client_id=' + client_credentials + '&' + scope
                                + '&' + redirect_uri)
    webwindow

    # response_item = response.json()
    # print(response.json())
    # print(json.dumps(response_item, indent=2))


base_api_address = 'https://api.spotify.com/v1/'
headers = {'Authorization': 'Bearer {token}'.format(token=token)}


# def auth(client_credentials, client_secret):
#     auth_url = "https://accounts.spotify.com/api/token"
#
#     # base64 encoding
#     message = f"{client_credentials}:{client_secret}"
#     message_Bytes = message.encode('ascii')
#     base64_Bytes = base64.b64encode(message_Bytes)
#     base64_Message = base64_Bytes.decode('ascii')
#     # print(base64Message)
#
#     auth_header = {'Authorization': 'Basic ' + base64_Message}
#     auth_data = {}
#     auth_data['grant_type'] = 'client_credentials'
#     response = requests.post(auth_url, headers=auth_header, data=auth_data)
#     response_item = response.json()
#     print(json.dumps(response_item, indent=2))

###code to get base 64 encoding###

# message = f"{client_credentials}:{client_secret}"
# messageBytes = message.encode('ascii')
# base64Bytes = base64.b64encode(messageBytes)
# base64Message = base64Bytes.decode('ascii')
# print(base64Message)

# if search_statusCode == 401:
#     data = {'grant_type': refresh_token}
#     refresh = requests.post('https://accounts.spotify.com/authorize', data= data)
#     print(refresh)
# else:
#     print(search_response)


def menu():
    print('\n********SELECTION MENU********\n'
          '1. Get auth credentials from a browser window URL\n'
          '2. Search for an artist or track\n'
          '3. Use an album ID to find an album\n'
          '4. Get your user ID\n'
          '5. Get a users playlist info\n'
          '6. Get track info from a playlist\n'
          '7. Create a playlist\n'
          '8. Add an item to a playlist\n'
          '9. Delete an item from a playlist\n'
          'q to quit the program\n')
    selection = input('What would you like to do? ')

    if selection == "1":
        auth_implicit_grant()

    elif selection == '2':
        search()

    elif selection == "3":
        print('\nTracks on this album')
        print(15 * '-')
        for item in album():
            print(item['name'])

    elif selection == "4":
        print('User ID: ' + get_user())

    elif selection == "5":
        print('\nPLAYLISTS: ')
        print(10 * '-')
        for name in get_playlist():
            print('PLAYLIST NAME: ' + name['name'] + "    " + 'PLAYLIST ID: ' + name['id'])

    elif selection == "6":
        print('\nPlaylist Tracks: ')
        print(10 * '-')
        for name in get_playlist_tracks():
            print(name['track']['name'] + '     Track ID: ' + name['track']['id'])

    elif selection == "7":
        create_playlist()

    elif selection == "8":
        add_items_playlist()

    elif selection == "9":
        delete_items_playlist()

    return selection


# gets the user id of the current user

def get_user():
    user_response = requests.get(base_api_address + 'me/', headers=headers)
    if user_response.status_code == 200 or 201:
        user_json = user_response.json()
        user_id = user_json['id']
        # print(json.dumps(user_json, indent=2))
    else:
        auth_implicit_grant()
    return user_id


# gets the playlist information and playlist ID of the current user

def get_playlist():
    user_playlist = requests.get(base_api_address + 'me/playlists', headers=headers)
    playlist_json = user_playlist.json()
    # print(user_playlist.status_code)
    # print(json.dumps(playlist_json, indent=2))
    playlist_names = playlist_json['items']
    return playlist_names


# gets track information from a specific playlist that the user provides the ID for

def get_playlist_tracks():
    playlist_id = input('What is the playlist ID? ')
    playlist_tracks = requests.get(base_api_address + 'playlists/' + playlist_id + '/tracks', headers=headers)
    tracks_json = playlist_tracks.json()
    # print(user_playlist.status_code)
    # print(json.dumps(tracks_json, indent=2))
    playlist_names = tracks_json['items']
    return playlist_names


# creates a playlist for the current user

def create_playlist():
    playlist_name = input('Playlist name: ')
    playlist_description = input('Description of playlist: ')
    data = {'name': playlist_name, 'description': playlist_description, 'public': False}
    playlist_response = requests.post(base_api_address + 'users/' + get_user() + '/playlists', json=data,
                                      headers=headers)
    # print(playlist_response.status_code)
    return playlist_response


# adds tracks to the playlist that the user provides the ID for

def add_items_playlist():
    playlist_id = input('What is the playlist ID you want to add this song to? ')
    track_id = input('What is the track ID of the song you want to add? ')
    data = '{"uris":["spotify:track:' + track_id + '"' + ']}'
    p_items_add = requests.post(base_api_address + 'playlists/' + playlist_id + '/tracks',
                                headers=headers, data=data)
    # print(p_items_add.status_code)
    return p_items_add


# playlist id 6pk64pZG7fCDeovWAoxaNC  random rock 5a3fc4IqrqBZlSLlYTFebh
# track id 57bgtoPSgt236HzfBOd8kj   7tFiyTwD0nx5a1eklYtX2J



# deletes tracks from the playlist that the user provides the information for

def delete_items_playlist():
    track_id = input('What is the track ID of the song you want to remove? ')
    playlist_id = input('What is the playlist ID you want to remove the song from? ')
    data = '{"tracks":[{"uri":"spotify:track:' + track_id + '"' + '}]}'
    p_items_remove = requests.delete(base_api_address + 'playlists/' + playlist_id + '/tracks',
                                     headers=headers, data=data)
    # print(p_items_remove.status_code)
    if p_items_remove.status_code == 200:
        print('Item Removed from Playlist!')
    else:
        print('That didn\'t work, try again')
        delete_items_playlist()


# gets the tracks from an album that the user provides the ID for

def album():
    album_response = requests.get(base_api_address + 'albums/' + example_album_id + '/tracks', headers=headers)
    album_info = album_response.json()
    album_tracks = album_info['items']
    # print(json.dumps(album_info['artists'], indent=2))
    # print(album_response.status_code)
    return album_tracks


# searches spotify for an artist or track and displays the information

def search():
    search_type_question = input('Are you searching for an artist or a track? ')
    if search_type_question == 'artist':
        search_query = input('Who are you searching for? ')
        search_type = 'artist'
        params = {'q': search_query, 'type': search_type}
        search_response = requests.get(base_api_address + 'search', params=params, headers=headers)
        # search_statusCode = search_response.status_code
        search_results = search_response.json()
        print('Artist Name: ' + search_results['artists']['items'][0]['name'])
        artist_genre = search_results['artists']['items'][0]['genres']
        artist_list = []
        for genre in artist_genre:
            artist_list.append(genre)
        artist_string = 'Artist Genre: '
        print(artist_string + ', '.join(artist_list))
        print('Artist ID: ' + search_results['artists']['items'][0]['id'])
        print('Artist link: ' + search_results['artists']['items'][0]['external_urls']['spotify'])
    elif search_type_question == 'track':
        search_query = input('What are you searching for? ')
        search_type = 'track'
        params = {'q': search_query, 'type': search_type}
        search_response = requests.get(base_api_address + 'search', params=params, headers=headers)
        # search_statusCode = search_response.status_code
        search_results = search_response.json()
        track_results = search_results['tracks']['items']
        # print(json.dumps(search_results['tracks']['items'][0], indent=2))
        for item in track_results:
            print('Track Name: ' + item['name'])
            print('Track Link: ' + item['external_urls']['spotify'] + '\n')


example_artist = '26AHtbjWKiwYzsoGoUZq53'
example_album_id = '2ryebd6mWqm1tI2Wr4ZbMp'

while menu() != 'q':
    menu()
