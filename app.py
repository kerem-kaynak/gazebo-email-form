from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_ADDRESS")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = ("Gazebo İletişim", os.getenv("EMAIL_ADDRESS"))

mail = Mail(app)


@app.route("/form-submission", methods=["POST"])
def form_submission():
    data = request.json or {}
    api_key = data.get("api_key")
    if api_key != os.getenv("API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    print("Preparing email")

    email_body = f"""
    <html>
        <body>
            <h3>İletişim formu üzerinden yeni bir kayıt alındı!</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr><th>Form Alanı</th><th>Değer</th></tr>
                <tr><td>İsim</td><td>{data.get('first_name', '')}</td></tr>
                <tr><td>Soyisim</td><td>{data.get('last_name', '')}</td></tr>
                <tr><td>Telefon Numarası</td><td>{data.get('phone_number', '')}</td></tr>
                <tr><td>Email</td><td>{data.get('email', '')}</td></tr>
                <tr><td>Tarih</td><td>{data.get('date', '')}</td></tr>
                <tr><td>Saat</td><td>{data.get('time', '')}</td></tr>
                <tr><td>Misafir Sayısı</td><td>{data.get('seats', '')}</td></tr>
                <tr><td>Mesaj</td><td>{data.get('message', '')}</td></tr>
            </table>
        </body>
    </html>
    """

    print("Email data: ", email_body)

    send_email("Yeni Form Kaydı", email_body)

    return jsonify({"message": "Form submitted successfully"}), 200


def send_email(subject, body):
    recipient = os.getenv("RECEIVER_EMAIL")
    if not recipient:
        raise ValueError("RECEIVER_EMAIL is not set in environment variables")

    msg = Message(subject, recipients=[recipient])
    msg.html = body
    mail.send(msg)
    print("Email sent successfully!")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
