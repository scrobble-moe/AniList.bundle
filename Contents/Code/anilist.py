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
                    coverImage {
                        extraLarge
                        medium
                    }
                    startDate {
                        year
                    }
                    studios {
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


        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')

        # Log.Error(JSON.ObjectFromString(request.content)['data'])

        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')
        # Log.Error('TEST')

        return request.content
    except:
        Log.Error('Error getting anime info')

    

