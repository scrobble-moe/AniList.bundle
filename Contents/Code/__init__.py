from search import search_anime
from update import update_anime

EN = Locale.Language.English

def Start():
    HTTP.CacheTime = CACHE_1DAY

class AniListTV(Agent.TV_Shows):
    name = 'AniList'
    languages = [ EN ]
    primary_provider = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        search_anime('tv', results, media, lang)

    def update(self, metadata, media, lang, force):
        update_anime('tv', metadata, media, force)

class AniListMovie(Agent.Movies):
    name = 'AniList'
    languages = [ EN ]
    primary_Provider = True
    fallback_agent = False
    accepts_from = None
    contributes_to = None

    def search(self, results, media, lang, manual):
        search_anime('movie', results, media, lang)

    def update(self, metadata, media, lang, force):
        update_anime('movie', metadata, media, force)
