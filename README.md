# Generic Web Crawler

A comprehensive web scraping tool that can crawl any website completely and extract all content into structured Markdown format. This crawler handles various content types including web pages, documents, images, and multimedia files while maintaining proper formatting and organization.

## Features

### Generic Website Crawling
- **Full Site Crawling**: Systematically crawls entire websites following all internal links
- **Smart Link Discovery**: Automatically finds and queues all internal links
- **Depth Control**: Configurable crawling depth to prevent infinite loops
- **Domain Filtering**: Stays within target domain boundaries
- **Duplicate Prevention**: Avoids processing duplicate URLs and content

### Content Extraction & Processing
- **HTML Content**: Extracts and converts web page content to structured Markdown
- **Document Downloads**: Automatically downloads PDF, DOCX, DOC, Excel, and CSV files
- **Advanced Image Processing**: Smart image content extraction with table detection
  - Uses `img2table` library to detect if tables exist in images
  - If tables are found: Crops image row and column-wise, extracts content via OCR, and formats as structured tables
  - If no tables: Extracts plain text content using OCR
- **Table Processing**: Converts HTML tables to properly formatted Markdown tables
- **Text Formatting**: Preserves headers, paragraphs, lists, and text formatting

### File Type Support
- **Web Content**: HTML pages converted to Markdown
- **Documents**: PDF, DOCX, DOC files (downloaded for offline processing)
- **Spreadsheets**: XLSX, CSV files (downloaded)
- **Images**: PNG, JPG, JPEG with OCR text extraction
- **Email Links**: Extracts email addresses from mailto links

### Output Organization
- **Structured Markdown**: All content saved in clean, readable Markdown format
- **Metadata Tracking**: Maintains metadata files for downloaded documents
- **File Organization**: Separate folders for different file types
- **Content Deduplication**: Prevents duplicate content in output files

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/AdeelIntizar/Generic-Crawler.git
cd Generic-Crawler
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install ChromeDriver
ChromeDriver must be compatible with your Google Chrome version.

1. **Check your Chrome version**:
   - Open Google Chrome
   - Go to `Settings` → `About Chrome` or type `chrome://version/` in address bar
   - Note your Chrome version (e.g., Version 120.0.6099.109)

2. **Download compatible ChromeDriver**:
   - Visit: https://chromedriver.chromium.org/downloads
   - Download the ChromeDriver version that matches your Chrome version
   - Extract the `chromedriver.exe` file to a known location
   - Example path: `C:\chromedriver\chromedriver.exe`

3. **Update ChromeDriver path in code**:
   ```python
   chrome_driver_path = "C:\\path\\to\\your\\chromedriver.exe"
   ```

### Step 4: Install Tesseract OCR
Required for extracting text from images.

1. **Download Tesseract**:
   - Visit: https://github.com/tesseract-ocr/tesseract
   - For Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the installer for your system

2. **Install Tesseract**:
   - Run the installer
   - Default installation path: `C:\Program Files\Tesseract-OCR\`
   - Make sure to install the English language pack
   - Note the installation path for configuration

3. **Update Tesseract path in code**:
   ```python
   pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
   ```

### Step 5: Configure Output Directories
Adjust the paths for markdown files and document storage directories in the code:

```python
# Main output file path
filename = "D:/scrapper/your_project_name/output.md"

# Document storage directories
pdf_files_path_dir = "D:/scrapper/your_project_name/documents/pdf/"
docx_files_path_dir = "D:/scrapper/your_project_name/documents/docx/"
doc_files_path_dir = "D:/scrapper/your_project_name/documents/doc/"
excel_files_path_dir = "D:/scrapper/your_project_name/documents/excel/"
csv_files_path_dir = "D:/scrapper/your_project_name/documents/csv/"
metadata_path = "D:/scrapper/your_project_name/documents/metadata"
```

2. **Run the Crawler**:
   ```bash
   python crawler.py
   ```

### Advanced Configuration
- **Crawling Depth**: Modify the depth limit in `get_all_links()` function
- **File Type Filtering**: Add or remove file extensions in the filtering logic
- **Content Filtering**: Customize header/footer exclusion rules
- **Output Format**: Modify content extraction in `extract_content_bs4()` function

## How It Works

### Crawling Process
1. **Initialization**: Starts with the base URL and initializes Chrome WebDriver
2. **Link Discovery**: Finds all internal links on each page
3. **Queue Management**: Maintains a queue of URLs to visit
4. **Content Extraction**: Processes each page to extract content
5. **File Downloads**: Downloads linked documents and files
6. **OCR Processing**: Extracts text from images using Tesseract
7. **Markdown Conversion**: Converts all content to structured Markdown

### Content Processing Pipeline
1. **HTML Parsing**: Uses BeautifulSoup to parse page structure
2. **Content Extraction**: Extracts headers, paragraphs, lists, tables, and images
3. **Format Conversion**: Converts HTML elements to Markdown equivalents
4. **Deduplication**: Prevents duplicate content using content hashing
5. **File Organization**: Saves content and downloads to organized directories

