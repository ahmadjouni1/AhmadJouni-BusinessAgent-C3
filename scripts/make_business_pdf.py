"""Generate me/about_business.pdf, the SunCedar Solar business profile.

SunCedar Solar is a fictional company created for the EECE 503P/798S C3 assignment.
All names, prices, phone numbers and policies below are invented.

Usage:
    python scripts/make_business_pdf.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent.parent / "me" / "about_business.pdf"

# Brand colors
CEDAR = colors.HexColor("#1F5E3B")   # deep cedar green
SUN = colors.HexColor("#F2A900")     # solar amber
SKY = colors.HexColor("#EAF4EE")     # pale green tint
INK = colors.HexColor("#1C1C1C")
MUTED = colors.HexColor("#5B6770")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=20, textColor=CEDAR, spaceBefore=6, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13.5, textColor=CEDAR, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=10.2, leading=14.5, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.8, leading=12, textColor=MUTED)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=9.2, leading=12.2, spaceAfter=0)
CELL_B = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
CELL_H = ParagraphStyle("CellH", parent=CELL_B, textColor=colors.white)
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=12, bulletIndent=2, spaceAfter=3)
COVER_TITLE = ParagraphStyle("CoverTitle", parent=H1, fontSize=34, leading=40,
                             alignment=TA_CENTER, textColor=CEDAR, spaceAfter=6)
COVER_SUB = ParagraphStyle("CoverSub", parent=BODY, fontSize=14, leading=19,
                           alignment=TA_CENTER, textColor=MUTED)
TAGLINE = ParagraphStyle("Tagline", parent=BODY, fontName="Helvetica-Oblique", fontSize=12,
                         alignment=TA_CENTER, textColor=CEDAR, spaceBefore=4)


def bullets(items):
    return [Paragraph(text, BULLET, bulletText="•") for text in items]


def table(rows, col_widths, header=True, zebra=True):
    data = [[Paragraph(str(c), CELL_H if (header and r == 0) else CELL) for c in row]
            for r, row in enumerate(rows)]
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6CE")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), CEDAR))
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if r % 2 == 0:
                style.append(("BACKGROUND", (0, r), (-1, r), SKY))
    t.setStyle(TableStyle(style))
    return t


def on_page(canvas, doc):
    w, h = A4
    canvas.saveState()
    # top band
    canvas.setFillColor(CEDAR)
    canvas.rect(0, h - 14 * mm, w, 14 * mm, stroke=0, fill=1)
    canvas.setFillColor(SUN)
    canvas.rect(0, h - 15.5 * mm, w, 1.5 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(18 * mm, h - 9 * mm, "SunCedar Solar")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(w - 18 * mm, h - 9 * mm, "Company Profile 2026")
    # footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18 * mm, 10 * mm,
                      "SunCedar Solar s.a.l. (fictional company) • hello@suncedar.example • WhatsApp +961 70 000 111")
    canvas.drawRightString(w - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def on_cover(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(CEDAR)
    canvas.rect(0, h - 70 * mm, w, 70 * mm, stroke=0, fill=1)
    # stylized sun
    canvas.setFillColor(SUN)
    canvas.circle(w / 2, h - 38 * mm, 16 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(SUN)
    canvas.setLineWidth(2.2)
    import math
    for i in range(12):
        a = i * math.pi / 6
        x1, y1 = w / 2 + 20 * mm * math.cos(a), h - 38 * mm + 20 * mm * math.sin(a)
        x2, y2 = w / 2 + 26 * mm * math.cos(a), h - 38 * mm + 26 * mm * math.sin(a)
        canvas.line(x1, y1, x2, y2)
    # cedar-ish triangle on the sun
    canvas.setFillColor(CEDAR)
    p = canvas.beginPath()
    p.moveTo(w / 2, h - 27 * mm)
    p.lineTo(w / 2 - 10 * mm, h - 47 * mm)
    p.lineTo(w / 2 + 10 * mm, h - 47 * mm)
    p.close()
    canvas.drawPath(p, stroke=0, fill=1)
    canvas.rect(w / 2 - 1.5 * mm, h - 52 * mm, 3 * mm, 5 * mm, stroke=0, fill=1)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(w / 2, 10 * mm,
                             "SunCedar Solar is a fictional company created for an academic assignment.")
    canvas.restoreState()


def build():
    story = []

    # ------------------------------------------------------------------ cover
    story += [Spacer(1, 78 * mm),
              Paragraph("SunCedar Solar", COVER_TITLE),
              Paragraph("Home solar for Lebanese families", COVER_SUB),
              Paragraph("Power your home, not your generator bill.", TAGLINE),
              Spacer(1, 14 * mm)]
    facts = [
        ["Founded", "2021"],
        ["Headquarters", "Zalka, Metn, Lebanon"],
        ["Homes powered", "1,400+ installations (as of September 2026)"],
        ["Contact", "WhatsApp +961 70 000 111 (24/7) • hello@suncedar.example"],
        ["Showroom hours", "Monday to Saturday, 9:00 to 18:00"],
    ]
    t = table(facts, [45 * mm, 115 * mm], header=False, zebra=False)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), SKY),
                           ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold")]))
    story += [t, PageBreak()]

    # ------------------------------------------------- about / mission / UVP
    story += [Paragraph("Who we are", H1),
              Paragraph(
                  "SunCedar Solar designs and installs solar power systems for homes across Lebanon. "
                  "For years, Lebanese families have lived between short hours of EDL (state grid) power and "
                  "expensive neighbourhood generator subscriptions (the <i>ishtirak</i>). We started SunCedar "
                  "in 2021 to give households a reliable, clean and predictable alternative: their own power, "
                  "on their own roof.", BODY),
              Paragraph("Our mission", H2),
              Paragraph(
                  "To help every Lebanese family stop depending on the grid and on generator subscriptions, "
                  "with honest pricing, fast installation and support that actually answers.", BODY),
              Paragraph("Why SunCedar: our three promises", H2)]
    story += bullets([
        "<b>Fixed-price quote after a free site visit.</b> An engineer visits your home for free, "
        "measures your roof and your consumption, and gives you one fixed price. The price on your quote is "
        "the price you pay. No hidden extras on installation day.",
        "<b>Installation within 7 days.</b> Your system is installed within 7 days of paying the deposit. "
        "If we are late, we credit you <b>$50 for every day of delay</b>, deducted from your final payment.",
        "<b>24/7 WhatsApp support.</b> A real person from our support team answers on WhatsApp "
        "(+961 70 000 111) day and night, including weekends and holidays.",
    ])
    story += [Paragraph("Our services", H2)]
    story += bullets([
        "<b>Home solar installation:</b> complete rooftop systems for apartments, houses and villas.",
        "<b>Battery and inverter systems:</b> LiFePO4 lithium batteries and hybrid inverters that keep the "
        "lights on at night and during blackouts. We also upgrade existing systems with extra batteries.",
        "<b>Maintenance plans:</b> panel cleaning, electrical checks and battery health reports (SunCare plans).",
        "<b>Free site assessment:</b> a no-obligation visit by an engineer, usually within 48 hours of your request.",
    ])
    story += [Paragraph("How it works", H2)]
    steps = [
        ["Step", "What happens", "Timing"],
        ["1. Contact us", "Send us a WhatsApp message, an email, or chat with Nour, our online advisor.", "Any time"],
        ["2. Free site visit", "An engineer checks your roof, shading, electrical panel, EDL hours and "
         "generator amperage.", "Within 48 hours"],
        ["3. Fixed-price quote", "You receive a written quote with one fixed price. The quote is valid for 14 days.",
         "Within 24 hours of the visit"],
        ["4. Installation", "Our crew installs, wires and tests the system. Most homes take 1 to 2 days on site.",
         "Within 7 days of the deposit"],
        ["5. Handover", "We set up the monitoring app on your phone and show you how the system works.",
         "On installation day"],
        ["6. Support", "24/7 WhatsApp support and your first-year maintenance visit.", "Ongoing"],
    ]
    story += [table(steps, [32 * mm, 95 * mm, 38 * mm]), PageBreak()]

    # ----------------------------------------------------------- packages
    story += [Paragraph("Packages and prices", H1),
              Paragraph(
                  "All prices are in US dollars, fixed, and include equipment, mounting structure, wiring, "
                  "protection devices, installation, integration with EDL and your generator, the monitoring "
                  "app, and one free maintenance visit in the first year. Prices apply to standard rooftop "
                  "installations in our main service areas; your fixed quote after the site visit confirms "
                  "the final price for your home.", BODY)]
    pk = [
        ["", "Basic", "Family", "Villa"],
        ["Price (USD)", "<b>$3,450</b>", "<b>$6,450</b>", "<b>$12,900</b>"],
        ["Solar panels", "6 × 550 W mono (3.3 kWp)", "12 × 550 W mono (6.6 kWp)",
         "24 × 550 W mono (13.2 kWp)"],
        ["Inverter", "5 kW hybrid inverter", "8 kW hybrid inverter", "12 kW three-phase hybrid inverter"],
        ["Battery", "5.12 kWh LiFePO4", "10.24 kWh LiFePO4", "20.48 kWh LiFePO4"],
        ["Typical daily production", "about 14 kWh", "about 28 kWh", "about 56 kWh"],
        ["Best for", "Apartments and small homes (2 to 3 people)", "Family homes (4 to 6 people)",
         "Villas and large homes"],
        ["What it can run", "Lights, fridge, TV, internet router, fans, laptops, washing machine (daytime)",
         "Everything in Basic, plus water pump, microwave, and 1 inverter AC during sunny hours",
         "Everything in Family, plus 2 to 3 inverter ACs during sunny hours and an electric water heater (daytime)"],
        ["Night backup (typical)", "8 to 10 hours of essential loads", "8 to 10 hours of most loads",
         "A full night of most loads, including 1 AC on low"],
        ["On-site install time", "1 day", "1 to 2 days", "2 days"],
    ]
    story += [table(pk, [36 * mm, 43 * mm, 43 * mm, 43 * mm]), Spacer(1, 5 * mm)]
    story += [Paragraph("Add-ons", H2)]
    addons = [
        ["Add-on", "Price (USD)", "Notes"],
        ["Extra battery module (5.12 kWh LiFePO4)", "$1,350", "Fits all packages; also for upgrading existing systems"],
        ["Extra 550 W panel", "$140 per panel", "Subject to roof space and inverter capacity"],
        ["Elevated steel structure", "$350", "For roofs with water tanks or shading; confirmed at site visit"],
        ["Bekaa travel fee", "$150", "One-time fee for installations in Zahle and Chtaura"],
    ]
    story += [table(addons, [62 * mm, 30 * mm, 73 * mm])]
    story += [Paragraph(
        "Note: we do not offer custom systems larger than the Villa package, commercial or industrial projects, "
        "or off-roof (ground-mounted) systems.", SMALL), PageBreak()]

    # ------------------------------------------- maintenance / warranty / pay
    story += [Paragraph("Maintenance plans (SunCare)", H1)]
    care = [
        ["Plan", "Price", "What is included"],
        ["SunCare Basic", "$120 per year",
         "2 visits per year: panel cleaning, electrical and connection check, inverter software update"],
        ["SunCare Plus", "$220 per year",
         "4 visits per year, everything in Basic, plus a battery health report and a priority technician "
         "visit within 24 hours if something goes wrong"],
    ]
    story += [table(care, [32 * mm, 30 * mm, 103 * mm]),
              Paragraph("Every new installation includes one free maintenance visit in the first year. "
                        "SunCare plans can be added at any time, including for systems installed by other companies "
                        "(after an inspection).", BODY)]
    story += [Paragraph("Warranty", H2)]
    war = [
        ["Component", "Warranty"],
        ["Solar panels", "12-year product warranty; 25-year performance warranty (at least 80% of rated output)"],
        ["Hybrid inverter", "5 years"],
        ["LiFePO4 battery", "10 years or 6,000 cycles, whichever comes first"],
        ["Installation workmanship", "2 years (wiring, mounting, leaks caused by our installation)"],
    ]
    story += [table(war, [45 * mm, 120 * mm]),
              Paragraph("Warranty claims are opened through WhatsApp support. Replacement parts are installed by "
                        "our technicians at no cost during the warranty period.", BODY)]
    story += [Paragraph("Payment options", H2)]
    story += bullets([
        "Cash in US dollars at our Zalka showroom or on installation day.",
        "Bank transfer in fresh US dollars.",
        "Card payment (Visa or Mastercard) at the showroom.",
        "Standard payment schedule: <b>30% deposit</b> when you accept the quote, <b>70% on completion</b> of the installation.",
        "Installment plan for Family and Villa packages: <b>40% upfront, then 6 equal monthly installments with 0% interest</b>.",
    ])
    story += [Paragraph("Service areas", H2)]
    areas = [
        ["Region", "Areas covered", "Travel fee"],
        ["Beirut", "All of Beirut", "None"],
        ["Mount Lebanon", "Metn, Keserwan, Baabda, Aley, Chouf", "None"],
        ["North", "Jbeil (Byblos), Batroun, Koura, Tripoli", "None"],
        ["South", "Saida, Jezzine, Tyre (Sour)", "None"],
        ["Bekaa", "Zahle and Chtaura only", "$150"],
    ]
    story += [table(areas, [32 * mm, 98 * mm, 35 * mm]),
              Paragraph("Areas not listed (for example Akkar, Baalbek-Hermel and Nabatieh) are not covered yet.", SMALL),
              PageBreak()]

    # ---------------------------------------------------------------- team
    story += [Paragraph("Our team", H1),
              Paragraph("SunCedar was founded by three friends who were tired of planning their evenings around "
                        "generator schedules. Today the company has 38 employees, including 6 installation crews.",
                        BODY)]
    team = [
        ("Karim Haddad, Co-founder and Chief Engineer",
         "Electrical engineer with 11 years of experience in power systems, including 6 years designing "
         "utility-scale solar plants in the Gulf. Karim designs every SunCedar package, approves every quote "
         "and trains our engineers. He believes a good system is one the customer never has to think about."),
        ("Rania Khoury, Co-founder and Head of Operations",
         "Rania spent 8 years in supply chain and logistics before co-founding SunCedar. She runs our warehouse "
         "and our 6 installation crews, and she is the reason we can promise installation within 7 days: "
         "SunCedar keeps every package in stock in its own warehouse."),
        ("Maya Nasr, Co-founder and Head of Customer Success",
         "Maya built SunCedar's 24/7 WhatsApp support team and the customer onboarding process. Before "
         "SunCedar she led customer service at a Lebanese telecom retailer. She personally reads every piece "
         "of customer feedback and every complaint."),
    ]
    for name, bio in team:
        story.append(KeepTogether([Paragraph(name, H2), Paragraph(bio, BODY)]))

    # ----------------------------------------------------------------- FAQ
    story += [Spacer(1, 4 * mm), Paragraph("Frequently asked questions", H1)]
    faq = [
        ("Will the system work at night and during blackouts?",
         "Yes. The battery charges from the sun during the day and powers your home at night and during EDL "
         "cuts. Switching from EDL to the battery is automatic and you will not notice it."),
        ("Can I keep my generator subscription?",
         "Yes. Every SunCedar system is integrated with EDL and with your generator. Most of our customers reduce "
         "their subscription (for example from 10 A to 5 A) and many cancel it completely after the first months."),
        ("How quickly does the system pay for itself?",
         "Most customers recover the cost in about 2 to 3 years, depending on their previous generator and EDL "
         "bills. We calculate an estimate for your home during the free site visit."),
        ("I live in an apartment building. Can I install on the roof?",
         "Usually yes, with the agreement of the building committee or the other owners. We can join a meeting "
         "with your building committee to explain the installation."),
        ("Do I need to be home for the site visit?",
         "Yes, an adult from the household should be present so our engineer can check the electrical panel "
         "and discuss your consumption. The visit takes about 45 minutes."),
        ("What happens in winter or on cloudy days?",
         "Production drops on cloudy days, typically to 30 to 60% of a sunny day. The system automatically uses "
         "EDL or your generator to recharge the battery when solar is not enough."),
        ("Can I add more batteries or panels later?",
         "Yes. All packages are designed to be expandable. See the add-ons table for prices."),
        ("Can I monitor my system?",
         "Yes. The SunCedar monitoring app shows production, battery level and consumption in real time on your phone."),
        ("Do I have to pay for the site visit?",
         "No. The site visit is always free and there is no obligation to buy."),
    ]
    for q, a in faq:
        story.append(KeepTogether([Paragraph(f"<b>{q}</b>", BODY), Paragraph(a, BODY)]))

    story += [Spacer(1, 6 * mm), Paragraph("Contact", H2)]
    story += bullets([
        "WhatsApp (24/7): +961 70 000 111",
        "Email: hello@suncedar.example",
        "Showroom: Zalka highway, Metn. Monday to Saturday, 9:00 to 18:00",
        "Online advisor: chat with Nour on our website",
    ])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=24 * mm, bottomMargin=18 * mm,
                            title="SunCedar Solar: Company Profile", author="SunCedar Solar (fictional)")
    doc.build(story, onFirstPage=on_cover, onLaterPages=on_page)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
