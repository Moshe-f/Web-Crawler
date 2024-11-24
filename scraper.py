# Web Scraper
# Get and downloads HTML from the web.
# Extract links from HTML content.
# Allows control over the number of URLs to extract.


from string import digits, ascii_letters
from typing import Generator

from bs4 import BeautifulSoup
import requests
from urllib.parse import unquote, urljoin, urlparse


class Page:
    """A Web Page class.
    
    Args:
        url (str): Web page url.
        content (str): Content of the HTML.
        parent (Page | None, optional): The `parent` web page. Defaults to None.

    Attributes:
        url (str): Web page url.
        name (str): Web page name (url with non-allowed characters replaced with underscores).
        content (str): Content of the HTML.
        parent (Page | None): The `parent` web page.
        all_sub_links (list[str]): All links inside the content.
        depth (int): Depth of the web page for the original url.
        str_depth (str): Depth in string.
    """

    def __init__(self, url: str, content: str, parent=None) -> None:
        self.url: str = url
        self.name: str = self.set_name(url)
        self.content: str = content
        self.parent: Page|None = parent
        self.all_sub_links: list[str] = []
        self.depth: int = 0
        self.set_depth()
        self.str_depth: str = str(self.depth)

    def set_name(self, url: str) -> str:
        """Set a valid name for the web page 
        (url with non-allowed characters replaced with underscores).

        Args:
            url (str): The web page url.

        Returns:
            str: Valid name.
        """
        name: str = ""
        url: str = unquote(url)
        for letter in url:
            if letter not in digits + ascii_letters:
                letter = "_"
            name += letter
        return name

    def set_depth(self) -> None:
        """Set page depth according to the parent."""
        if self.parent is not None:
            self.depth = self.parent.depth + 1    


def extract_link(page: Page) -> Generator[str, str, str]:
    """Yields sub link from HTML content.

    Args:
        page (Page): Web page.

    Yields:
        Generator[str, str, str]: Sub link in the page.
    """
    soup = BeautifulSoup(page.content, "html.parser")

    for link in soup.find_all("a"):
        link: str = link.get('href')

        if link is None or link.startswith("#") or link.startswith("mailto:") or link.startswith("tel:"):
            continue

        link: str = urljoin(page.url, link)
        link: str = urljoin(link, urlparse(link).path)

        yield link


def extract_links(page: Page, max_urls: int = -1) -> list[str]:
    """Extract links from the HTML content.

    Args:
        page (Page): Web page.
        max_urls (int, optional): Max sub-urls to extract. Defaults to -1 (all urls in the page).

    Returns:
        list[str]: All sub links in the page.
    """
    all_links_in_page: list[str] = []

    for link in extract_link(page):
        if link not in all_links_in_page:
            all_links_in_page.append(link)

        if len(all_links_in_page) == max_urls:
            return all_links_in_page

    return all_links_in_page


def get_page(url: str, parent: Page | None = None) -> Page:
    """Get and download page from the internet.

    Args:
        url (str): Url to download.
        parent (Page | None, optional): Page parent. Defaults to None.

    Returns:
        Page: A Web page.
    """
    source: requests.Response = requests.get(url)
    data: str = source.content.decode(encoding="utf-8", errors="ignore")

    page: Page = Page(url, data, parent)
    
    return page


def main():
    pass


if __name__ == "__main__":
    main()
