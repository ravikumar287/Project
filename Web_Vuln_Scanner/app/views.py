from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from .models import db, Scan, Vulnerability
from .scanner import start_scan_async
import threading

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/scan', methods=['POST'])
@login_required
def start_scan():
    target_url = request.form.get('url')
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Create new scan record
    new_scan = Scan(
        target_url=target_url,
        user_id=current_user.id,
        status='Pending'
    )
    db.session.add(new_scan)
    db.session.commit()
    
    # Start the scan in a background thread
    thread = threading.Thread(target=start_scan_async, args=(new_scan.id,))
    thread.daemon = True
    thread.start()
    
    flash('Scan started! It may take a while. Check the scans page for updates.')
    return redirect(url_for('main.scans'))

@main.route('/scans')
@login_required
def scans():
    user_scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.date.desc()).all()
    return render_template('scans.html', scans=user_scans)

@main.route('/scan/<int:scan_id>')
@login_required
def scan_detail(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    if scan.user_id != current_user.id:
        flash('You do not have permission to view this scan')
        return redirect(url_for('main.scans'))
    return render_template('scan_detail.html', scan=scan)   


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
