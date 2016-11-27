from django import template
from os.path import exists

from Elodin.settings import LOCK_FILE

register = template.Library()


@register.simple_tag
def server_running():
    return exists(LOCK_FILE)