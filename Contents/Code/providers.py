from datetime import datetime
from time import sleep
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
            data = {'query': query},
            verify=certifi.where()
        ).content
    except:
        Log.Error('Error getting anime info')
    return

def get_episodes(id):
    sleep(4)
    anime_episodes = {}

    mal_request = requests.get(
        'https://api.jikan.moe/v3/anime/' + id + '/episodes',
        verify=certifi.where()
    ).content
    episodes = JSON.ObjectFromString(mal_request)

    try:
        mal_request = requests.get(
            'https://api.jikan.moe/v3/anime/' + id + '/episodes',
            verify=certifi.where()
        ).content
        episodes = JSON.ObjectFromString(mal_request)

        for episode in episodes['episodes']:
            if not episode['recap']:
                anime_episodes[episode['episode_id']] = episode
                
        return anime_episodes
    except:
        Log.Error('Error getting mal data')
    return