from urllib.parse import urlparse, urljoin
from model import Session, User
import hashlib

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def check_user_creds(username='', password=''):
    # Returns user or false
    s = Session()
    user = s.query(User).filter_by(username=username).first()
    if user != None:
        if password == user.password:
            return user
    return False

def hash_password(password):
    m = hashlib.sha256()
    m.update(password.encode())
    return m.hexdigest()
