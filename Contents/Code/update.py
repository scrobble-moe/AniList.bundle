from datetime import datetime
from anilist import get_anime

VOICE_LANGUAGES = {
    'de': 'German',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'he': 'Hebrew',
    'hu': 'Hungarian',
    'it': 'Italian',
    'ja_jp': 'Japanese',
    'ko': 'Korean',
    'pt_br': 'Portuguese',
}

def update_anime(type, metadata, media, force):
    result = JSON.ObjectFromString(get_anime(metadata.id))
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')

    # Log.Error()

    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')
    # Log.Error('TEST')

    anime = result['data']['Page']['media'][0]


    

    # includes = {
    #     'categories': [],
    #     'episodes': [],
    #     'animeProductions': [],
    #     'producers': [],
    #     'mediaCharacters': [],
    #     'characters': [],
    #     'characterVoices': [],
    #     'people': [],
    #     'mediaStaff': [],
    #     'mappings': []
    # }
    # for include in result['included']:
    #     includes[include['type']].append(include)

    # if metadata.genres is None or force:
    #     metadata.genres = map(lambda c: c['attributes']['title'], includes['categories'])

    # if (metadata.duration is None or force) and anime['episodeLength'] is not None:
        # metadata.duration = anime['episodeLength'] * 60000

    if (metadata.rating is None or force) and anime['averageScore'] is not None:
        metadata.rating = float(anime['averageScore']) / 10

    if (metadata.title is None or force) and anime['title']['romaji'] is not None:
        # title_language = Prefs['title_language']
        # if title_language == 'English' and anime['titles']['en'] is not None:
        #     metadata.title = anime['titles']['en']
        # elif title_language == 'Romanized' and anime['titles']['en_jp'] is not None:
        #     metadata.title = anime['titles']['en_jp']
        # else:
        #     metadata.title = anime['canonicalTitle']
        metadata.title = anime['title']['romaji']

    if (metadata.summary is None or force) and anime['description'] is not None:
        metadata.summary = anime['description']

    # if (metadata.originally_available_at is None or force) and anime['startDate'] is not None:
    #     split = map(lambda s: int(s), anime['startDate'].split('-'))
    #     start_date = datetime(split[0], split[1], split[2])
    #     metadata.originally_available_at = start_date

    # if (metadata.content_rating is None or force) and anime['ageRatingGuide'] is not None:
    #     metadata.content_rating = anime['ageRatingGuide']

    # if metadata.studio is None or force:
    #     anime_studio = find_first(lambda ap: ap['attributes']['role'] == 'studio',
    #         includes['animeProductions'])
    #     if anime_studio is not None:
    #         studio_id = anime_studio['relationships']['producer']['data']['id']
    #         studio = find_first(lambda p: p['id'] == studio_id, includes['producers'])
    #         if studio is not None:
    #             metadata.studio = studio['attributes']['name']

    # if metadata.roles is None or force:
    #     for char in includes['mediaCharacters']:
    #         char_id = char['relationships']['character']['data']['id']
    #         character = find_first(lambda c: c['id'] == char_id, includes['characters'])
    #         if character is not None:
    #             voice_ids = map(lambda cv: cv['id'], char['relationships']['voices']['data'])
    #             voices = filter(lambda v: v['id'] in voice_ids, includes['characterVoices'])
    #             if voices is not None:
    #                 for voice in voices:
    #                     person_id = voice['relationships']['person']['data']['id']
    #                     person = find_first(lambda p: p['id'] == person_id, includes['people'])
    #                     if person is not None:
    #                         role = metadata.roles.new()
    #                         role.name = person['attributes']['name']
    #                         if person['attributes']['image'] is not None:
    #                             role.photo = person['attributes']['image']['original']

    #                         if voice['attributes']['locale'] is not None:
    #                             locale = voice['attributes']['locale']
    #                             locale = VOICE_LANGUAGES.get(locale, locale)
    #                             role.role = '{} ({})'.format(
    #                                 character['attributes']['canonicalName'], locale
    #                             )
    #                         else:
    #                             role.role = character['attributes']['canonicalName']

    #     for staff in includes['mediaStaff']:
    #         person_id = staff['relationships']['person']['data']['id']
    #         person = find_first(lambda p: p['id'] == person_id, includes['people'])
    #         if person is not None:
    #             role = metadata.roles.new()
    #             role.name = person['attributes']['name']
    #             if person['attributes']['image'] is not None:
    #                 role.photo = person['attributes']['image']['original']
    #             if staff['attributes']['role'] is not None:
    #                 role.role = staff['attributes']['role']

    if (metadata.posters is None or force) and anime['coverImage']['extraLarge'] is not None:
        poster_image = anime['coverImage']
        try:
            thumbnail = Proxy.Preview(HTTP.Request(
                poster_image['medium'], immediate = True
            ).content)
            metadata.posters[poster_image['extraLarge']] = thumbnail
        except:
            Log.Error('Error loading poster - Anime: ' + metadata.id)

    # if type == 'tv':
    #     if (metadata.banners is None or force) and anime['coverImage'] is not None:
    #         cover_image = anime['coverImage']
    #         try:
    #             thumbnail = Proxy.Preview(HTTP.Request(
    #                 cover_image['original'], immediate = True
    #             ).content)
    #             metadata.banners[cover_image['original']] = thumbnail
    #         except:
    #             Log.Error('Error loading banner - Anime: ' + metadata.id)

    #     if 1 in media.seasons:
    #         update_episodes(media, metadata, force, anime, includes['episodes'])

    # if type == 'movie':
    #     if (metadata.year is None or force) and anime['startDate'] is not None:
    #         metadata.year = int(anime['startDate'][:4])

def update_episodes(media, metadata, force, anime, inc_episodes):
    for number in media.seasons[1].episodes:
        number = int(number)
        episode = metadata.seasons[1].episodes[number]

        if anime['subtype'] == 'movie':
            if (episode.title is None or force) and metadata.title is not None:
                episode.title = metadata.title

            if (episode.summary is None or force) and metadata.summary is not None:
                episode.summary = metadata.summary

            if (episode.originally_available_at is None or force):
                if metadata.originally_available_at is not None:
                    episode.originally_available_at = metadata.originally_available_at

            if (episode.thumbs is None or force) and anime['posterImage'] is not None:
                poster_image = anime['posterImage']
                try:
                    thumbnail = Proxy.Preview(HTTP.Request(
                        poster_image['tiny'], immediate = True
                    ).content)
                    episode.thumbs[poster_image['large']] = thumbnail
                except:
                    Log.Error('Error loading poster - Anime: ' + metadata.id)

            if (episode.duration is None or force) and metadata.duration is not None:
                episode.duration = metadata.duration

            return

        ep = find_first(lambda e: e['attributes']['relativeNumber'] == number,
            inc_episodes)

        if ep is None:
            ep = find_first(lambda e: e['attributes']['number'] == number, inc_episodes)
            if ep is None:
                return

        ep = ep['attributes']

        if (episode.title is None or force) and ep['canonicalTitle'] is not None:
            episode.title = ep['canonicalTitle']

        if (episode.summary is None or force) and ep['synopsis'] is not None:
            episode.summary = ep['synopsis']

        if (episode.originally_available_at is None or force) and ep['airdate'] is not None:
            split = map(lambda s: int(s), ep['airdate'].split('-'))
            air_date = datetime(split[0], split[1], split[2])
            episode.originally_available_at = air_date

        if (episode.thumbs is None or force) and ep['thumbnail'] is not None:
            thumb_image = ep['thumbnail']['original']
            try:
                thumbnail = Proxy.Preview(HTTP.Request(thumb_image, immediate = True).content)
                episode.thumbs[thumb_image] = thumbnail
            except:
                Log.Error('Error loading thumbnail - Anime:Episode: ' +
                    metadata.id + ':' + number)

        if (episode.duration is None or force) and ep['length'] is not None:
            episode.duration = ep['length'] * 60000

def find_first(p, list):
    for i in list:
        if p(i):
            return i
    return None
