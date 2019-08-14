from datetime import datetime

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
                            voiceActors {
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

    request = HTTP.Request(
        'https://graphql.anilist.co',
        values = {'query': query},
        method = "POST"
    )
    try:
        request.load()

        return request.content
    except:
        Log.Error('Error getting anime info')

def get_anime_kitsu(id):
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }

    kitsuRequest = HTTP.Request(
        'https://kitsu.io/api/edge/mappings?filter[externalSite]=myanimelist/anime&filter[externalId]=' + str(id) + '&include=item',
        headers = headers
    )
    try:
        kitsuRequest.load()
        return kitsuRequest.Content
    except:
        Log.Error('Error getting anime info')

def get_episodes_kitsu(id):
    headers = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json'
    }

    kitsuRequest = HTTP.Request(
        'https://kitsu.io/api/edge/anime/' + str(id) + '/episodes',
        headers = headers
    )
    try:
        kitsuRequest.load()
        return kitsuRequest.content
    except:
        Log.Error('Error getting anime info')
