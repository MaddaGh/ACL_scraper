# file ACL_URLManager 

## Class: `URLManager`

The `URLManager` class provides functionality to:
- Load URLs from either:
  - A `.txt` file containing a list of URLs, or
  - A single URL string.
- Keep track of which URLs have **not yet been parsed**.
- Move processed URLs into a separate list (`parsed_urls`) for tracking.

This is particularly useful when working with batch URL parsing or scraping tasks where progress tracking is required.

---

### Initialization
```python
URLManager(txt_filepath: str)
```
### Parameters:
- `txt_filepath` (`str`): Either:
    - A path to a `.txt` file containing one URL per line, or
    - A single URL string.

### Attributes:
- `txt_filepath` (`str`): Stores the provided file path or URL.
- `urls` (`list[str]`): Active list of URLs to be processed.
- `parsed_urls` (`list[str]`): List of URLs that have been removed from `urls` (already processed).

--- 

## Methods

`_load_urls(self)`
Private helper method called during initialization.
- If txt_filepath starts with "http", treats it as a single URL and stores it.
- If txt_filepath ends with .txt, reads the file and loads all URLs (one per line).
- Raises ValueError if the input is invalid.

---

`get_urls(self) -> list`

Returns the list of currently unprocessed URLs.

```python
urls = url_manager.get_urls()
```

--- 

`get_url_count(self) -> int`

Returns the number of URLs still left to process.

```python
count = url_manager.get_url_count()
```

--- 

`remove_url(self)`

Removes the first URL from `urls` and appends it to `parsed_urls`.

This allows tracking of progress by separating processed URLs from pending ones.

```python
url_manager.remove_url()
print(url_manager.parsed_urls)
```

### Example Usage

```python
# Initialize with a .txt file containing URLs
url_loader = URLManager("path.txt")

# Get list of URLs
print(url_loader.get_urls())

# Get count of URLs
print(url_loader.get_url_count())

# Remove and track first URL
url_loader.remove_url()
print(url_loader.parsed_urls)

# Access original file path
print(url_loader.txt_filepath)

```

## Developer Notes

- File size consideration:
Currently, `_load_urls` reads all lines at once. For very large files, consider replacing it with a generator (line-by-line reading) to reduce memory usage.

---

# file ACL_WebScraper

## Class: `WebScraper`

The `WebScraper` class provides functionality to:
- Validate and fetch a web page from a given URL.
- Parse the HTML content using `BeautifulSoup`.
- Store the parsed HTML in memory for further analysis.

This class is used to scrape structured web pages, in particular conference proceedings from ACL anthology, and prepare them for data extraction.

---

### Initialization
```python
WebScraper(url: str)
```
**Parameters:**
- `url` (`str`): The web page URL to scrape.

**Attributes:**
- `url` (`str`): Stores the provided URL.
- `soup` (`BeautifulSoup | None`): The parsed HTML content (set after calling `parse()`).
- `conference_name` (`str`): Extracted identifier from the URL, e.g., the conference code in ACL Anthology URLs.

---

### Methods

#### `_is_valid_url(self) -> bool`
Private helper method that checks whether the given URL starts with `"http"`.  

**Returns:**  
- `True` if the URL is valid.  
- `False` otherwise.  

---

#### `parse(self) -> bool`
Fetches and parses the HTML content of the provided URL.  

**Process:**
1. Validates the URL format using `_is_valid_url()`.  
2. Sends a GET request with browser-like headers to avoid blocking.  
3. If the request is successful (`status_code == 200`):
   - Stores the parsed HTML in `self.soup`.  
   - Prints a success message.  
   - Returns `True`.  
4. If the request fails or status is not `200`, returns `False`.  

**Exceptions:**  
- Raises `ValueError` if the URL is invalid (does not start with `"http"`).  

---

## Example Usage
```python
# Initialize the scraper with a URL
scraper = WebScraper("https://aclanthology.org/volumes/2023.eacl-main/")

# Access the soup before parsing (None initially)
print(scraper.soup)

# Parse the web page (returns True if successful, False otherwise)
print(scraper.parse())

# Access the parsed HTML (BeautifulSoup object)
print(scraper.soup)

# Optionally save the HTML to a file
with open("html.txt", "w", encoding="utf-8") as output:
    output.write(str(scraper.soup))
```

---

## Developer Notes

- **HTTP Headers:**  
  The scraper uses a custom set of headers (e.g., `User-Agent`, `Referer`) to mimic a real browser and reduce the chance of being blocked. These headers may need to be updated depending on the target site.  

- **Error Handling:**  
  If the request fails (network error, timeout, etc.), a `RequestException` is caught and logged, and `self.soup` is reset to `None`.  

---

# file Data_Extractor 

## Class: `DataExtractor`
The `DataExtractor` class provides functionality to:
- Extract structured bibliographic information and abstracts from HTML content.
- Store the extracted data in a pandas DataFrame.
- Track unresolved or missing bibliographic links.

It is designed to work with HTML content retrieved by the `WebScraper` class, particularly from ACL Anthology conference pages.

---

### Initialization
```python
DataExtractor(html_soup, conference_name, abstract_bool)
```
**Parameters:**
- `html_soup` (`BeautifulSoup`): Parsed HTML content from a web page.
- `conference_name` (`str`): Identifier for the conference (used for tracking or naming).
- `abstract_bool` (`bool`): Flag indicating whether abstracts are found in the HTML .

**Attributes:**
- `html` (`BeautifulSoup`): Stores the HTML content.
- `data` (`pandas.DataFrame | None`): Stores the extracted bibliographic and abstract data.
- `conference_name` (`str`): Name/code of the conference.
- `abs_bool` (`bool`): Indicates if abstracts are found and included in the DataFrame.
- `bib_link_not_found` (`list[str]`): Tracks bibliographic links that could not be resolved.

---

### Methods

#### `extract_data(self) -> bool`
Extracts bibliographic entries and abstracts from the HTML content and compiles them into a pandas DataFrame.

**Process:**
1. Initializes empty DataFrames for bibliographic data (`bibtex_data`) and abstracts (`abstract_data`).  
2. Iterates over `<a>` tags with class `'badge badge-secondary align-middle mr-1'` to find bib links:
   - Sends GET requests for each bib file.
   - Parses key-value pairs from the bib content.
   - Builds a dictionary for each paper and appends it as a row to `bibtex_data`.
   - Tracks any unresolved bib links in `bib_link_not_found`.
3. Iterates over `<div>` elements with class `'card bg-light mb-2 mb-lg-3 collapse abstract-collapse'` to extract abstracts:
   - Matches abstract IDs with regular expressions.
   - Extracts text from the `<div>` with class `'card-body p-3 small'`.
   - Appends abstract data to `abstract_data`.
4. Merges `bibtex_data` and `abstract_data` on the `"ID"` column if abstracts exist.
5. Updates `self.data` with the final DataFrame.
6. Sets `self.abs_bool` to indicate whether abstracts are included.
7. Returns `True` if any data was extracted, `False` if no bib entries were found.

---

## Example Usage
```python
# First, scrape HTML using WebScraper
scraper = WebScraper("https://aclanthology.org/volumes/2023.eacl-main/")
scraper.parse()
html = scraper.soup

# Initialize the DataExtractor with HTML and conference info
extractor = DataExtractor(html, "eacl", True)

# Extract data
success = extractor.extract_data()
print(success)

# Access the extracted DataFrame
data = extractor.data
print(data.head())

# Optionally save to CSV
data.to_csv("eacl_data.csv", index=False, encoding="utf-8")
```

---

## Developer Notes

- **HTTP Headers:**  
  Bibliographic requests use custom headers to mimic a real browser and reduce the chance of being blocked. These may need to be updated depending on the target site.  

- **Error Handling:**  
  Unresolved bib links are tracked in `bib_link_not_found` for debugging or retrying.  

- **Data Merging:**  
  If abstracts are present, the bib and abstract data are merged on the `"ID"` field. If no abstracts exist, an empty `"abstract"` column is added.  

---

# file Keyword_Filter

## Class: `CsvDdata`
The `CsvDdata` class provides functionality to:
- Load a CSV dataset created from  containing conference papers.
- Filter the dataset based on athe presence of keywords in the `title` or `abstract` columns.

This class is useful for extracting relevant subsets of papers based on thematic keywords.

---

### Initialization
```python
CsvDdata(csv_path)
```
**Parameters:**
- `csv_path` (`str`): Path to the CSV file containing the dataset.

**Attributes:**
- `csv` (`pandas.DataFrame`): Loaded dataset from the CSV file.

---

### Methods

#### `keyword_filter(self, keywords) -> pandas.DataFrame`
Filters the dataset based on a list of keywords.

**Parameters:**
- `keywords` (`list[str]`): List of keywords to search for in the `title` or `abstract` columns.

**Process:**
1. Converts the list of keywords into a regular expression pattern with word boundaries to avoid partial matches.  
2. Creates a boolean mask where the `title` or `abstract` contains any of the keywords (case-insensitive).  
3. Applies the mask to filter the dataset.  
4. Prints the number of matching rows.  
5. Returns the filtered DataFrame.

---

## Example Usage
```python
# Define keywords for filtering
keywords = [
    "polyvocality", "polyperspectivity", "poliphony", "polysemy",
    "plurality", "polycentrism", "perspectivism", "multi perspective",
    "multiplicity", "multivocality"
]

# Load CSV dataset
data = CsvDdata("path/to/dataset.csv")

# Filter data based on keywords
filtered_data = data.keyword_filter(keywords)

# Save filtered dataset to CSV
filtered_data.to_csv("path/to/filtered_data.csv", index=False)
```

---

## Developer Notes

- **Regex Matching:**  
  Word boundaries (`\b`) are used to prevent partial matches within larger words.  
- **Case-Insensitive Search:**  
  The search ignores case using the `re.IGNORECASE` flag.  
- **Data Requirements:**  
  The CSV file must contain `title` and `abstract` columns for filtering to work properly.  

