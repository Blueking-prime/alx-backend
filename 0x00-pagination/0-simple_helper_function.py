#!/usr/bin/env python3
'''Returns page index ranges'''
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''return a tuple of size two containing a start index and an end index'''
    if page < 1:
        return (0, 0)
    return ((page - 1) * page_size, page * page_size)
