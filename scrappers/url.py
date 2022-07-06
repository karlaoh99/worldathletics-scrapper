from __future__ import annotations
from typing import Any


class URL(object):

    def __init__(self, url: str) -> None:
        self.url = url
    
    def add_param(self, name: str, value: Any) -> URL:
        final_url = self.url
        value = str(value)
        if '?' not in final_url:
            final_url += '?'
        if not final_url.endswith('?'):
            final_url += '&'
        final_url += f'{name}={value}'
        return URL(final_url)
    
    def __add__(self, other):
        if isinstance(other, str):
            return URL(self.url + other)
        if isinstance(other, URL):
            return URL(self.url + other.url)
        raise ValueError("Invalid operation between 'URL' and "
                         f"{type(other).__name__}")

    def __str__(self):
        return self.url
    
    def __repr__(self):
        return 'URL: ' + self.url
