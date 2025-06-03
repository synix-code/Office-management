from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import pink, blue, red, black
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def generate_attendance_pdf():
    # ✅ Firebase Init
    cred = credentials.Certificate("office-hub.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # ✅ Fetch attendance from Firestore
    doc_ref = db.collection("users").document("butterflyowner1@gmail.com")
    doc = doc_ref.get()
    attendance_raw = doc.to_dict().get("Attendance", {})

    # ✅ Organize data by date
    attendance_by_date = {}
    for employee, records in attendance_raw.items():
        for date, times in records.items():
            attendance_by_date.setdefault(date, []).append({
                "employee": employee,
                "arrival": times.get("arrival", "N/A"),
                "departure": times.get("departure", "N/A")
            })

    # ✅ Sort dates (latest first)
    sorted_dates = sorted(attendance_by_date.keys(), key=lambda d: datetime.datetime.strptime(d, "%d/%m/%Y"), reverse=True)

    # ✅ PDF Setup
    c = canvas.Canvas("OfficeHub-Attendance.pdf", pagesize=A4)
    width, height = A4
    margin = 50
    line_height = 20

    # ✅ Header + Watermark
    def draw_header():
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(pink)
        c.drawString(margin, height - 50, "Office Hub")
        c.setStrokeColor(pink)
        c.setLineWidth(2)
        c.line(margin, height - 60, width - margin, height - 60)

        c.setFont("Helvetica", 16)
        c.setFillColor(black)
        c.drawString(margin, height - 85, "Company: Office Hub Pvt. Ltd.")

        c.saveState()
        c.setFont("Helvetica-Bold", 60)
        c.setFillColor(pink)
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, "AS Developer")
        c.restoreState()

    # ✅ Styled text printer
    def draw_text(x, y, text, color=black, bold=False, strike=False):
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, 12)
        c.setFillColor(color)
        c.drawString(x, y, text)
        if strike:
            text_width = c.stringWidth(text, font, 12)
            c.setLineWidth(1)
            c.setStrokeColor(color)
            c.line(x, y + 6, x + text_width, y + 6)

    # ✅ Column + pagination
    left_x = margin
    right_x = width / 2 + 10
    left_y = right_y = height - 120
    column = "left"

    def get_xy():
        return (left_x, left_y) if column == "left" else (right_x, right_y)

    def has_space(y, needed):
        return y - needed > 60

    def switch_col_or_page():
        nonlocal column, left_y, right_y
        if column == "left":
            column = "right"
        else:
            c.showPage()
            draw_header()
            column = "left"
            left_y = right_y = height - 120

    def update_y(lines):
        nonlocal left_y, right_y
        if column == "left":
            left_y -= lines
        else:
            right_y -= lines

    # ✅ Begin PDF
    draw_header()

    for date in sorted_dates:
        records = attendance_by_date[date]
        lines_needed = (len(records) * 3 + 1) * line_height
        y_pos = left_y if column == "left" else right_y

        if not has_space(y_pos, lines_needed):
            switch_col_or_page()

        x, y = get_xy()
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(pink)
        c.drawString(x, y, f"📅 Date: {date}")
        y -= line_height

        for rec in records:
            emp = rec['employee']
            arr = rec['arrival']
            dep = rec['departure']
            c.setFont("Helvetica-Bold", 15)

            draw_text(x + 20, y, f"👤 {emp}", color=blue, bold=True)
            y -= line_height

            c.setFont("Helvetica-Bold", 14)
            strike = any(w in arr.lower() for w in ["sunday", "closed"])
            draw_text(x + 40, y, f"🟢 Arrival: {arr}", red if strike else black, bold=strike, strike=strike)
            y -= line_height

            strike = any(w in dep.lower() for w in ["sunday", "closed"])
            draw_text(x + 40, y, f"🔴 Departure: {dep}", red if strike else black, bold=strike, strike=strike)
            y -= line_height

        update_y(lines_needed)

    # ✅ Save PDF
    c.save()
    print("✅ PDF saved as 'OfficeHub-Attendance.pdf'")
generate_attendance_pdf()