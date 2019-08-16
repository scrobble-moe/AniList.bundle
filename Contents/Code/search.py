def search_anime(type, results, media, lang):
    query = media.show if type == 'tv' else media.name
    query = String.Quote(query)

    if query.isdigit():
        query = '''
            query {
                anime: Page (perPage: 8) {
                    pageInfo {
                        total
                    }
                    results: media (type: ANIME, id: ''' + query + ''') {
                        id
                        title {
                            romaji
                        }
                        startDate {
                            year
                        }
                    }
                }
            }
        '''

    else:
        query = '''
            query {
                anime: Page (perPage: 8) {
                    pageInfo {
                        total
                    }
                    results: media (type: ANIME, search: "''' + query + '''") {
                        id
                        title {
                            romaji
                        }
                        startDate {
                            year
                        }
                    }
                }
            }
        '''

    Log.Error(query)

    request = HTTP.Request(
        'https://graphql.anilist.co',
        values = {'query': query},
        method = "POST"
    )


    try:
        request.load()
    except:
        Log.Error('Error searching AniList - Anime: ' + query)
        return

    s = 100
    for result in JSON.ObjectFromString(request.content)['data']['anime']['results']:
        results.Append(MetadataSearchResult(
            id = str(result['id']),
            name = result['title']['romaji'],
            year = result['startDate']['year'],
            score = s,
            lang = lang
        ))
        s = s - 1
    return
    