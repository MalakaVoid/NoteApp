from bson import ObjectId
from pymongo import *
import datetime

client = MongoClient()
db = client['DB5']

def recover_note(deleted_note, user_id):
    notes_collection = db['notes']
    user_collection = db['users']
    deleted_notes_collection = db['deleted_notes']

    try:
        deleted_notes_collection.find_one_and_delete({"_id": ObjectId(deleted_note['_id'])})
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$pull": {"deleted_notes": ObjectId(deleted_note['_id'])}})
        note_id = notes_collection.insert_one(deleted_note).inserted_id
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$push": {"notes": ObjectId(note_id)}})
    except Exception as ex:
        print(ex)
        return 404


def delete_note_forever(note_id, user_id):
    del_notes_collection = db['deleted_notes']
    user_collection = db['users']
    try:
        del_notes_collection.find_one_and_delete({"_id": ObjectId(note_id)})
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$pull": {"deleted_notes": ObjectId(note_id)}})
    except Exception as ex:
        return 404
    return 200


def get_deleted_notes(user_id):
    note_ids = db['users'].find_one({"_id": ObjectId(user_id)})['deleted_notes']
    del_notes_collection = db['deleted_notes']
    arr_of_notes = []
    for each in note_ids:
        arr_of_notes.append(del_notes_collection.find_one({"_id": each}))
    return arr_of_notes


def search_note(user_id, text):
    try:
        db['notes'].create_index([('title', 'text'), ('text', 'text')])
    except Exception as ex:
        a=1
    user_collection = db['users']
    notes_collection = db['notes']

    user = user_collection.find_one({"_id": ObjectId(user_id)})

    search_result = notes_collection.find({
                     "$text": {
                         "$search": text
                     }
                     })
    search_arr = []
    for each in search_result:
        if each['_id'] in user['notes']:
            search_arr.append(each)
    return search_arr


def delete_note(note, user_id):
    notes_collection = db['notes']
    user_collection = db['users']
    deleted_notes_collection = db['deleted_notes']

    insert_to_delete = {
        "title": note['title'],
        "text": note['text'],
        "creation_date": note['creation_date'],
        "update_date": note['update_date']
    }

    try:
        notes_collection.find_one_and_delete({"_id": ObjectId(note['_id'])})
        deleted_id = deleted_notes_collection.insert_one(insert_to_delete).inserted_id
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$pull": {"notes": ObjectId(note['_id'])}})
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$push": {"deleted_notes": ObjectId(deleted_id)}})
    except Exception as ex:
        print(ex)
        return 404
    return 200


def update_note(note_id, text, title) -> int:
    notes_collection = db['notes']
    edited_note = {
        "title": title,
        "text": text,
        "update_date": datetime.datetime.now(),
    }
    try:
        notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": edited_note})
    except Exception as ex:
        print(ex)
        return 404
    return 200


def get_notes(user_id):
    note_ids = db['users'].find_one({"_id": ObjectId(user_id)})['notes']
    notes_collection = db['notes']
    arr_of_notes = []
    for each in note_ids:
        arr_of_notes.append(notes_collection.find_one({"_id": each}))
    return arr_of_notes


def add_note(user_id, title, text):
    user_collection = db['users']
    notes_collection = db['notes']
    data_note = {
        "title": title,
        "text": text,
        "creation_date": datetime.datetime.now(),
        "update_date": datetime.datetime.now()
    }
    try:
        note_id = notes_collection.insert_one(data_note).inserted_id
        user_collection.update_one({"_id": ObjectId(user_id)},
                                   {"$push": {"notes": ObjectId(note_id)}})
    except Exception as ex:
        return 404
    return 200

def registrate_user(username, name, password):
    if authorize_user(username, password) != 404:
        return 500
    post = {
        "username": username,
        "name": name,
        "password": password,
        "notes": list(),
        "deleted_notes": list()
    }

    collection = db['users']
    try:
        user_id = collection.insert_one(post).inserted_id
    except Exception as ex:
        return 404
    return user_id


def authorize_user(username, password):
    collection = db['users']
    user = collection.find_one({"username": username})
    if user is None:
        return 404
    if user['password'] != password:
        return 500
    return user['_id']