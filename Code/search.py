import certifi
import requests
import re


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
    if Prefs['folder_id']:
        variables = '''{
            "id": "'''+ re.match('(.*?) - ', search_term).group(1) +'''"
        }'''
    elif search_term.isdigit():
        variables = '''{
            "id": "'''+ search_term +'''"
        }'''
    else: 
        variables = '''{
            "search": "'''+ search_term +'''",
            "perPage": 6,
            "seasonYear": '''+ str(search_year) +'''
        }'''

    try:
        request = requests.post(
            'https://graphql.anilist.co',
            data = {'query': query, 'variables': variables}
        )
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
    