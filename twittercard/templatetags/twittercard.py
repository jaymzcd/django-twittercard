from django import template
from django.conf import settings
register = template.Library()


def get_twittercard_attributes(card_type, **kwargs):
    """
        Create a dictionary with our base card data

        :param card: the name/type of card
        :param kwargs: meta attributes for this card
        :type card: str
        :type kwargs: dict
    """
    card = {}
    card['card'] = card_type
    card['title'] = kwargs.get('title', None)
    card['description'] = kwargs.get('description', None)
    card['image'] = kwargs.get('image', None)
    config = getattr(settings, 'TWITTERCARD_CONFIG', None)
    if config is not None:
        card['site'] = kwargs.get('site', config.get('SITE', None))
        card['site_id'] = kwargs.get('site_id', config.get('SITE_ID', None))
        card['creator'] = kwargs.get('creator', config.get('CREATOR', None))
        card['creator_id'] = kwargs.get('creator_id', config.get('CREATOR_ID', None))
    return card


def twittercard_summary(context, *args, **kwargs):
    """
        A summary card - the standard one
    """
    card = get_twittercard_attributes('summary', **kwargs)
    request = context['request']
    card['url'] = kwargs.get('url', request.build_absolute_uri())
    return card
register.inclusion_tag('twittercard/summary.html', takes_context=True)(twittercard_summary)


def twittercard_photo(context, *args, **kwargs):
    """
        A photo card
    """
    card = get_twittercard_attributes('photo', **kwargs)
    card['image_width'] = kwargs.get('image_width', None)
    card['image_height'] = kwargs.get('image_height', None)
    return card
register.inclusion_tag('twittercard/photo.html', takes_context=True)(twittercard_photo)


def twittercard_product(context, *args, **kwargs):
    """
        A product specific card including price data
    """
    card = get_twittercard_attributes('product', **kwargs)
    card['price'] = kwargs.get('price', None)
    card['location'] = kwargs.get('location', None)
    return card
register.inclusion_tag('twittercard/product.html', takes_context=True)(twittercard_product)
