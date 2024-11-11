"""
Класс интервального представления номеров страниц в строке навигации.
Пример для 35-и элементов по 10 на странице:
[1–10] [11–20] [21–30] [31–35]
"""
from .Pager import Pager


class ItemsRange:
    """
    Класс интервального представления номеров страниц в строке навигации.
    Пример для 35-и элементов по 10 на странице:
    [1–10] [11–20] [21–30] [31–35]
    :param request: Объект django.http.request.
    """
    def __init__(self, request):
        self.request = request
        self.pager: Pager

    def link(self, title: str, current_page: int = 1) -> str:
        """
        Элемент панели навигации (ссылки).
        :param title: Текст ссылки.
        :param current_page: Номер страницы, для которой строиться ссылка.
        """
        # В оригинале этот метод находится в родительском абстрактном классе View, от которого наследуются и другие
        # классы представлений. Для данного проекта такое выделение не требуется.
        params = self.pager.getParameters()
        return (f'<a href="{self.request.path}?'
                f'{self.pager.getCounterParam()}={current_page}{'&' if params else ''}{params}">{title}</a>')

    @staticmethod
    def range(first: int, last: int) -> str:
        """
        Текст с интервалом.
        :param first: Номер первого в интервале элемента.
        :param last: Номер последнего в интервале элемента.
        """
        return f'[{first}–{last}]'

    def render(self, pager: Pager) -> str:
        """
        Панель навигации.
        :param pager: Объект ISPager.Pager.
        """
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
