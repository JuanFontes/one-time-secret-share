from flask import Flask, render_template, request, url_for
from database import init_db, save_secret, get_and_delete_secret

# Initialize the Flask app
app = Flask(__name__)

# Initialize SQLite database (creates table if not exists)
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page route. Handles:
    - GET: Shows form to submit a secret.
    - POST: Saves the secret and generates a one-time URL.
    """
    secret_url = None
    expire_label = None

    # Mapping for dropdown values to human-readable labels
    expire_labels = {
        "1": "1 minute",
        "10": "10 minutes",
        "60": "1 hour",
        "1440": "1 day",
    }
    if request.method == "POST":
        secret = request.form.get("secret")  # Text from textarea
        expire_value = request.form.get(
            "expire", "10"
        )  # Expiration dropdown (default 10 minutes)
        expire_minutes = int(expire_value)  # Convert to integer

        # Save the encrypted secret and get the unique key
        key = save_secret(secret, expire_minutes)

        # Construct the full URL to retrieve the secret
        secret_url = request.host_url.rstrip("/") + url_for("read_secret", key=key)
        expire_label = expire_labels.get(expire_value, f"{expire_minutes} minutes")

    # Render the page, optionally showing the generated URL
    return render_template(
        "index.html", secret_url=secret_url, expire_label=expire_label
    )


@app.route("/secret/<key>")
def read_secret(key):
    """
    Route to view a secret via one-time link.
    If the secret exists and hasn't expired, it is shown and deleted.
    If not found or already viewed, show an error.
    """
    secret = get_and_delete_secret(key)

    if secret:
        return render_template("secret.html", secret=secret)
    else:
        return render_template("error.html"), 404


# Run the Flask app if executed directly (not via gunicorn or similar)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
