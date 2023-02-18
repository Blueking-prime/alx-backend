#!/usr/bin/env python3
'''Returns page index ranges'''
import csv
from math import ceil
from typing import Dict, List, Tuple, Union


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''return a tuple of size two containing a start index and an end index'''
    if page < 1:
        return (0, 0)
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''Gets a page of the dataset'''
        assert type(page) == int and page > 0
        assert type(page_size) == int and page_size > 0
        start, end = index_range(page, page_size)
        try:
            return self.dataset()[start: end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) \
            -> Dict[str, Union[int, List, None]]:
        '''returns a context page'''
        curr_page = self.get_page(page, page_size)
        total_pages = ceil(len(self.dataset()) / page_size)
        return {
            'page_size': len(curr_page),
            'page': page,
            'data': curr_page,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_page': total_pages
        }
