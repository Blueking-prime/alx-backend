#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""
import csv
from typing import Dict, List, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self,
                        index: Union[int, None] = None,
                        page_size: int = 10) -> Dict[str, Union[int, List]]:
        '''Returns a hyper indexed page'''
        if not index:
            index = 0
        dataset = self.indexed_dataset()
        assert index >= 0 and index < sorted(dataset.keys())[-1]

        data_list = []
        added = 0
        cur_idx = 0
        for i in sorted(dataset.keys()):
            if i >= index:
                data_list.append(dataset[i])
                added += 1
                cur_idx = i
            if added == page_size:
                break

        return {
            'index': index,
            'next_index': cur_idx + 1 if cur_idx else index + page_size,
            'page_size': page_size,
            'data': data_list
        }
