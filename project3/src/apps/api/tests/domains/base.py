from django.test import SimpleTestCase, Client


class TestDomainBaseView(SimpleTestCase):
    url = None  # need to override in derived classes
    content_type = "application/json"
    client = Client()
    test_links = {"links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "qwe123.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
    ]}
