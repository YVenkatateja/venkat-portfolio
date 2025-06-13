from flask import Flask, render_template, request, redirect, flash
import smtplib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret in production

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Contact Form Submission
@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    full_message = f"From: {name} <{email}>\n\n{message}"

    # Read environment variables for email credentials
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = "venkatateja310@gmail.com"

    if not sender_email or not sender_password:
        flash("Email configuration is missing. Please contact site admin.", "error")
        return redirect('/contact')

    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, full_message)
        server.quit()

        flash("✅ Message sent successfully!", "success")
    except Exception as e:
        print("❌ Email send failed:", e)
        flash("⚠️ Failed to send message. Try again later.", "error")

    return redirect('/contact')

# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Entry Point
if __name__ == '__main__':
    app.run(debug=True)
