import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    body = '<h1>Book Info: {}</h1>'.format(book_id)
    book_info = DB.title_info(book_id)
    if book_info is None:
        raise NameError
    else:
        body += """
<b>Title:</b> {title}<br />
<b>Author:</b> {author}<br />
<b>Publisher:</b> {publisher}<br />
<b>ISBN:</b> {isbn}<br />
""".format(**book_info)

    return body



def books():
    body = '<h1>Book List</h1>'
    for book in DB.titles():
        body += '\n<b><a href="/book/{}">{}</a></b><br />'.format(
            book['id'],
            book['title']
        )
    return body


def resolve_path(path):
    handlers = {
        '': books,
        'book': book
    }
    path = path.strip('/').split('/')
    try:
        return handlers[path[0]], path[1:]
    except KeyError:
        raise NameError
    raise NotImplementedError


def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    try:
        path, args = resolve_path(environ.get('PATH_INFO'))
        status = "200 OK"
        body = path(*args)
    except NameError:
        status = "404 Not Found"
        body = "<h1>404 Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>500 Internal Server Error</h1>"
    start_response(status, headers)

    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
