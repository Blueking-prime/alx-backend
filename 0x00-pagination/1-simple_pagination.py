#!/usr/bin/env python3
'''Returns page index ranges'''
import csv
from typing import List


def index_range(page: int, page_size: int) -> tuple[int, int]:
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
