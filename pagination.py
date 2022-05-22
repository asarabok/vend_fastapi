from math import ceil
from typing import Any, List
from pydantic import BaseModel, conint
import os


class Pagination:
    @classmethod
    def get_total_items(cls, query):
        return query.count()

    @classmethod
    def get_total_items_and_pages(cls, query, page_size):
        total_items = cls.get_total_items(query)
        number_of_pages = int(ceil(total_items / page_size))
        return total_items, number_of_pages

    @classmethod
    def paginate_query(cls, query, current_page, page_size):
        offset = page_size * (current_page - 1)
        return query.offset(offset).limit(page_size)


class PaginationInputModel(BaseModel):
    page: conint(gt=0) = 1
    page_size: conint(gt=0, lt=51) = int(os.environ['PAGE_SIZE'])


class PaginatedMetaModel(BaseModel):
    page: conint(gt=0)
    page_size: conint(gt=0, lt=51)
    num_pages: int
    total_items: int


class PaginatedResponseModel(BaseModel):
    meta: PaginatedMetaModel
    content: List[Any]
