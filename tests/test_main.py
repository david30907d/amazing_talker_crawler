import pytest

from project.main import AmazingTalker


@pytest.fixture
def amazing_talker_obj():
    return AmazingTalker(lang="japanese", page_num_upperbound=2)


def test_crawl_every_page(amazing_talker_obj):
    resp = amazing_talker_obj.crawl_every_page()
    if __debug__:
        if resp:
            raise AssertionError("something wrong in crawl_every_page")


def test_crawl_single_page(amazing_talker_obj):
    resp = amazing_talker_obj._crawl_single_page(1)
    if __debug__:
        if resp:
            raise AssertionError("something wrong in crawl_single_page")


def test_sort_tutors(amazing_talker_obj):
    resp = amazing_talker_obj.sort_tutors()
    if __debug__:
        if not isinstance(resp, AmazingTalker):
            raise AssertionError("something wrong in sort_tutors")


def test_show_tutors(amazing_talker_obj):
    resp = amazing_talker_obj.show_tutors()
    if __debug__:
        if resp:
            raise AssertionError("something wrong in show_tutors")
