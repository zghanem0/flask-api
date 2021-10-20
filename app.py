import logging
from flask_restful import Resource, Api
from pymongo import MongoClient
import time, datetime, logging

import flask
from flask import Flask, request, jsonify
from time import strftime

# before
start_time = time.time()

# app init
app = flask.Flask(__name__)
api = Api(app)

#
# class Visit(Resource):
#     def get(self):
#         retJson = "helllllo"
#         return retJson
#


client = MongoClient("mongodb://192.168.1.7:27017")
store = client.store
books = store["books"]


@app.route("/show_books")
def show_books():
    all_books = books.find({}, {"title": 1, "_id": 0})

    jason = []
    boks = [bok for bok in list(all_books)]
    for bok in boks:
        if 'title' in bok:
            jason.append(bok['title'])
    return jsonify({'books': str(jason)})


@app.route("/add_one", methods=['GET', 'POST'])
def add_one():
    all_books = books.find({}, {"title": 1, "_id": 0})

    try:
        if request.method == 'POST':
            for bok in list(all_books):
                if 'title' in bok:
                    # u can use  request.json.get('title') instead of request.get_json()["title"]
                    if request.get_json()["title"] == bok["title"]:
                        return "the book already exist"
        # request.json.get()  instead of request.get_json()
        books.insert_one(request.get_json())
        return "added successfully"
    except BaseException as error:
        result = f"error : {error}"
        return result


@app.route("/book", methods=['GET', 'POST'])
def get_book():
    all_books = books.find({},
                           {'isbn': 1, "title": 1, 'author_last_name': 1, 'page_count': 1, 'description': 1, "_id": 0})

    try:
        if request.method == 'GET':
            for bok in list(all_books):
                if 'title' in bok:
                            # request.json.get('title')  instead of request.get_json()["title"] 
                    if request.get_json()["title"] == bok["title"]:
                        return jsonify({"book details": bok})


    except BaseException as error:
        result = f"error : {error}"
        return result


@app.route("/")
def home():
    return jsonify({'all books details': str(list(books.find({}, {"_id": 0})))})


@app.route("/delete_book", methods=['DELETE'])
def delete_one():
    all_books = books.find({}, {"title": 1, "_id": 0})

    # print(list(books.find()))
    try:
        for b in all_books:
            # request.json.get('title')  instead of request.get_json()["title"] 
            if request.get_json()["title"] == b['title']:
                book = books.delete_one({'title': request.get_json()["title"]})
                return str(f"delete successfully with this result : {book.raw_result}")

        return "Not exist make sure you have wrote the book name correctly", 404
    except BaseException as error:
        result = f'error : {error}'
        return result


# api.add_resource(Visit, "/hello")


# after
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    end_time = time.time()
    Elapsed_time = end_time - start_time
    app.logger.error(f'%s {Elapsed_time} %s %s %s %s %s ', timestamp, request.remote_addr, request.method,
                     request.scheme, request.full_path, response.status)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

