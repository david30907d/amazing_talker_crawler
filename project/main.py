import pprint
from operator import itemgetter

import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed, stop_after_delay, stop_after_attempt


class AmazingTalker(object):
    def __init__(self, lang, page_num_upperbound):
        self._lang = lang
        self._prefix = "https://tw.amazingtalker.com"
        self._url = f"{self._prefix}/tutors/{lang}"
        self._sess = requests.session()
        self._page_num_upperbound = page_num_upperbound
        self._pp = pprint.PrettyPrinter(indent=4)
        self.candidates = []

    @property
    def lang(self):
        return self._lang

    @property
    def url_prefix(self):
        return self._prefix

    @property
    def url(self):
        return self._url

    def url_with_page_num(self, page_num):
        return f"{self.url}?page={page_num}"

    @property
    def sess(self):
        return self._sess

    @property
    def page_num_upperbound(self):
        return self._page_num_upperbound

    @property
    def pp(self):
        return self._pp

    def crawl_every_page(self):
        for page_num in range(1, self.page_num_upperbound):
            if self._crawl_single_page(page_num) == "fail":
                break

    @retry(
        stop=(stop_after_delay(5) | stop_after_attempt(3)), wait=wait_fixed(2),
    )
    def _crawl_single_page(self, page_num):
        resp = self.sess.get(self.url_with_page_num(page_num))
        if resp.status_code != 200:
            raise Exception("fail!")
        html_doc = resp.text
        soup = BeautifulSoup(html_doc, "html.parser")
        if not soup.select("li.at-shadow-box div.book"):
            return "fail"
        self._filter_tutors(
            zip(
                soup.select("li.at-shadow-box div.book"),
                soup.select("li.at-shadow-box div.name-and-rating"),
                soup.select("div.price"),
            )
        )

    def _filter_tutors(self, payloads) -> None:
        for booking_status, name_and_rating, price in payloads:
            if booking_status.text == "預約立即體驗" or True:
                self.candidates.append(
                    {
                        "name": name_and_rating.text,
                        "url": f"{self.url_prefix}{name_and_rating.find('a')['href']}",
                        "price": int(price.text[3:].replace(",", "")),
                    }
                )

    def sort_tutors(self) -> "AmazingTalker":
        self.candidates = sorted(self.candidates, key=itemgetter("price"))
        return self

    def show_tutors(self):
        self.pp.pprint(self.candidates)


if __name__ == "__main__":
    a = AmazingTalker(lang="japanese", page_num_upperbound=50)
    a.crawl_every_page()
    a.sort_tutors().show_tutors()

    a = AmazingTalker(lang="english", page_num_upperbound=50)
    a.crawl_every_page()
    a.sort_tutors().show_tutors()
