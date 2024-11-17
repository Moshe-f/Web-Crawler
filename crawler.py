# Web Crawler
# Downloads the HTML of a specified source URL.
# Recursively get HTML content from sub URLs found in the resulting page.
# Allows control over the depth of the crawl, the number of URLs to process at each level, and URL uniqueness across levels.

import os
import sys

from scraper import Page, get_page, extract_links


FOLDER_PATH: str = "tests2"


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


def crawl(url: str, max_urls: int, depth: int, uniqueness: bool, parents: Page | None = None) -> None:
    """Web crawler recursively.

    Args:
        url (str): Url to download.
        max_urls (int): Max of unique URLs to extract from each page.
        depth (int): How deep the crawler should run.
        uniqueness (bool): _description_
        parents (Page | None, optional): Indicating whether URLs should be unique across different levels. Defaults to None.
    """
    page: Page = get_page(url, parents)

    if page.depth == depth + 1:
        return

    save_page(page)
    all_links: list[str] = extract_links(page, max_urls)
    page.all_sub_links.extend(all_links)

    for sub_link in page.all_sub_links:
        crawl(sub_link, max_urls, depth, uniqueness, page)


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

    if args[4].lower() == "true":  # In progress.
        uniqueness: bool = True  # In progress.
    else:
        uniqueness: bool = False  # In progress.

    crawl(url, max_urls, depth, uniqueness)

    print("Done!")


if __name__ == "__main__":
    # main(['crawler.py', 'https://www.wikipedia.org/', '5', '2', 'False'])
    main(sys.argv)
