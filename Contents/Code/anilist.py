from datetime import datetime
import certifi
import requests

def get_anime(id):
    query = '''
        query {
            Page {
                media(id: ''' + id + ''') {
                    genres
                    episodes
                    averageScore
                    description
                    format
                    idMal
                    countryOfOrigin
                    bannerImage
                    coverImage {
                        extraLarge
                        medium
                    }
                    staff {
                        edges {
                        node {
                            name {
                            full
                            }
                            image {
                            large
                            }
                        }
                        role
                        }
                    }
                    startDate {
                        day
                        month
                        year
                    }
                    studios(isMain: true) {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                    title {
                        romaji
                        english
                        native
                    }
                    status
                    characters {
                        edges {
                            node {
                                name {
                                    full
                                }
                                image {
                                    large
                                }
                            }
                            role
                            voiceActors(language: ''' + Prefs['va_language'] + ''') {
                                name {
                                    full
                                }
                                image {
                                    large
                                }
                                language
                            }
                        }
                    }
                }
            }
        }
    '''

    try:
        return requests.post(
            'https://graphql.anilist.co',
            data = {'query': query}
        ).content
    except:
        Log.Error('Error getting anime info')
    return

def get_anime_kitsu(id):
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }

    try:
        return requests.get(
            'https://kitsu.io/api/edge/mappings?filter[externalSite]=myanimelist/anime&filter[externalId]=' + id + '&include=item',
            headers = headers
        ).content
    except:
        Log.Error('Error getting kitsu data')
    return

def get_episodes_kitsu(id):
    anime_episodes = {}

    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }
    try:
        kitsuRequest = requests.get(
            'https://kitsu.io/api/edge/anime/' + id + '/relationships/episodes',
            headers = headers
        ).content
        episodes = JSON.ObjectFromString(kitsuRequest)

        for episode in episodes['data']:
            episodeRequest = requests.get(
                'https://kitsu.io/api/edge/episodes/' + episode['id'] + '?fields[episodes]=synopsis,canonicalTitle,relativeNumber,number,airdate',
                headers = headers
            ).content
            episode = JSON.ObjectFromString(episodeRequest)

            if episode['data']['attributes']['relativeNumber']:
                anime_episodes[episode['data']['attributes']['relativeNumber']] = episode['data']
            else: anime_episodes[episode['data']['attributes']['number']] = episode['data']

        return anime_episodes
    except:
        Log.Error('Error anime episodes info')
    return