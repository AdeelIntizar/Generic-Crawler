   

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from docx import Document
import os
import aspose.words as aw
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from bs4 import BeautifulSoup
import requests
from img2table.document import Image as img2table_Image
import pytesseract
import numpy as np
from PIL import Image
from io import BytesIO
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
from img2table.document import Image as img2table_Image
import pytesseract

def extract_content_from_image(image_path):
    image_flag = None
    text = ""
    image_table_content = []

    try:
        with urlopen(image_path) as response:
            image_bytes = response.read()
            image = Image.open(BytesIO(image_bytes))
            img = img2table_Image(src=image_bytes)
            pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            image_tables = img.extract_tables()
            if len(image_tables) >= 1:
                image_flag = 0
                for table_index, table in enumerate(image_tables):
                    structured_table_content = []
                    table_content = []
                    for i in range(1, len(table.content)):
                        row_content = []
                        cell = table.content[i]
                        for inner_attr in cell:
                            bbox = inner_attr.bbox
                            x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
                            cropped_image = image.crop((x1, y1, x2, y2))
                            cell_text = pytesseract.image_to_string(cropped_image)
                            cell_text = ' '.join(cell_text.split())
                            row_content.append(cell_text)
                        if any(cell.strip() for cell in row_content):
                            table_content.append(row_content)
                    structured_table_content.append(table_content)
                    for table_index, table in enumerate(structured_table_content):
                        for row_index, row in enumerate(table):
                            if row_index == 0:
                                image_table_content.append(f"| {' | '.join(row)} |")
                                image_table_content.append(f"| {' | '.join(['-' * len(col) for col in row])} |")
                            else:
                                image_table_content.append(f"| {' | '.join(row)} |")
            else:
                text = pytesseract.image_to_string(image)
                image_flag = 1

    except Exception as e:
        print(f"Error occurred: {e}")
        image_flag = None

    return image_flag, image_table_content, text



def download_document(pdf_url, save_path,base_url,metadata_path,temp_metadata,file_name):
    file_flag=False
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": base_url
    }
    try:
        response = requests.get(pdf_url,headers=headers, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        file_flag=True
        print(f"PDF downloaded and saved at {save_path}")
        if file_flag:
            with open(metadata_path+f"/{file_name}.md","a",encoding="utf-8") as file:
                for item in temp_metadata:
                    file.write(item+"\n")

    except requests.exceptions.RequestException as e:
        try:
            new_url=base_url+"/"+pdf_url
            response = requests.get(new_url,headers=headers, stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                file.write(response.content)
            file_flag=True
            print(f"PDF downloaded and saved at {save_path}")
            if file_flag:
                with open(metadata_path+f"/{file_name}.md","a",encoding="utf-8") as file:
                    for item in temp_metadata:
                        file.write(item+"\n")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the PDF: {e}")

            
   

def save_document(content, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, "a", encoding="utf-8") as file:
        for item in content:
            if isinstance(item, list): 
                for line in item:
                    file.write(line)
            else:
                file.write(item + "\n\n")
           

def extract_content_bs4(url,page_source, visited_contents, first_link,visited_images,base_url):
    temp_metadata=[]
    metadata_path="D:/scrapper/documents2/metadata"
    soup = BeautifulSoup(page_source, "html.parser")
    content = []
    content_check=[]
    header = soup.find("header")
    header_descendants = set(header.descendants) if header else set()
    footer = soup.find("footer")
    footer_descendants = set(footer.descendants) if footer else set()

    if soup:
        content.append(f"Page Url : {url}")
        for element in soup.body.descendants:
            
            if not first_link:
                if element in footer_descendants:
                    continue
                if element in header_descendants:
                    continue
            elif first_link:
                if element in footer_descendants:
                    continue
                first_link = False

            if element.name == "h1":
                content.append(f"# {element.get_text(strip=True)}")
                content_check.append(f"# {element.get_text(strip=True)}")
                temp_metadata.append(f"# {element.get_text(strip=True)}")
            elif element.name == "h2":
                content.append(f"## {element.get_text(strip=True)}")
                content_check.append(f"## {element.get_text(strip=True)}")
                temp_metadata.append(f"## {element.get_text(strip=True)}")
            elif element.name in [f"h{i}" for i in range(3, 7)]:
                content.append(f"### {element.get_text(strip=True)}")
                content_check.append(f"### {element.get_text(strip=True)}")
                temp_metadata.append(f"### {element.get_text(strip=True)}")
            elif element.name == "p":
                # content.append(element.get_text(strip=True))
                # content_check.append(element.get_text(strip=True))
                paragraph_text = element.get_text(strip=True)
                if element.find_all(["b", "strong"]):  
                    bold_text = ""
                    for part in element.find_all(True):
                        if part.name in ["b", "strong"]:
                            bold_text += f"**{part.get_text()}**"  
                        else:
                            bold_text += part.get_text() 
                    content.append(bold_text.strip())
                    content_check.append(bold_text.strip())
                else:
                    content.append(paragraph_text)
                    content_check.append(paragraph_text)
            elif element.name == "li" or element.parent.name == "ul":
                content.append(f"- {element.get_text(strip=True)}")
                content_check.append(f"- {element.get_text(strip=True)}")
            elif element.name == "ol":
                content.append([f"{index+1}. {li.get_text(strip=True)}\n" for index, li in enumerate(element.find_all("li"))])
                content_check.append([f"{index+1}. {li.get_text(strip=True)}\n" for index, li in enumerate(element.find_all("li"))])
            elif element.name == "span":
                span_text = element.get_text(strip=True)
                if span_text:
                    content.append(span_text)
                    content_check.append(span_text)
            elif element.name == "a":
                href = element.get("href", "")
                if href.startswith("mailto:"):
                    new_href = str(href).split(":")[1]
                    content.append(f"{new_href}")
                elif href.endswith(".pdf"):
                    if href not in visited_pdfs:
                        visited_pdfs.append(href)
                        pdf_files_path_dir="D:/scrapper/documents2/pdf/"
                        pdf_name=href.split("/")[-1]
                        pdf_file_path=os.path.join(pdf_files_path_dir,pdf_name)
                        file_name=pdf_name.split(".")[0]
                        # save_path=os.path.join(pdf_file_path,href.split("/")[-1])
                        download_document(href, pdf_file_path,base_url,metadata_path,temp_metadata,file_name)
                        # pdf_content = extract_text_from_pdf(href,base_url)
                        # content.append(f"\n{pdf_content}")
                elif href.endswith(".docx"):
                    if href not in visited_docx:
                        visited_docx.append(href)
                        docx_files_path_dir="D:/scrapper/documents2/docx/"
                        docx_name=href.split("/")[-1]
                        docx_file_path=os.path.join(docx_files_path_dir,docx_name)
                        # save_path=os.path.join(docx_file_path,href.split("/")[-1])
                        file_name=docx_name.split(".")[0]
                        download_document(href, docx_file_path,base_url,metadata_path,temp_metadata,file_name)

                elif href.endswith(".doc"):
                    if href not in visited_docx:
                        visited_docx.append(href)
                        doc_files_path_dir="D:/scrapper/documents2/doc/"
                        doc_name=href.split("/")[-1]
                        doc_file_path=os.path.join(doc_files_path_dir,doc_name)
                        # save_path=os.path.join(doc_file_path,href.split("/")[-1])
                        file_name=doc_name.split(".")[0]
                        download_document(href, doc_file_path,base_url,metadata_path,temp_metadata,file_name)

                elif href.endswith(".xlsx"):
                    if href not in visited_docx:
                        visited_docx.append(href)
                        excel_files_path_dir="D:/scrapper/documents2/excel/"
                        excel_name=href.split("/")[-1]
                        excel_file_path=os.path.join(excel_files_path_dir,excel_name)
                        # save_path=os.path.join(excel_file_path,href.split("/")[-1])
                        file_name=excel_name.split(".")[0]
                        download_document(href, excel_file_path,base_url,metadata_path,temp_metadata,file_name)

                elif href.endswith(".csv"):
                    if href not in visited_docx:
                        visited_docx.append(href)
                        csv_files_path_dir="D:/scrapper/documents2/csv/"
                        csv_name=href.split("/")[-1]
                        csv_file_path=os.path.join(csv_files_path_dir,csv_name)
                        # save_path=os.path.join(csv_file_path,href.split("/")[-1])
                        file_name=csv_name.split(".")[0]
                        download_document(href, csv_file_path,base_url,metadata_path,temp_metadata,file_name)




                        # doc_content=get_document_content(href)
                        # content.append("\n".join(doc_content))
            elif element.name == "img":
                img_src = element.get("src")
                if img_src not in visited_images:
                    visited_images.append(img_src)
                    if img_src and (img_src.endswith("png") or img_src.endswith("jpg") or img_src.endswith("jpeg")) and  img_src.startswith("https:"):
                        image_flag, image_table_content, text = extract_content_from_image(img_src)
                        if image_flag is not None:
                            if image_flag == 0:
                                content.append("\n".join(image_table_content))
                            elif image_flag == 1:
                                content.append(text)

            elif element.name == "table":
                table_data = []
                rows = element.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    if row_data:
                        table_data.append(row_data)
                if table_data:
                    markdown_table = []
                    headers = table_data[0]
                    markdown_table.append(f"| {' | '.join(headers)} |")
                    markdown_table.append(f"| {' | '.join(['-' * len(h) for h in headers])} |")
                    for row in table_data[1:]:
                        markdown_table.append(f"| {' | '.join(row)} |")
                    content.append("\n".join(markdown_table))

    if content_check in visited_contents:
        return None, visited_contents,visited_images
    else:
        visited_contents.append(content_check)
        return content, visited_contents,visited_images

def get_all_links(next_link, link_queue, seen_links, url):
    page_source = None
    try:
        driver.get(next_link)
        time.sleep(1)
        links = driver.find_elements(By.TAG_NAME, "a")
        page_source = driver.page_source
        temp_list = []
        for link in links:
            href = link.get_attribute("href")
            links_parts = str(href).split("//")[-1]
            broken_parts = links_parts.split("/")
            if len(broken_parts) <= 6:
                if href and url in href:
                    if not (href.endswith(".docx") or href.endswith(".doc") or href.endswith(".pdf") or 
                            href.endswith(".jpg") or href.endswith(".png") or href.endswith(".jpeg") or 
                            href.endswith("#") or href.endswith(".zip")):
                        if href not in seen_links and not any(site in href for site in ["twitter.com", "youtube.com", "facebook.com", "linkedin.com", "mailto"]):
                            seen_links.append(href)
                            temp_list.append(href)
        link_queue = temp_list + link_queue
        return link_queue, seen_links, page_source
    except Exception as e:
        time.sleep(8)
        driver.refresh()
        # driver.refresh()
        try:
            driver.get(next_link)
            time.sleep(1)
            links = driver.find_elements(By.TAG_NAME, "a")
            page_source = driver.page_source
            temp_list = []
            for link in links:
                href = link.get_attribute("href")
                links_parts = str(href).split("//")[-1]
                broken_parts = links_parts.split("/")
                if len(broken_parts) <= 6:
                    if href and url in href:
                        if not (href.endswith(".docx") or href.endswith(".doc") or href.endswith(".pdf") or 
                                href.endswith(".jpg") or href.endswith(".png") or href.endswith(".jpeg") or 
                                href.endswith(".#") or href.endswith(".zip")):
                            if href not in seen_links and not any(site in href for site in ["twitter.com", "youtube.com", "facebook.com", "linkedin.com", "mailto"]):
                                seen_links.append(href)
                                temp_list.append(href)
            link_queue = temp_list + link_queue
            return link_queue, seen_links, page_source
        except Exception as e:
            print(f"Error fetching links from {url}: {e}")
            return link_queue, seen_links, page_source

if __name__ == "__main__":
    chrome_driver_path = "C:\\Users\\aktiv\\OneDrive\\Documents\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(180)
    
    link_queue = []
    visited_links = []
    visited_pdfs=[]
    visited_docx=[]
    seen_links = []
    first_link = True
    base_url = "https://www.sharjah.ac.ae/en/"
    url_parts=base_url.split("//")[-1]
    # new_url_parts=url_parts.split("/")[-1]
    link_queue.append(base_url)
    filename = "D:/scrapper/IIUI/University of Sharjah Data1.md"
    visited_contents = []
    visited_images=[]
    j = 0
    while link_queue:
        next_link = link_queue.pop(0)
        if next_link not in visited_links:
            print(next_link)
            visited_links.append(next_link)
            if url_parts in next_link:
                driver.refresh()
                link_queue, seen_links, page_source = get_all_links(next_link, link_queue, seen_links, url_parts)
                print(f"Stored {len(link_queue)} links in the queue.")
                if page_source is not None:
                    content, visited_contents,visited_images = extract_content_bs4(next_link,page_source, visited_contents, first_link,visited_images,base_url)
                    if content is not None:
                        save_document(content, filename)
                else:
                    print(f"Failed to fetch page source for {next_link}")

            print("Index : ", j)
            j += 1
    
    driver.quit()
                
                
                
                
                
                
           



                
                
                