from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)
NOTES_FILE = "notes.json"

#@app.get("/")
#def index():
#    return send_from_directory(".", "index.html")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


@app.get("/notes")
def get_notes():
    return jsonify(load_notes())


@app.post("/notes")
def add_note():
    notes = load_notes()
    data = request.get_json()

    note = {
        "id": len(notes) + 1,
        "text": data["text"]
    }

    notes.append(note)
    save_notes(notes)

    return jsonify(note), 201


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    notes = load_notes()
    notes = [note for note in notes if note["id"] != note_id]
    save_notes(notes)

    return "", 204


app.run(host="127.0.0.1", port=8080)
