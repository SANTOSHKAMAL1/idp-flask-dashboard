from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)

# Configurations
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# MongoDB connection
mongo = PyMongo(app, tlsCAFile=certifi.where())
collection = mongo.db.sections

# -------------------------------
# ROUTES
# -------------------------------

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

@app.route("/enablers")
def enablers(): return render_template("enablers.html")

@app.route("/enablersA")
def enablersA(): return render_template("enablersA.html")

@app.route("/enablersb")
def enablersb(): return render_template("enablersb.html")

@app.route("/enablersc")
def enablersc(): return render_template("enablersc.html")

@app.route("/enablersd")
def enablersd(): return render_template("enablersd.html")

@app.route("/enablerse")
def enablerse(): return render_template("enablerse.html")

@app.route("/enablersf")
def enablersf(): return render_template("enablersf.html")

@app.route("/enablersg")
def enablersg(): return render_template("enablersg.html")

@app.route("/enablersh")
def enablersh(): return render_template("enablersh.html")

@app.route("/index")
def index(): return render_template("index.html")

# -------------------------------
# API Endpoints
# -------------------------------

@app.route("/api/sections", methods=["GET"])
def get_sections():
    sections = []
    for sec in collection.find():
        sec["_id"] = str(sec["_id"])
        sections.append(sec)
    return jsonify(sections)

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

@app.route("/api/sections/<id>", methods=["PUT"])
def update_section(id):
    name = request.form.get("name")
    content = request.form.get("content")
    pdf = request.files.get("pdf")

    update_data = {"name": name, "content": content}

    if pdf:
        filename = secure_filename(pdf.filename)
        pdf_path = f"uploads/{filename}"
        pdf.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        update_data["pdfPath"] = pdf_path

    result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return jsonify({"updated": result.modified_count})

@app.route("/api/sections/<id>", methods=["DELETE"])
def delete_section(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"deleted": result.deleted_count})

@app.route("/uploads/<filename>")
def serve_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------------------------------
# For Local Development
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

