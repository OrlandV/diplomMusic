class Pager:
    def __init__(self, view, items_per_page: int = 10, links_count: int = 3, get_params: str | None = None,
                 counter_param: str = 'page'):
        self.view = view
        self.parameters = get_params
        self.counter_param = counter_param
        self.links_count = links_count
        self.items_per_page = items_per_page

    def getItemsCount(self) -> int:
        pass

    def getItems(self, *args):
        pass

    def getVisibleLinkCount(self) -> int:
        return self.links_count

    def getParameters(self) -> str:
        return self.parameters

    def getCounterParam(self) -> str:
        return self.counter_param

    def getItemsPerPage(self) -> int:
        return self.items_per_page

    # def getCurrentPagePath(self, path: str):
    #     # Добавил для данного проекта .replace('/search.html', '/')
    #     return path.replace('/index.html', '/').replace('/search.html', '/')

    def getCurrentPage(self, _get) -> int:
        if self.getCounterParam() in _get:
            return int(_get.get(self.getCounterParam()))
        return 1

    def getPagesCount(self) -> int:
        total = self.getItemsCount()
        result = total // self.getItemsPerPage()  # int
        if (total / self.getItemsPerPage()) - result != 0:
            result += 1
        return result

    def render(self) -> str:
        return self.view.render(self)

    def __str__(self) -> str:
        return self.render()
