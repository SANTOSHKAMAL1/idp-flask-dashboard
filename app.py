from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Configurations
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def dashboard():
    return render_template("dashboard.html", sections=[])

@app.route("/section/<section_id>")
def view_section(section_id):
    return render_template("dashboard.html", sections=[])

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
# Dummy API (Optional)
# -------------------------------

@app.route("/api/sections", methods=["GET"])
def get_sections():
    return jsonify([])

@app.route("/uploads/<filename>")
def serve_pdf(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# -------------------------------
# For Local Development
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
