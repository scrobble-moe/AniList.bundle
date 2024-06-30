from time import sleep
import certifi
import requests

def get_anime(id):
    query = '''
        query {
            Page {
                media(id: ''' + id + ''') {
                    genres
                    duration
                    episodes
                    averageScore
                    description
                    format
                    idMal
                    season
                    seasonYear
                    countryOfOrigin
                    bannerImage
                    coverImage {
                        extraLarge
                        medium
                    }
                    tags {
                        name
                    }
                    reviews {
                        edges {
                            node {
                                score
                                siteUrl
                                summary
                                user {
                                    name
                                    avatar {
                                        large
                                    }
                                }
                            }
                        }
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
                            voiceActors(language: ''' + str(Prefs['va_language']).upper() + ''') {
                                name {
                                    full
                                }
                                image {
                                    large
                                }
                            }
                        }
                    }
                }
            }
        }
    '''

    try:
        sleep(1)
        return requests.post(
            'https://graphql.anilist.co',
            data={'query': query},
            verify=certifi.where()
        ).content
    except:
        Log.Error('Error getting anime info')
    return


def get_episodes(id):
    sleep(4) #TODO: Rate limit FIX
    anime_episodes = {}
    page = 1
    has_next_page = True
    try:
        while has_next_page:
            episodes = get_episode_data(id, page)
            has_next_page = episodes['pagination']['has_next_page']
            page += 1
            for episode in episodes['data']:
                if not episode['recap']:
                    anime_episodes[episode['mal_id']] = episode
        return anime_episodes
    except:
        Log.Error('Error getting mal data')
    return

def get_episode_data(id, page):

    mal_request = requests.get(
        'https://api.jikan.moe/v4/anime/' + id + '/episodes?page=' + str(page),
        verify=certifi.where()
    ).content
    return JSON.ObjectFromString(mal_request)
