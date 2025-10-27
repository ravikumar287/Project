import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

# SQL error patterns for detection
SQL_ERROR_PATTERNS = [
    r"SQL syntax.*MySQL",
    r"Warning.*mysql_.*",
    r"Unclosed quotation mark after the character string",
    r"quoted string not properly terminated",
    r"SQL Server.*error",
    r"ORA-[0-9]{5}",
    r"PostgreSQL.*ERROR"
]

def check_sql_errors(response):
    """Check response for SQL error patterns"""
    for pattern in SQL_ERROR_PATTERNS:
        if re.search(pattern, response.text, re.IGNORECASE):
            return True
    return False

def get_form_details(form):
    """Extract form details"""
    details = {}
    action = form.attrs.get('action', '').lower()
    method = form.attrs.get('method', 'get').lower()
    inputs = []
    
    for input_tag in form.find_all('input'):
        input_type = input_tag.attrs.get('type', 'text')
        input_name = input_tag.attrs.get('name')
        if input_name:
            inputs.append({'type': input_type, 'name': input_name})
    
    # Also consider textarea and select tags
    for textarea_tag in form.find_all('textarea'):
        input_name = textarea_tag.attrs.get('name')
        if input_name:
            inputs.append({'type': 'textarea', 'name': input_name})
    
    for select_tag in form.find_all('select'):
        input_name = select_tag.attrs.get('name')
        if input_name:
            options = []
            for option in select_tag.find_all('option'):
                options.append(option.attrs.get('value', ''))
            inputs.append({'type': 'select', 'name': input_name, 'options': options})
    
    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details

def submit_form(form_details, url, payload, session):
    """Submit form with payload"""
    target_url = urljoin(url, form_details['action'])
    data = {}
    
    for input in form_details['inputs']:
        if input['type'] in ['text', 'textarea', 'select', 'search', 'email']:
            data[input['name']] = payload
        else:
            data[input['name']] = input.get('value', '')
    
    if form_details['method'] == 'post':
        response = session.post(target_url, data=data, allow_redirects=False)
    else:
        response = session.get(target_url, params=data, allow_redirects=False)
    
    return response