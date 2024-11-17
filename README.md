# Web Crawler

## Status
![Status](https://img.shields.io/badge/status-in%20progress-yellow)

🚧 **Work in Progress** 🚧  
This project is currently under development. Features and documentation may change frequently.

## Description

A web crawler program that:
- Downloads the HTML of a specified source URL.
- Recursively get HTML content from sub URLs found in the resulting page.
- Allows control over the depth of the crawl, the number of URLs to process at each level, and URL uniqueness across levels.

### Program arguments

The program accepts the following command-line arguments:
1. **URL**: The starting URL for the crawl.
2. **Max URLs**: Maximum number of unique URLs to extract from each page.
3. **Depth Factor**: How deep the crawler should run.
4. **Uniqueness Flag**: A Boolean flag (`True` or `False`) indicating whether URLs should be unique across different levels.

### Output

Each HTML page is saved as a file with a naming convention structured by depth level:
- Files are stored under `<depth>/<name>.html`, where:
  - `<depth>` is the level of recursion (`0`, `1`, `2`).
  - `<name>` is the URL where non-allowed characters are replaced with underscores.

### Example

**Input**:
- **URL**: `https://www.wikipedia.org/`
- **Max URLs**: `5`
- **Depth Factor**: `2`
- **Uniqueness Flag**: `True`

**Output**:
1. **Depth 0**: 
   - Download and save the HTML of `https://www.wikipedia.org/` to `0/https___www_wikipedia_org.html`.
   - Extract up to 5 unique URLs from this page for the next depth level.
   
2. **Depth 1**:
   - Download and save HTML content of the 5 URLs found in Depth 0 to files under `1/<file-name>.html`.
   - Extract up to 5 unique URLs from this page for Depth 2.
   - Ensure URLs are unique across Depth 0 and Depth 1 due to the `Uniqueness Flag` being set to `True`.
   
3. **Depth 2**:
   - Download up to 25 unique URLs (5 per page) from Depth 1, saving each HTML file to `2/<file-name>.html`.
   - The crawl stop here as the specified Depth Factor is 2.

### Running the Program

To run the program, execute:
```
python crawler.py <url> <max_urls> <depth_factor> <uniqueness_flag>
```

Example Command:
```
python crawler.py https://www.wikipedia.org/ 5 2 true
```

## Requirements
1. Python 3.x
2. requests
3. beautifulsoup4
