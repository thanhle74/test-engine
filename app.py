from flask import Flask, render_template
from flask_cors import CORS
from routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

# Giao diện chính
@app.route("/")
def index():
    return render_template("index.html")

# Đăng ký blueprint
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
