"""
Абстрактный класс пагинатора, наследуемый классом реализации с конкретным представлением.
"""


class Pager:
    """
    Абстрактный класс пагинатора, наследуемый классом реализации с конкретным представлением.
    :param view: Объект представления.
    :param items_per_page: Количество элементов на странице.
    :param links_count: Количество видимых ссылок слева и справа от текущей страницы.
    :param get_params: Дополнительные параметры, которые необходимо передавать по ссылкам.
    :param counter_param: Название GET-параметра, через который передаётся номер текущей страницы.
    """
    def __init__(self, view, items_per_page: int = 10, links_count: int = 3, get_params: str | None = None,
                 counter_param: str = 'page'):
        self.view = view  # В оригинале — объект ISPager.View. Здесь же — ISPager.ItemsRange.
        self.parameters = get_params
        self.counter_param = counter_param
        self.links_count = links_count
        self.items_per_page = items_per_page

    def getItemsCount(self) -> int:
        """
        Количество элементов (строк).
        """
        pass

    def getItems(self, *args):
        """
        Элементы выборки для текущей страницы.
        """
        pass

    def getVisibleLinkCount(self) -> int:
        """
        Количество видимых ссылок слева и справа от текущей страницы.
        """
        return self.links_count

    def getParameters(self) -> str:
        """
        Дополнительные параметры, которые необходимо передавать по ссылкам.
        """
        return self.parameters

    def getCounterParam(self) -> str:
        """
        Название GET-параметра, через который передаётся номер текущей страницы.
        """
        return self.counter_param

    def getItemsPerPage(self) -> int:
        """
        Количество элементов на странице.
        """
        return self.items_per_page

    def getCurrentPage(self, _get: dict) -> int:
        """
        Номер текущей страницы.
        :param _get: Словарь (либо QueryDict) request.GET.
        """
        if self.getCounterParam() in _get:
            return int(_get.get(self.getCounterParam()))
        return 1

    def getPagesCount(self) -> int:
        """
        Количество страниц.
        """
        total = self.getItemsCount()
        result = total // self.getItemsPerPage()  # int
        if (total / self.getItemsPerPage()) - result != 0:
            result += 1
        return result

    def render(self) -> str:
        """
        Строка с постраничной навигацией.
        """
        return self.view.render(self)

    def __str__(self) -> str:
        return self.render()
