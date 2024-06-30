from datetime import datetime
from providers import get_anime, get_episodes
import certifi
from utils import requests_retry_session
import re
import base64
try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

def update_generic(metadata, media, force, anime):

    # genres
    if metadata.genres is None or force:
        try:
            metadata.genres = anime['genres']
        except:
            Log.Error('Error: Show has no genres: ' + metadata.id)

        try:
            for tag in anime['tags']:
                metadata.genres.add(tag['name'])
        except:
            Log.Error('Error: Show has no tags: ' + metadata.id)

        try:
            metadata.genres.add(anime['format'])
        except:
            Log.Error('Error: Show has no format: ' + metadata.id)

        try:
            metadata.genres.add(anime['status'])
        except:
            Log.Error('Error: Show has no status: ' + metadata.id)

        try:
            metadata.genres.add(str(str(anime['seasonYear']) + ' ' + anime['season']))
        except:
            Log.Error('Error: Show has no season or seasonYear: ' + metadata.id)


    # tags

    # collections

    # reviews
    if metadata.reviews is None or force:
        metadata.reviews.clear()
        try:
            for review in anime['reviews']['edges']:

                # Create new review
                r = metadata.reviews.new()

                # Set Review Author
                try:
                    r.author = review['node']['user']['name']
                except:
                    pass

                # Set Review Source
                r.source = 'AniList'

                # Set Review Image
                try:
                    if int(review['node']['score']) >= 50:
                        r.image = 'rottentomatoes://image.review.fresh'
                    else:
                        r.image = 'rottentomatoes://image.review.rotten'
                except:
                    pass

                # Set Review Link
                try:
                    r.link = review['node']['siteUrl']
                except:
                    pass

                # Set Review Text
                try:
                    r.text = review['node']['summary']
                except:
                    pass
        except:
            Log.Error('Error: Show has no reviews: ' + metadata.id)

    # duration
    if metadata.duration is None or force:
        try:
            metadata.duration = anime['duration']
        except:
            Log.Error('Error: Show has no duration: ' + metadata.id)

    # rating
    if metadata.rating is None or force:
        try:
            metadata.rating = float(anime['averageScore']) / 10
        except:
            Log.Error('Error: Show has no rating: ' + metadata.id)

    # audience_rating

    # rating_image

    # audience_rating_image

    # original_title

    # title_sort

    # rating_count

    # key

    # rating_key

    # source_title

def update_anime(metadata, media, force):
    result = JSON.ObjectFromString(get_anime(metadata.id))
    anime = result['data']['Page']['media'][0]
    has_mal_page = True

    # Get episode data
    if Prefs['episode_support']:
        try:
            mal_episodes = get_episodes(str(anime['idMal']))
        except:
            has_mal_page = False
            Log.Error('Error: Show has no episode data: ' + metadata.id)
    else:
        has_mal_page = False

    update_generic(metadata, media, force, anime)

    # title
    if metadata.title is None or force:
        for language in anime['title']:
            if language == Prefs['title_language']:
                metadata.title = anime['title'][language]
                break
            metadata.title = anime['title'][language]

    # summary
    if metadata.summary is None or force:
        try:
            h = HTMLParser()
            cleanr = re.compile('<.*?>')
            metadata.summary = re.sub(
                cleanr, '', h.unescape(anime['description']))
        except:
            Log.Error('Error: Show has no summary: ' + metadata.id)

    # originally_available_at
    if metadata.originally_available_at is None or force:
        try:
            metadata.originally_available_at = datetime(
                anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
        except:
            Log.Error('Error: Show has no start date: ' + metadata.id)

    # content_rating

    # studio
    if metadata.studio is None or force:
        try:
            #TODO: Plex does not support multiple studios
            metadata.studio = anime['studios']['edges'][0]['node']['name']
        except:
            Log.Error('Error: Show has multiple or no studio: ' + metadata.id)

    # posters
    if metadata.posters is None or force:
        try:
            poster = Proxy.Media(
                requests_retry_session().get(
                    anime['coverImage']['extraLarge'],
                    verify=certifi.where()
                ).content
            )
            metadata.posters.validate_keys([]) #TODO: VERIFY
            metadata.posters[anime['coverImage']['extraLarge']] = poster
        except:
            Log.Error('Error: Show has no posters: ' + metadata.id)

    # banners
    if metadata.banners is None or force:
        try:
            banner_hash = base64.b64encode(str(anime['bannerImage']))
            banner = Proxy.Media(
                requests_retry_session().get(
                    anime['bannerImage'],
                    verify=certifi.where()
                ).content
            )
            metadata.banners[banner_hash] = banner
        except:
            Log.Error('Error: Show has no banners: ' + metadata.id)

    # art
    if metadata.art is None or force:
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

    # themes

    # seasons

    # roles
    if metadata.roles is None or force:
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

    # countries
    if metadata.countries is None or force:
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

    # extras

    # similar

    # thumb

    # art_url

    # episode_count

    # viewed_episode_count

    # has episodes?
        if Prefs['episode_support'] and has_mal_page and 1 in media.seasons:
            update_episodes(media, metadata, force, mal_episodes)

def update_movie(metadata, media, force):
    result = JSON.ObjectFromString(get_anime(metadata.id))
    anime = result['data']['Page']['media'][0]

    update_generic(metadata, media, force, anime)

    # title
    if metadata.title is None or force:
        for language in anime['title']:
            if language == Prefs['title_language']:
                metadata.title = anime['title'][language]
                break
            metadata.title = anime['title'][language]

    # year
    if metadata.year is None or force:
        try:
            metadata.year = anime['startDate']['year']
        except:
            Log.Error('Error: Show has no start date: ' + metadata.id)

    # originally_available_at
    if metadata.originally_available_at is None or force:
        try:
            metadata.originally_available_at = datetime(
                anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
        except:
            Log.Error('Error: Show has no start date: ' + metadata.id)

    # studio
    if metadata.studio is None or force:
        try:
            metadata.studio = anime['studios']['edges'][0]['node']['name']
        except:
            Log.Error('Error: Show has no studio: ' + metadata.id)

    # tagline

    # summary
    if metadata.summary is None or force:
        try:
            h = HTMLParser()
            cleanr = re.compile('<.*?>')
            metadata.summary = re.sub(
                cleanr, '', h.unescape(anime['description']))
        except:
            Log.Error('Error: Show has no summary: ' + metadata.id)

    # trivia

    # quotes

    # content_rating

    # content_rating_age

    # writers
    if metadata.writers is None or force:
        try:
            for staff in anime['staff']['edges']:
                # Create new role
                if staff['role'] == 'Original Creator':
                    writer = metadata.writers.new()
                    writer.name = staff['node']['name']['full']
        except:
            Log.Error('Error: Show has no Writers: ' + metadata.id)

    # directors
    if metadata.directors is None or force:
        try:
            for staff in anime['staff']['edges']:
                # Create new role
                if staff['role'] == 'Director':
                    director = metadata.directors.new()
                    director.name = staff['node']['name']['full']
        except:
            Log.Error('Error: Show has no Directors: ' + metadata.id)

    # producers
    if metadata.producers is None or force:
        try:
            for staff in anime['staff']['edges']:
                # Create new role
                if staff['role'] == 'Producer':
                    producer = metadata.producers.new()
                    producer.name = staff['node']['name']['full']
        except:
            Log.Error('Error: Show has no Producers: ' + metadata.id)

    # roles
    if metadata.roles is None or force:
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

    # countries
    if metadata.countries is None or force:
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

    # posters
    if metadata.posters is None or force:
        try:
            poster = Proxy.Media(
                requests_retry_session().get(
                    anime['coverImage']['extraLarge'],
                    verify=certifi.where()
                ).content
            )
            metadata.posters.validate_keys([]) #TODO: VERIFY
            metadata.posters[anime['coverImage']['extraLarge']] = poster
        except:
            Log.Error('Error: Show has no posters: ' + metadata.id)

    # art
    if metadata.art is None or force:
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

    # banners
    if metadata.banners is None or force:
        try:
            banner_hash = base64.b64encode(str(anime['bannerImage']))
            banner = Proxy.Media(
                requests_retry_session().get(
                    anime['bannerImage'],
                    verify=certifi.where()
                ).content
            )
            metadata.banners[banner_hash] = banner
        except:
            Log.Error('Error: Show has no banners: ' + metadata.id)

    # themes

    # chapters

    # extras

    # similar

    # thumb

    # art_url

def update_episodes(media, metadata, force, mal_episodes):
    for plex_episode_number in media.seasons[1].episodes:
        try:
            episode = metadata.seasons[1].episodes[int(plex_episode_number)]
            mal_episode = mal_episodes.get(int(plex_episode_number))

            try:
                # Title
                if episode.title is None or force:
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
                Log.Error('Error: Episode has no title: ' +
                        metadata.id + ' Episode:' + str(plex_episode_number))

            # Air date
                try:
                    if mal_episode and mal_episode['aired'] and episode.originally_available_at is None or force:
                        cleanr = re.compile('\+[0-9][0-9]:[0-9][0-9]')
                        timestr = re.sub(cleanr, '', mal_episode['aired'])
                        episode.originally_available_at = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S')
                except:
                    Log.Error('Error: Episode has no air date: ' + metadata.id + ' Episode:' + str(plex_episode_number))
        except:
            Log.Error('Error: could not get episode data')
