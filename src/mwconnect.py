import requests

class Connection:
    S: requests.Session

    def __init__(self) -> None:
        self.S = requests.Session()

    def get_page_raw(self, wiki: str, page: str) -> requests.Response:
        base = "https://{}/wiki/{}?action=raw"
        url = base.format(wiki, page)
        return self.S.get(url)

    def get_page(self, wiki_api: str, page: str) -> requests.Response:
        URL = wiki_api
        PARAMS = {
            "action": "query",
            "prop": "revisions",
            "titles": f"{page}",
            "rvprop": "content",
            "rvslots": "main",
            "formatversion": "2",
            "format": "json"
        }
        return self.S.get(url=URL, params=PARAMS)

    def get_pages(self, wiki_api: str, pages: list[str]) -> requests.Response:
        URL = wiki_api
        PARAMS = {
            "action": "query",
            "prop": "revisions",
            "titles": f"{'|'.join(pages)}",
            "rvprop": "content",
            "rvslots": "main",
            "formatversion": "2",
            "format": "json"
        }
        return self.S.get(url=URL, params=PARAMS)

    #

