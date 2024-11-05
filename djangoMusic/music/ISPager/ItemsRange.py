from .Pager import Pager


class ItemsRange:
    def __init__(self, request):
        super().__init__()
        self.request = request
        self.pager: Pager

    def link(self, title: str, current_page: int = 1) -> str:
        return (f'<a href="{self.request.path}?'
                f'{self.pager.getCounterParam()}={current_page}{self.pager.getParameters()}">{title}</a>')

    @staticmethod
    def range(first: int, second: int) -> str:
        return f'[{first}–{second}]'

    def render(self, pager: Pager) -> str:
        self.pager = pager
        return_page = ''
        current_page = self.pager.getCurrentPage(self.request.GET)
        total_pages = self.pager.getPagesCount()
        if current_page - self.pager.getVisibleLinkCount() > 2:
            range_ = self.range(1, self.pager.getItemsPerPage())
            return_page += self.link(range_, 1) + ' …'
            init = current_page - self.pager.getVisibleLinkCount()
            for i in range(init, current_page + 1):
                range_ = self.range(
                    (i - 1) * self.pager.getItemsPerPage() + 1,
                    i * self.pager.getItemsPerPage()
                )
                return_page += ' ' + self.link(range_, i)
        else:
            for i in range(1, current_page):
                range_ = self.range(
                    (i - 1) * self.pager.getItemsPerPage() + 1,
                    i * self.pager.getItemsPerPage()
                )
                return_page += ' ' + self.link(range_, i)
        if current_page + self.pager.getVisibleLinkCount() + 1 < total_pages:
            cond = current_page + self.pager.getVisibleLinkCount()
            for i in range(current_page, cond + 1):
                if current_page == i:
                    return_page += ' ' + self.range(
                        (i - 1) * self.pager.getItemsPerPage() + 1,
                        i * self.pager.getItemsPerPage()
                    )
                else:
                    range_ = self.range(
                        (i - 1) * self.pager.getItemsPerPage() + 1,
                        i * self.pager.getItemsPerPage()
                    )
                    return_page += ' ' + self.link(range_, i)
            range_ = self.range(
                (total_pages - 1) * self.pager.getItemsPerPage() + 1,
                self.pager.getItemsCount()
            )
            return_page += ' … ' + self.link(range_, total_pages)
        else:
            for i in range(current_page, total_pages + 1):
                if total_pages == i:
                    if current_page == i:
                        return_page += ' ' + self.range(
                            (i - 1) * self.pager.getItemsPerPage() + 1,
                            self.pager.getItemsCount()
                        )
                    else:
                        range_ = self.range(
                            (i - 1) * self.pager.getItemsPerPage() + 1,
                            self.pager.getItemsCount()
                        )
                        return_page += ' ' + self.link(range_, i)
                else:
                    if current_page == i:
                        return_page += ' ' + self.range(
                            (i - 1) * self.pager.getItemsPerPage() + 1,
                            i * self.pager.getItemsPerPage()
                        )
                    else:
                        range_ = self.range(
                            (i - 1) * self.pager.getItemsPerPage() + 1,
                            i * self.pager.getItemsPerPage()
                        )
                        return_page += ' ' + self.link(range_, i)
        return return_page
