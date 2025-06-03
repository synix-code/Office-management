import firebase_admin
from firebase_admin import credentials, firestore
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, pink, blue
import datetime
import json
import io
import smtplib
from email.message import EmailMessage

def send_inward_pdf_email():
    try:
        # ✅ Load user data
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
        email = user_data.get("email")
        comp = user_data.get("comp")

        # ✅ Firebase init
        if not firebase_admin._apps:
            cred = credentials.Certificate("office-hub.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        # ✅ Get inward entries
        doc_ref = db.collection("users").document(email)
        doc = doc_ref.get()
        inward = doc.to_dict().get("inward", {})

        # ✅ Sort by date
        sorted_keys = sorted(
            inward.keys(),
            key=lambda x: datetime.datetime.strptime(inward[x].get("date", "01/01/1970"), "%d/%m/%Y"),
            reverse=True
        )

        # ✅ Generate PDF in memory
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 50
        line_height = 20

        def draw_header():
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(pink)
            c.drawString(margin, height - 50, "Inward Entry")
            c.setStrokeColor(pink)
            c.setLineWidth(2)
            c.line(margin, height - 60, width - margin, height - 60)

            c.setFont("Helvetica", 14)
            c.setFillColor(black)
            c.drawString(margin, height - 80, f"Company: {comp}")

        draw_header()
        y = height - 120

        for key in sorted_keys:
            entry = inward[key]
            lines_needed = 8 * line_height
            if y < margin + lines_needed:
                c.showPage()
                draw_header()
                y = height - 120

            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(blue)
            c.drawString(margin, y, f"Invoice: {entry.get('invoice', key)}")
            y -= line_height

            fields = [
                ("Date", entry.get("date", "N/A")),
                ("Time", entry.get("time", "N/A")),
                ("Article", entry.get("article", "N/A")),
                ("Quantity", entry.get("quantity", "N/A")),
                ("Amount", entry.get("amount", "N/A")),
                ("Party", entry.get("party", "N/A")),
                ("Vehicle", entry.get("vehicle", "N/A")),
            ]

            for label, value in fields:
                c.setFont("Helvetica", 12)
                c.drawString(margin + 20, y, f"{label}: {value}")
                y -= line_height

            y -= 10  # gap between entries

        c.save()

        # ✅ Prepare email
        buffer.seek(0)
        msg = EmailMessage()
        msg['Subject'] = f"{comp} - Inward Entry Report"
        msg['From'] = 'streetcoding777@gmail.com'
        msg['To'] = email
        msg.set_content("Attached is your inward entry PDF from Office Hub.")

        # Attach PDF
        msg.add_attachment(buffer.read(), maintype='application', subtype='pdf', filename='Inward-Entry.pdf')

        # ✅ Send Email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("streetcoding777@gmail.com", "xctp fqxt qzbr rejd")
            smtp.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

send_inward_pdf_email()
