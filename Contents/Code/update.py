from datetime import datetime
from providers import get_anime, get_episodes
import certifi
from utils import requests_retry_session
import re
import base64

def update_anime(type, metadata, media, force):
    resp = get_anime(metadata.id)
    Log.Debug("Anilist Response: {}".format(resp))
    result = JSON.ObjectFromString(resp)
    anime = result['data']['Page']['media'][0]
    has_mal_page = True
    #Get episode data
    if Prefs['episode_support']:
        try:
            mal_episodes = get_episodes(str(anime['idMal']))
        except:
            has_mal_page = False
            Log.Error('Error: Show has no episode data: ' + metadata.id)
    else: has_mal_page = False

    # Genres
    metadata.genres.clear()
    try:
        metadata.genres = anime['genres'] + anime['tags'] + [anime['format']] + [anime['status']] + [anime['season'] + ' ' + anime['seasonYear']]
    except:
        Log.Error('Error: Show has no genres: ' + metadata.id)

    # Rating
    try:
        metadata.rating = float(anime['averageScore']) / 10
    except:
        Log.Error('Error: Show has no rating: ' + metadata.id)

    # Title
    title_language = Prefs['title_language']
    for language in anime['title']:
        if language == title_language:
            metadata.title = anime['title'][language]
            break
        metadata.title = anime['title'][language]

    # Posters
    try:
        poster = Proxy.Media(
            requests_retry_session().get(
                anime['coverImage']['extraLarge'],
                verify=certifi.where()
            ).content
        )
        # //save file
        metadata.posters.validate_keys([])
        metadata.posters[anime['coverImage']['extraLarge']] = poster
    except:
        Log.Error('Error: Show has no posters: ' + metadata.id)

    # Summary
    try:
        cleanr = re.compile('<.*?>')
        metadata.summary = re.sub(cleanr, '', anime['description'])
    except:
        Log.Error('Error: Show has no summary: ' + metadata.id)

    # Country
    try:
        if anime['countryOfOrigin'] == 'JP':
            metadata.countries = ['Japan']
        elif anime['countryOfOrigin'] == 'CN':
            metadata.countries = ['China']
        elif anime['countryOfOrigin'] == 'KR':
            metadata.countries = ['Korea']
        else:
            metadata.countries = ['Unknown, please report']
    except:
        Log.Error('Error: Show has no country of origin: ' + metadata.id)

    # Start Date
    try:
        metadata.originally_available_at = datetime(anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
    except:
        Log.Error('Error: Show has no start date: ' + metadata.id)

    # Studio
    try:
        metadata.studio = anime['studios']['edges'][0]['node']['name']
    except:
        Log.Error('Error: Show has no studio: ' + metadata.id)

    metadata.roles.clear()

    # Characters
        # Log.Error(anime['characters']['edges'])
    try:
        for character in anime['characters']['edges']:
            # Create new role
            role = metadata.roles.new()

            # Get correct VA
            for VA in character['voiceActors']:

                # Set VA Name
                try:
                    role.name = VA['name']['full']
                except:
                    pass

                # Set VA Photo
                try:
                    role.photo = VA['image']['large']
                except:
                    pass

                # Set Character Name
                try:
                    role.role = character['node']['name']['full']
                except:
                    pass
    except:
        Log.Error('Error: Show has no Characters: ' + metadata.id)

    # Staff
    try:
        for staff in anime['staff']['edges']:

            # Create new role
            role = metadata.roles.new()

            # Set Staff Name
            try:
                role.name = staff['node']['name']['full']
            except:
                pass

            # Set Staff Photo
            try:
                role.photo = staff['node']['image']['large']
            except:
                pass

            # Set Staff Role
            try:
                role.role = staff['role']
            except:
                pass
    except:
        Log.Error('Error: Show has no staff: ' + metadata.id)

    # TV Specific
    if type == 'tv':

    # Banners
        try:
            banner_hash = base64.b64encode(str(anime['bannerImage']))
            banner = Proxy.Media(
                requests_retry_session().get(
                    anime['bannerImage'],
                    verify=certifi.where()
                ).content
            )
        except:
            Log.Error('Error: Show has no banners: ' + metadata.id)
            metadata.banners[banner_hash] = banner
            metadata.art[banner_hash] = banner


    # Movie Specific
    if type == 'movie':

        try:
            banner_hash = base64.b64encode(str(anime['bannerImage']))
            banner = Proxy.Media(
                requests_retry_session().get(
                    anime['bannerImage'],
                    verify=certifi.where()
                ).content
            )
            metadata.art[banner_hash] = banner
        except:
            Log.Error('Error: Show has no banners: ' + metadata.id)

    # Year
        try:
            metadata.year = anime['startDate']['year']
        except:
            Log.Error('Error: Show has no start date: ' + metadata.id)

    # Roles

        # Staff
        try:
            for staff in anime['staff']['edges']:

                # Director
                try:
                    if staff['role'] == 'Director':
                        director = metadata.directors.new()
                        director.name = staff['node']['name']['full']
                except:
                    pass
        except:
            Log.Error('Error: Show has no staff: ' + metadata.id)

    # Episodes
    if Prefs['episode_support'] and has_mal_page and 1 in media.seasons:
        update_episodes(media, metadata, force, mal_episodes)


def update_episodes(media, metadata, force, mal_episodes):
    for plex_episode_number in media.seasons[1].episodes:
        try:
            episode = metadata.seasons[1].episodes[int(plex_episode_number)]
            mal_episode = mal_episodes.get(int(plex_episode_number))
        except:
            Log.Error('Error: could not get episode data')
        try:
        #     # Title
                if Prefs['episode_title_language'] == 'default' and mal_episode['title']:
                    episode.title = mal_episode['title']
                elif Prefs['episode_title_language'] == 'japanese' and mal_episode['title_japanese']:
                    episode.title = mal_episode['title_japanese']
                elif Prefs['episode_title_language'] == 'romaji' and mal_episode['title_romaji']:
                    episode.title = mal_episode['title_romaji']
                else:
                    if mal_episode['title']:
                        episode.title = mal_episode['title']
                    elif mal_episode['title_romanji']:
                        episode.title = mal_episode['title_romanji']
                    elif mal_episode['title_japanese']:
                        episode.title = mal_episode['title_japanese']
        except:
            Log.Error('Error: Episode has no title: ' + metadata.id + ' Episode:' + str(plex_episode_number))

        # Air date
            try:
                if mal_episode['aired']:
                    cleanr = re.compile('\+[0-9][0-9]:[0-9][0-9]')
                    timestr = re.sub(cleanr, '', mal_episode['aired'])
                    episode.originally_available_at = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S')
            except:
                Log.Error('Error: Episode has no air date: ' + metadata.id + ' Episode:' + str(plex_episode_number))