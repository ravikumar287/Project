def test_csrf(form_details):
    """Check if form has CSRF protection (token)"""
    has_token = False
    for input_field in form_details['inputs']:
        if input_field['type'] == 'hidden' and (input_field['name'] == 'csrf_token' or 'csrf' in input_field['name'] or 'token' in input_field['name']):
            has_token = True
            break
    
    if not has_token:
        return [{
            'type': 'CSRF',
            'url': form_details['action'],
            'payload': None,
            'severity': 'Medium',
            'description': 'Form is missing CSRF token'
        }]
    return []