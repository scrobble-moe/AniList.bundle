from datetime import datetime
from anilist import get_anime, get_anime_kitsu, get_episodes_kitsu

def update_anime(type, metadata, media, force):
    result = JSON.ObjectFromString(get_anime(metadata.id))

    anime = result['data']['Page']['media'][0]

    kitsu = JSON.ObjectFromString(get_anime_kitsu(anime['idMal']))

    kitsu_episodes = JSON.ObjectFromString(get_episodes_kitsu(kitsu['included'][0]['id']))

    if metadata.genres is None or force:
        metadata.genres = anime['genres']

    if (metadata.rating is None or force) and anime['averageScore'] is not None:
        metadata.rating = float(anime['averageScore']) / 10

    if (metadata.title is None or force) and anime['title'] is not None:
        title_language = Prefs['title_language']
        if title_language == 'romaji' and anime['title']['romaji'] is not None:
            metadata.title = anime['title']['english']
        elif title_language == 'english' and anime['title']['english'] is not None:
            metadata.title = anime['title']['english']
        elif title_language == 'native' and anime['title']['native'] is not None:
            metadata.title = anime['title']['english']
        elif anime['title']['romaji'] is not None:
            metadata.title = anime['title']['romaji']
        elif anime['title']['english'] is not None:
            metadata.title = anime['title']['english']
        else:
            metadata.title = anime['title']['romaji']
        

    if (metadata.summary is None or force) and anime['description'] is not None:
        metadata.summary = anime['description']

    if (metadata.originally_available_at is None or force) and anime['startDate'] is not None:
        start_date = datetime(anime['startDate']['year'], anime['startDate']['month'], anime['startDate']['day'])
        metadata.originally_available_at = start_date

    if (metadata.content_rating is None or force) and kitsu['included'][0]['attributes']['ageRating'] is not None:
        metadata.content_rating = kitsu['included'][0]['attributes']['ageRating']

    if (metadata.studio is None or force) and len(anime['studios']['edges']):
        anime_studio = anime['studios']['edges'][0]

        if anime_studio is not None:
                metadata.studio = anime_studio['node']['name']

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
            banner_image = anime['bannerImage']
            try:
                thumbnail = Proxy.Preview(HTTP.Request(
                    banner_image, immediate = True
                ).content)
                metadata.banners[banner_image] = thumbnail
            except:
                Log.Error('Error loading banner - Anime: ' + metadata.id)

    # try:
    #     update_episodes(media, metadata, force, anime)
    # except:
    #     Log.Error('Not updating episodes')
    #     return

# def update_episodes(media, metadata, force, anime):
#     for number in media.seasons[1].episodes:
#         number = int(number)
#         episode = metadata.seasons[1].episodes[number]
#         Log.Error(kitsu_episodes['data'][number])

        # if anime['format'] == 'MOVIE':
        #     if (episode.title is None or force) and metadata.title is not None:
        #         episode.title = metadata.title

        #     if (episode.thumbs is None or force) and anime['coverImage'] is not None:
        #         poster_image = anime['coverImage']
        #         try:
        #             thumbnail = Proxy.Preview(HTTP.Request(
        #                 poster_image['medium'], immediate = True
        #             ).content)
        #             episode.thumbs[poster_image['extraLarge']] = thumbnail
        #         except:
        #             Log.Error('Error loading poster - Anime: ' + metadata.id)

        # if (episode.summary is None or force) and metadata.summary is not None:
        #     episode.summary = metadata.summary

        # if (episode.originally_available_at is None or force):
        #     if metadata.originally_available_at is not None:
        #         episode.originally_available_at = metadata.originally_available_at


        

        

            # if (episode.duration is None or force) and metadata.duration is not None:
            #     episode.duration = metadata.duration

            # return

        # ep = find_first(lambda e: e['attributes']['relativeNumber'] == number,
        #     inc_episodes)

        # if ep is None:
        #     ep = find_first(lambda e: e['attributes']['number'] == number, inc_episodes)
        #     if ep is None:
        #         return

        # ep = ep['attributes']

        # if (episode.title is None or force) and ep['canonicalTitle'] is not None:
        #     episode.title = ep['canonicalTitle']

        # if (episode.summary is None or force) and ep['synopsis'] is not None:
        #     episode.summary = ep['synopsis']

        # if (episode.originally_available_at is None or force) and ep['airdate'] is not None:
        #     split = map(lambda s: int(s), ep['airdate'].split('-'))
        #     air_date = datetime(split[0], split[1], split[2])
        #     episode.originally_available_at = air_date

        # if (episode.thumbs is None or force) and ep['thumbnail'] is not None:
        #     thumb_image = ep['thumbnail']['original']
        #     try:
        #         thumbnail = Proxy.Preview(HTTP.Request(thumb_image, immediate = True).content)
        #         episode.thumbs[thumb_image] = thumbnail
        #     except:
        #         Log.Error('Error loading thumbnail - Anime:Episode: ' +
        #             metadata.id + ':' + number)
# DONT THINK THIS IS NEEDED
        # if (episode.duration is None or force) and ep['length'] is not None:
        #     episode.duration = ep['length'] * 60000
