from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)


books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 9780394800165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]


@app.route('/')
@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


# POST /books
# {
#     'name': 'F',
#     'price': 6.99,
#     'isbn': 1234567890
# }

def valid_book_object(book_object):
    if ('name' in book_object and 'price' in book_object and 'isbn' in book_object):  # noqa
        return True
    else:
        return False


# /books/isbn_number

@app.route('/book', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (valid_book_object(request_data)):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalid_book_object_error_msg = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in must be similar to this {"name": "bookname", "price": 7.99, "isbn": 1234567890}'  # noqa
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')  # noqa
        return response

# PUT /books/132456789
# {
#     'name': 'The Odyssey',
#     'price': 0.99
# }


def valid_put_request_data(book_object):
    if ('name' in book_object and 'price' in book_object):
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if (not valid_put_request_data(request_data)):
        invalid_book_object_error_msg = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in must be similar to this {"name": "bookname", "price": 7.99}'  # noqa
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')  # noqa
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        current_isbn = book['isbn']
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response

# PATCH /books/9780394800165
# {
#     'name': 'Harry Potter'
# }


@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if ('name' in request_data):
        updated_book['name'] = request_data['name']
    if ('price' in request_data):
        updated_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


app.run(port=5000)
