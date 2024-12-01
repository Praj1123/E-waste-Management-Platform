from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ecorecycle98123@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'oufq tcps yggm synm'   # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'ecorecycle98123@gmail.com'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('dummymail.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    recipient_email = request.form['recipient_email']
    subject = request.form['subject']
    body = request.form['body']
    attachment = request.files.get('attachment')  # Handle file attachment if present

    try:
        # Create a message
        msg = Message(subject, recipients=[recipient_email], body=body)

        # Attach file if uploaded
        if attachment:
            # Save the file temporarily
            attachment_path = os.path.join('uploads', attachment.filename)
            attachment.save(attachment_path)
            with app.open_resource(attachment_path) as fp:
                msg.attach(attachment.filename, attachment.content_type, fp.read())
            os.remove(attachment_path)  # Clean up the file after sending

        # Send the email
        mail.send(msg)
        return redirect(url_for('index'))  # Redirect to the form after email is sent

    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error: Unable to send email", 500

if __name__ == "__main__":
    app.run(debug=True)
