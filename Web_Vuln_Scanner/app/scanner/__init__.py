from .crawler import crawl_and_scan

def start_scan_async(scan_id):
    from app import create_app
    from app.models import db, Scan, Vulnerability
    
    app = create_app()
    with app.app_context():
        scan = Scan.query.get(scan_id)
        if not scan:
            return
        
        try:
            scan.status = 'Running'
            db.session.commit()
            
            # Start the scan
            vulnerabilities = crawl_and_scan(scan.target_url)
            
            # Save vulnerabilities
            for vuln in vulnerabilities:
                db.session.add(Vulnerability(
                    type=vuln['type'],
                    url=vuln['url'],
                    payload=vuln['payload'],
                    severity=vuln['severity'],
                    scan_id=scan.id
                ))
            
            scan.status = 'Completed'
            db.session.commit()
        except Exception as e:
            scan.status = f'Failed: {str(e)}'
            db.session.commit()