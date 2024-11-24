# Web Crawler
# Downloads the HTML of a specified source URL.
# Recursively get HTML content from sub URLs found in the resulting page.
# Allows control over the depth of the crawl, the number of URLs to process at each level, and URL uniqueness across levels.

import os
import sys

from scraper import Page, get_page, extract_link


FOLDER_PATH: str = "tests"


def save_page(page: Page) -> bool:
    """Save html page into `depth/name.html`.

    Args:
        page (Page): Web page.

    Returns:
        bool: If saved.
    """
    if FOLDER_PATH not in os.listdir():
        os.mkdir(FOLDER_PATH)
    os.chdir(FOLDER_PATH)

    if page.str_depth not in os.listdir():
        os.mkdir(page.str_depth)
    os.chdir(page.str_depth)

    with open(f"{page.name}.html", "w", encoding="utf-8") as file:
        file.write(page.content)

    os.chdir("..")
    os.chdir("..")

    return True


def crawl(url: str, max_urls: int, depth: int, uniqueness: bool, parents: Page | None = None, all_pages: set = set()) -> None:
    """Web crawler recursively.

    Args:
        url (str): Url to download.
        max_urls (int): Max of unique URLs to extract from each page.
        depth (int): How deep the crawler should run.
        uniqueness (bool): Indicating whether URLs should be unique across different levels.
        parents (Page | None, optional): The `parent` web page. Defaults to None.
        all_pages (set): All saved pages links.
    """
    page: Page = get_page(url, parents)

    if page.depth == depth + 1:
        return

    save_page(page)

    if uniqueness:
        all_pages.add(page.url)

    for sub_link in extract_link(page):
        if sub_link not in page.all_sub_links and sub_link not in all_pages:
            page.all_sub_links.append(sub_link)

            if uniqueness:
                all_pages.add(sub_link)

        if len(page.all_sub_links) == max_urls:
            break

    for sub_link in page.all_sub_links:
        crawl(sub_link, max_urls, depth, uniqueness, page, all_pages)


def main(args: list[str]) -> None:
    """Get args from commend-line and start the crawler.

    Args:
        args (list[str]): Argument from commend-line.

    Raises:
        TypeError: If argument missing.
    """
    print("Start...")

    if len(args) != 5:
        raise TypeError(
            "Missing required argument \n(python crawler.py <url> <max_urls> <depth_factor> <uniqueness_flag>).")

    url: str = args[1]
    max_urls: int = int(args[2])
    depth: int = int(args[3])

    if args[4].lower() == "true":
        uniqueness: bool = True
    else:
        uniqueness: bool = False

    crawl(url, max_urls, depth, uniqueness)

    print("Done!")


if __name__ == "__main__":
    # main(['crawler.py', 'https://www.wikipedia.org/', '5', '2', 'True'])
    main(sys.argv)
