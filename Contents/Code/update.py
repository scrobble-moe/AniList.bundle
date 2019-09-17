from datetime import datetime
from anilist import get_anime, get_anime_kitsu, get_episodes_kitsu
import certifi
import requests
import re

def update_anime(type, metadata, media, force):
    result = JSON.ObjectFromString(get_anime(metadata.id))
    has_kitsu_data = True
    has_kitsu_episode_data = True
    anime = result['data']['Page']['media'][0]

    # Get Kistu data
    try:
        kitsu = JSON.ObjectFromString(get_anime_kitsu(str(anime['idMal'])))
    except:
        has_kitsu_data = False
        Log.Error('Error: Show has no relation for getting kitsu data: ' + metadata.id)

    #Get episode data
    if has_kitsu_data and Prefs['episode_support']:
        try:
            kitsu_episodes = get_episodes_kitsu(str(kitsu['included'][0]['id']))
        except:
            has_kitsu_episode_data = False
            Log.Error('Error: Show has no episode data: ' + metadata.id)
    else: has_kitsu_episode_data = False

    # Genres
    if metadata.genres is None or force:
        metadata.genres.clear()
        try:
            metadata.genres = anime['genres']
        except:
            Log.Error('Error: Show has no genres: ' + metadata.id)
        
    # Rating
    if metadata.rating is None or force:
        try:
            metadata.rating = float(anime['averageScore']) / 10
        except:
            Log.Error('Error: Show has no rating: ' + metadata.id)

    # Title
    if metadata.title is None or force:
        title_language = Prefs['title_language']        
        for language in anime['title']:
            if language == title_language:
                metadata.title = anime['title'][language]
                break
            metadata.title = anime['title'][language]

    # Posters
    if metadata.posters is None or force:
        try:            
            thumbnail = Proxy.Preview(
                requests.get(
                    anime['coverImage']['medium'],
                    verify=certifi.where()
                ).content
            )
            metadata.posters[anime['coverImage']['extraLarge']] = thumbnail
        except:
            Log.Error('Error: Show has no posters: ' + metadata.id)
      
    # Summary
    if metadata.summary is None or force:
        try:
            metadata.summary = anime['description']
        except:
            Log.Error('Error: Show has no summary: ' + metadata.id)

    # Country
    if metadata.countries is None or force:
        try:
            if anime['countryOfOrigin'] == 'JP':
                metadata.countries = ["Japan"]
            elif anime['countryOfOrigin'] == 'CN':
                metadata.countries = ["China"]
            elif anime['countryOfOrigin'] == 'KR':
                metadata.countries = ["Korea"]
            else:
                metadata.countries = ["Unknown, please report"]
        except:
            Log.Error('Error: Show has no country of origin: ' + metadata.id)
        
    # Start Date
    if metadata.originally_available_at is None or force:
        try:
            metadata.originally_available_at = datetime(anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
        except:
            Log.Error('Error: Show has no start date: ' + metadata.id)

    # Studio
    if metadata.studio is None or force:
        try:
            metadata.studio = anime['studios']['edges'][0]['node']['name']
        except:
            Log.Error('Error: Show has no studio: ' + metadata.id)

    # Content Rating
    if has_kitsu_data and metadata.content_rating is None or force:
        try:
            metadata.content_rating = kitsu['included'][0]['attributes']['ageRating']
        except:
            Log.Error('Error: Show has no content rating: ' + metadata.id)


    if metadata.roles is None or force:
        metadata.roles.clear()

    # Characters
    if metadata.roles is None or force:
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
    if metadata.roles is None or force:
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
        if metadata.banners is None or force:
            try:
                thumbnail = Proxy.Preview(
                    requests.get(
                        anime['bannerImage'],
                        verify=certifi.where()
                    ).raw
                )
                metadata.banners[anime['bannerImage']] = thumbnail
            except:
                Log.Error('Error: Show has no banners: ' + metadata.id)

    # Movie Specific
    if type == 'movie':

        # Year
        if metadata.year is None or force:
            try:
                metadata.year = anime['startDate']['year']
            except:
                Log.Error('Error: Show has no start date: ' + metadata.id)

        # Roles
        if metadata.roles is None or force:
            
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
    if Prefs['episode_support'] and has_kitsu_episode_data and 1 in media.seasons:
        update_episodes(media, metadata, force, anime, kitsu_episodes)


def update_episodes(media, metadata, force, anime, kitsu_episodes):

    for plex_episode_number in media.seasons[1].episodes:
        try:
            episode = metadata.seasons[1].episodes[int(plex_episode_number)]
            kitsu_episode = kitsu_episodes.get(int(plex_episode_number))

            # Description
            if episode.summary is None or force:
                try:
                    cleanr = re.compile('<.*?>')
                    episode.summary = re.sub(cleanr, '', kitsu_episode['attributes']['synopsis'])
                except:
                    Log.Error('Error: Episode has no summary: ' + metadata.id)

            # Title
            if episode.title is None or force:
                try:
                    episode.title = kitsu_episode['attributes']['canonicalTitle']
                except:
                    Log.Error('Error: Episode has no title: ' + metadata.id)

            # Air date
            if episode.originally_available_at is None or force:
                try:
                    split = map(lambda s: int(s), kitsu_episode['attributes']['airdate'].split('-'))
                    episode.originally_available_at = datetime(split[0], split[1], split[2])
                except:
                    Log.Error('Error: Episode has no air date: ' + metadata.id)
        except:
            pass