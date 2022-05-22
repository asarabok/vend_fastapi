from math import ceil


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
