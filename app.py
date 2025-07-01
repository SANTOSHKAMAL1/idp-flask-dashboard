from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import certifi

# Load env variables
load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)

# Config
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# MongoDB
mongo = PyMongo(app, tlsCAFile=certifi.where())
collection = mongo.db.sections

# Dashboard - view all
@app.route("/")
def dashboard():
    sections = list(collection.find())
    for sec in sections:
        sec["_id"] = str(sec["_id"])
    return render_template("dashboard.html", sections=sections)

@app.route("/section/<section_id>")
def view_section(section_id):
    sections = list(collection.find({"sectionId": section_id}))
    for sec in sections:
        sec["_id"] = str(sec["_id"])
    return render_template("dashboard.html", sections=sections)


# Add form page
@app.route("/index")
def index():
    return render_template("index.html")

# API: Get all sections (optional)
@app.route("/api/sections", methods=["GET"])
def get_sections():
    sections = []
    for sec in collection.find():
        sec["_id"] = str(sec["_id"])
        sections.append(sec)
    return jsonify(sections)

# API: Add section
@app.route("/api/sections", methods=["POST"])
def add_section():
    name = request.form.get("name")
    content = request.form.get("content")
    section_id = request.form.get("sectionId")
    pdf = request.files.get("pdf")

    pdf_path = ""
    if pdf:
        filename = secure_filename(pdf.filename)
        pdf.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        pdf_path = f"uploads/{filename}"

    new_section = {
        "name": name,
        "content": content,
        "sectionId": section_id,
        "pdfPath": pdf_path
    }

    inserted = collection.insert_one(new_section)
    new_section["_id"] = str(inserted.inserted_id)
    return jsonify(new_section), 201

# Delete section
@app.route("/api/sections/<id>", methods=["DELETE"])
def delete_section(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"deleted": result.deleted_count})

# Serve uploaded PDF
@app.route("/uploads/<filename>")
def serve_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
