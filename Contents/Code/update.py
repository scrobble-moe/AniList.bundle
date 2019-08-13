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

    anime = result['data']['Page']['media'][0]


    if metadata.genres is None or force:
        metadata.genres = anime['genres']

    if (metadata.duration is None or force) and anime['duration'] is not None:
        metadata.duration = anime['duration'] * 60000

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

    if (metadata.originally_available_at is None or force) and anime['startDate'] is not None:
    #     split = map(lambda s: int(s), anime['startDate'].split('-'))
        start_date = datetime(anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
        metadata.originally_available_at = start_date

    # if (metadata.content_rating is None or force) and anime['ageRatingGuide'] is not None:
    #     metadata.content_rating = anime['ageRatingGuide']

    if metadata.studio is None or force:
        # anime_studio = find_first(lambda ap: ap['attributes']['role'] == 'studio',
        #     includes['animeProductions'])
        anime_studio = anime['studios']['edges'][0]

        if anime_studio is not None:
                metadata.studio = anime_studio['node']['name']


    # if metadata.studio is None or force:
    #     anime_studio = find_first(lambda ap: ap['attributes']['role'] == 'studio',
    #         includes['animeProductions'])
    #     if anime_studio is not None:
    #         studio_id = anime_studio['relationships']['producer']['data']['id']
    #         studio = find_first(lambda p: p['id'] == studio_id, includes['producers'])
    #         if studio is not None:
    #             metadata.studio = studio['attributes']['name']

    if metadata.roles is None or force:
        for character in anime['characters']['edges']:
            if character is not None:
                voices = character['voiceActors']
                if voices is not None:
                    for person in voices:
                        if person is not None:
                            role = metadata.roles.new()
                            role.name = person['name']['full']
                            if person['image']['large'] is not None:
                                role.photo = person['image']['large']
                            if character['node']['name']['full'] is not None:
                                role.role = character['node']['name']['full']

        for staff in anime['staff']['edges']:
            if staff is not None:
                role = metadata.roles.new()
                role.name = staff['node']['name']['full']
                if staff['node']['image']['large'] is not None:
                    role.photo = staff['node']['image']['large']
                if staff['role'] is not None:
                    role.role = staff['role']

    if (metadata.posters is None or force) and anime['coverImage']['extraLarge'] is not None:
        poster_image = anime['coverImage']
        try:
            thumbnail = Proxy.Preview(HTTP.Request(
                poster_image['medium'], immediate = True
            ).content)
            metadata.posters[poster_image['extraLarge']] = thumbnail
        except:
            Log.Error('Error loading poster - Anime: ' + metadata.id)

    if type == 'tv':
        if (metadata.banners is None or force) and anime['bannerImage'] is not None:
            cover_image = anime['coverImage']
            try:
                thumbnail = Proxy.Preview(HTTP.Request(
                    cover_image, immediate = True
                ).content)
                metadata.banners[cover_image] = thumbnail
            except:
                Log.Error('Error loading banner - Anime: ' + metadata.id)

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
# DONT THINK THIS IS NEEDED
        # if (episode.duration is None or force) and ep['length'] is not None:
        #     episode.duration = ep['length'] * 60000
