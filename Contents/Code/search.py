def search_anime(type, results, media, lang):
    query = media.show if type == 'tv' else media.name
    query = String.Quote(query)
    # if media.year is not None:
    #     query += ' (' + media.year + ')'

    query = '''
    query {
        Media (search: "''' + query + '''", type: ANIME) {
            id
            title {
                romaji
            }
            startDate {
                year
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
    except:
        Log.Error('Error searching AniList - Anime: ' + query)
        return
    result = JSON.ObjectFromString(request.content)

    results.Append(MetadataSearchResult(
        id = str(result['data']['Media']['id']),
        name = result['data']['Media']['title']['romaji'],
        year = result['data']['Media']['startDate']['year'],
        score = 100,
        lang = lang
    ))