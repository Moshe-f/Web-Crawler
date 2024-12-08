# !!!DO NOT USE!!!
# Using this crawler may result in your IP address being blocked from Wikipedia!!!
# https://en.wikipedia.org/wiki/Wikipedia:Database_download#Please_do_not_use_a_web_crawler
# https://en.wikipedia.org/wiki/Wikipedia:Database_download#Sample_blocked_crawler_email
# This crawler is simple and very slow!!!
# To create a program that searches in a proper way, you need to create and use in local copy of `Wikipedia dump DB`.

# Wiki game
# https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game
# Finds the best path between two wiki pages(`English Wikipedia` only).
# To change to other wikipedia languages change BASE_WIKI to the base wikipedia url ("https://<language code>.wikipedia.org/").

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys

from scraper import Page, get_page, extract_link


BASE_WIKI: str = "https://en.wikipedia.org/"
ANSWER_PATH: str = "wiki_chain.txt"


def path_finder(start_url: str, end_url: str) -> Page:
    """Path finder.

    Args:
        start_url (str): Url to start from.
        end_url (str): Url to find.

    Returns:
        Page: End page.
    """
    start_page: Page = get_page(start_url)
    all_links: set = {start_url}
    all_pages: list[Page] = [start_page]
    
    for page in all_pages:
        for sub_link in extract_link(page):
            if sub_link not in all_links and sub_link.startswith(BASE_WIKI):
                sub_page: Page = get_page(sub_link, page)
                if sub_link == end_url:
                    return sub_page
                all_links.add(sub_link)
                all_pages.append(sub_page)


def crawl_back(page: Page) -> str:
    """Return the path.

    Args:
        page (Page): End page.

    Returns:
        str: Path.
    """
    path: list[str] = []
    if page is None:
        return "Path does not found!"
    while page.parent is not None:
        path.append(page.url)
        page = page.parent
    path.append(page.url)
    return " -> ".join(path[::-1])


def main(args: list[str]) -> None:
    """Get args from commend-line and start the search.

    Args:
        args (list[str]): Argument from commend-line.

    Raises:
        TypeError: If argument missing.
    """
    print("Start searching...")

    if len(args) != 3:
        raise TypeError(
            "Missing required argument \n(python wiki_game.py <start_url> <stop_url>.")

    start_url: str = args[1]
    end_url: str = args[2]

    found_page: Page = path_finder(start_url, end_url)
    path: str = crawl_back(found_page)
    print(path)


if __name__ == "__main__":
    # main(['wiki_game.py', 'https://en.wikipedia.org/wiki/Financial_crisis', 'https://en.wikipedia.org/wiki/Client_(business)'])
    main(sys.argv)
