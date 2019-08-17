def search_anime(type, results, media, lang):
    search_term = media.show if type == 'tv' else media.name
    search_year = media.year
    if media.year is None:
        search_year = 'null'

    query = '''
    query ($id: Int, $perPage: Int, $search: String, $seasonYear: Int) {
        anime: Page(perPage: $perPage) {
            pageInfo {
                total
            }
            results: media(type: ANIME, id: $id, search: $search seasonYear: $seasonYear) {
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

    if search_term.isdigit():
        variables = '''{
            "id": "'''+ search_term +'''",
            "perPage": 3
        }'''
    else: 
        variables = '''{
            "search": "'''+ search_term +'''",
            "perPage": 3,
            "seasonYear": '''+ str(search_year) +'''
        }'''

    request = HTTP.Request(
        'https://graphql.anilist.co',
        values = {'query': query, 'variables': variables},
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
    