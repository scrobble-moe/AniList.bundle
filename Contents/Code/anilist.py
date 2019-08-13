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
                    duration
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

    

