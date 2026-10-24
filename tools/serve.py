import http.server
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Only the site itself is served; résumé sources, FAQ, reference/ and tooling stay private.
ALLOWED = ('/index.html', '/src/', '/public/', '/fonts/', '/projects/', '/icon.svg', '/profile-placeholder.svg', '/suyash.jpg', '/resume.pdf', '/og.png', '/robots.txt')


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        p = super().translate_path(path)
        if not os.path.exists(p):
            alt = os.path.join(ROOT, 'public', os.path.relpath(p, ROOT))
            if os.path.exists(alt):
                return alt
        return p

    def send_head(self):
        clean = self.path.split('?', 1)[0]
        if clean != '/' and not any(clean == a or (a.endswith('/') and clean.startswith(a)) for a in ALLOWED):
            self.send_error(404)
            return None
        return super().send_head()


os.chdir(ROOT)
http.server.ThreadingHTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
