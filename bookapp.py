import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    return "<h1>a book with id %s</h1>" % book_id


def books():
    return "<h1>a list of books</h1>"


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
