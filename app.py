from flask import Flask, request, jsonify
import pdfkit
import smtplib
from email.message import EmailMessage
from config import *
from interview_agent import generate_feedback
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
env = Environment(loader=FileSystemLoader("templates"))

@app.route('/interview', methods=['POST'])
def process_interview():
    data = request.json
    transcript = data['transcript']
    candidate_name = data['candidate_name']
    role = data['role']
    recipient_email = data['email']

    feedback = generate_feedback(transcript, candidate_name, role)
    template = env.get_template("feedback_template.html")
    html_out = template.render(candidate_name=candidate_name, role=role, feedback=feedback)

    pdf_path = f"{candidate_name}_feedback.pdf"
    pdfkit.from_string(html_out, pdf_path)

    msg = EmailMessage()
    msg['Subject'] = f"Interview Feedback - {candidate_name}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email
    msg.set_content("Interview feedback attached as PDF.")
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=pdf_path)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return jsonify({"status": "success", "message": "Feedback sent!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
