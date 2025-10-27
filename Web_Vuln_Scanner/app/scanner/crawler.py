from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from .utils import get_form_details, submit_form
from .xss import test_xss
from .sqli import test_sqli
from .csrf import test_csrf
from .command_injection import test_command_injection

def crawl_and_scan(start_url):
    """Crawl the website starting from the given URL and scan forms and links"""
    visited = set()
    to_visit = [start_url]
    vulnerabilities = []
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all forms on the page
            forms = soup.find_all('form')
            for form in forms:
                form_details = get_form_details(form)
                # Test each form for vulnerabilities
                vulnerabilities += test_xss(url, form_details, session)
                vulnerabilities += test_sqli(url, form_details, session)
                vulnerabilities += test_csrf(form_details)
                vulnerabilities += test_command_injection(url, form_details, session)

            # Find all links and add them to the queue
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith(('mailto:', 'tel:', 'javascript:', '#')) and not href.endswith(('.pdf', '.jpg', '.png', '.docx')):
                    absolute_url = urljoin(url, href)
                    parsed = urlparse(absolute_url)
                    if parsed.netloc == urlparse(start_url).netloc and absolute_url not in visited:
                        to_visit.append(absolute_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    return vulnerabilities    