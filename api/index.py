from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Compose


@register(Compose)
class ComposeModelIndex(AlgoliaIndex):
    fields = ('title', 'description', 'composer', 'image', 'compose_date')
    settings = {'searchableAttributes': ['title'],
                'hitsPerPage': 15,
                'attributesForFaceting': ['composer'],
                }
    index_name = 'personal_diary'
