import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Image

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6c757d"))
        
        # Header (Top of every page)
        self.drawString(54, 800, "Anamnesebogen - Hausarztpraxis Dipl. med. Hanaa Ahmad")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Footer (Bottom of every page)
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Schleifweg 3, 04932 Prösen | Tel: 03533-8217")
        page_str = f"Seite {self._pageNumber} von {page_count}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()

def create_anamnese_pdf(output_path, logo_path):
    # Setup document
    # A4 dimensions: 595.27 x 841.89 points
    # Printable area: 54 to 541 (left-right width = 487 pt)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#3a424e")
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#00adb5")
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#94a3b8")
    )
    
    section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#3a424e"),
        spaceBefore=12,
        spaceAfter=6
    )

    sub_section_title = ParagraphStyle(
        'SubSecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#475569")
    )

    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )
    
    bold_label_style = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#3a424e")
    )

    checkbox_label_style = ParagraphStyle(
        'CheckboxLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#3a424e")
    )

    story = []

    # --- PAGE 1: HEADER & PERSONAL DETAILS ---
    
    # Header block with logo
    logo_w = 60
    logo_h = 60
    
    header_data = [
        [Image(logo_path, width=logo_w, height=logo_h) if os.path.exists(logo_path) else "LOGO", 
         [
             Paragraph("Hausarztpraxis Dipl. med. Hanaa Ahmad", title_style),
             Paragraph("Fachärztin für Innere Medizin", subtitle_style),
             Paragraph("ANAMNESEBOGEN ZUR ERSTUNTERSUCHUNG / NEUPATIENTEN", meta_style)
         ]
        ]
    ]
    header_table = Table(header_data, colWidths=[70, 417])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Greeting Box
    greeting_text = (
        "<b>Liebe Patientin, lieber Patient,</b><br/>"
        "herzlich willkommen in unserer Praxis. Um Sie im Rahmen unserer hausärztlich-internistischen "
        "Versorgung bestmöglich behandeln zu können, bitten wir Sie, diesen Anamnesebogen sorgfältig auszufüllen. "
        "Alle Angaben unterliegen selbstverständlich der ärztlichen Schweigepflicht und dem Datenschutz."
    )
    greeting_table = Table([[Paragraph(greeting_text, body_style)]], colWidths=[487])
    greeting_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(greeting_table)
    story.append(Spacer(1, 12))

    # Section 1: Aktueller Anlass
    story.append(Paragraph("1. AKTUELLER BESUCHSGRUND", section_title))
    reason_table = Table([
        [Paragraph("Grund des heutigen Besuchs / Aktuelle Hauptbeschwerden:", label_style)],
        [""],
        [""]
    ], colWidths=[487], rowHeights=[14, 20, 20])
    reason_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (0,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(reason_table)
    story.append(Spacer(1, 14))

    # Red/Warning box: Dringende internistische Warnhinweise
    warning_title = Paragraph("<b>DRINGENDE INTERNISTISCHE WARNHINWEISE (BITTE ZUTREFFENDES ANKREUZEN)</b>", ParagraphStyle('WarnT', parent=body_style, textColor=colors.HexColor("#991b1b"), fontName="Helvetica-Bold"))
    
    cb = " [  ] "
    warning_data = [
        [Paragraph(f"{cb}<b>Blutverdünner</b> (z.B. ASS, Marcumar, Eliquis, Xarelto, Lixiana)", checkbox_label_style),
         Paragraph(f"{cb}<b>Herzschrittmacher</b> / Defibrillator (ICD)", checkbox_label_style)],
        [Paragraph(f"{cb}<b>Metallimplantate</b> / Gelenkersatz / Stents", checkbox_label_style),
         Paragraph(f"{cb}<b>Infektionskrankheiten</b> (z.B. Hepatitis, HIV, Tuberkulose)", checkbox_label_style)]
    ]
    warning_table = Table([[warning_title], [Table(warning_data, colWidths=[238, 238])]], colWidths=[487])
    warning_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef2f2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#fca5a5")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,1), (0,1), 4),
    ]))
    story.append(warning_table)
    story.append(Spacer(1, 14))

    # Section 2: Persönliche Angaben
    story.append(Paragraph("2. PERSÖNLICHE ANGABEN", section_title))
    
    # 2-column personal details table
    pers_data = [
        [Paragraph("NAME, VORNAME", label_style), Paragraph("GEBURTSDATUM", label_style)],
        ["", ""],
        [Paragraph("STRASSE, HAUSNUMMER", label_style), Paragraph("PLZ, WOHNORT", label_style)],
        ["", ""],
        [Paragraph("TELEFON (MOBIL / FESTNETZ)", label_style), Paragraph("E-MAIL-ADRESSE", label_style)],
        ["", ""],
        [Paragraph("BERUF / AKTUELLE TÄTIGKEIT", label_style), Paragraph("KRANKENKASSE", label_style)],
        ["", ""],
        [Paragraph("BISHERIGER HAUSARZT (NAME, ORT)", label_style), ""]
    ]
    pers_table = Table(pers_data, colWidths=[243, 244], rowHeights=[12, 16, 12, 16, 12, 16, 12, 16, 12])
    pers_table.setStyle(TableStyle([
        ('SPAN', (0,8), (1,8)), # Span GP field across columns
        ('LINEBELOW', (0,1), (0,1), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,1), (1,1), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,3), (0,3), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,3), (1,3), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,5), (0,5), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,5), (1,5), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,7), (0,7), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,7), (1,7), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,8), (1,8), 0.5, colors.HexColor("#cbd5e1")), # Bisheriger Hausarzt line
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(pers_table)
    story.append(Spacer(1, 14))

    # Section 3: Lebensstil & Soziale Anamnese
    story.append(Paragraph("3. LEBENSSTIL & SOZIALANAMNESE", section_title))
    
    lifestyle_data = [
        [Paragraph("GRÖSSE (CM)", label_style), Paragraph("GEWICHT (KG)", label_style), Paragraph("WOHNSITUATION", sub_section_title)],
        ["", "", Paragraph(f"{cb}Alleinlebend  {cb}Mit Partner/Familie  {cb}Betreutes Wohnen", checkbox_label_style)],
        [Paragraph("NIKOTINKONSUM", sub_section_title), "", Paragraph("ALKOHOLKONSUM", sub_section_title)],
        [Paragraph(f"{cb}Nein  {cb}Ja (..... / Tag)  {cb}Früher (seit: .....)", checkbox_label_style), "",
         Paragraph(f"{cb}Nein  {cb}Gelegentlich  {cb}Regelmäßig", checkbox_label_style)],
        [Paragraph("SPORTLICHE AKTIVITÄTEN / BEWEGUNG IM ALLTAG", sub_section_title), "", ""],
        ["", "", ""]
    ]
    lifestyle_table = Table(lifestyle_data, colWidths=[100, 80, 307])
    lifestyle_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (0,1), 0.5, colors.HexColor("#cbd5e1")), # Grösse
        ('LINEBELOW', (1,1), (1,1), 0.5, colors.HexColor("#cbd5e1")), # Gewicht
        ('SPAN', (0,2), (1,2)), # Span nicotine label
        ('SPAN', (0,3), (1,3)), # Span nicotine checkboxes
        ('SPAN', (0,4), (2,4)), # Span sport label
        ('SPAN', (0,5), (2,5)), # Span sport textline
        ('LINEBELOW', (0,5), (2,5), 0.5, colors.HexColor("#cbd5e1")), # Sport line
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,2), (-1,2), 8),
        ('TOPPADDING', (0,4), (-1,4), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(lifestyle_table)

    story.append(PageBreak())

    # --- PAGE 2: CONDITIONS, ALLERGIES, PREVENTIONS & MEDICATION ---
    
    # Section 4: Vorerkrankungen & Befunde
    story.append(Paragraph("4. VORERKRANKUNGEN & BEFUNDE", section_title))
    
    cond_data = [
        [Paragraph(f"{cb}Bluthochdruck (Hypertonie)", checkbox_label_style), Paragraph(f"{cb}Lungenerkrankung (z.B. Asthma, COPD)", checkbox_label_style)],
        [Paragraph(f"{cb}Herzerkrankung (z.B. KHK, Rhythmusstör.)", checkbox_label_style), Paragraph(f"{cb}Magen-/Darmerkrankung (z.B. Reflux)", checkbox_label_style)],
        [Paragraph(f"{cb}Schlaganfall / TIA", checkbox_label_style), Paragraph(f"{cb}Leber- / Nierenerkrankung", checkbox_label_style)],
        [Paragraph(f"{cb}Diabetes mellitus (Zuckerkrankheit)", checkbox_label_style), Paragraph(f"{cb}Psychische / Neurologische Erkrankung", checkbox_label_style)],
        [Paragraph(f"{cb}Schilddrüsenerkrankung", checkbox_label_style), Paragraph(f"{cb}Tumorerkrankung / Krebs", checkbox_label_style)],
        [Paragraph(f"{cb}Fettstoffwechselstörung (z.B. Cholesterin)", checkbox_label_style), Paragraph(f"{cb}Blutgerinnungsstörung / Thrombose", checkbox_label_style)]
    ]
    cond_table = Table(cond_data, colWidths=[243, 244])
    cond_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(cond_table)
    story.append(Spacer(1, 6))

    # Additional text line for Vorerkrankungen
    cond_add_table = Table([
        [Paragraph("Zusätzliche Informationen zu Vorerkrankungen / Befunden / Sonstiges:", label_style)],
        [""]
    ], colWidths=[487], rowHeights=[14, 18])
    cond_add_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (0,1), 0.5, colors.HexColor("#cbd5e1")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(cond_add_table)
    story.append(Spacer(1, 12))

    # Section 5: Allergien & Unverträglichkeiten
    story.append(Paragraph("5. ALLERGIEN & UNVERTRÄGLICHKEITEN", section_title))
    allergy_data = [
        [Paragraph(f"{cb}Keine bekannt", checkbox_label_style), Paragraph(f"{cb}Medikamente", checkbox_label_style), Paragraph(f"{cb}Lebensmittel", checkbox_label_style), Paragraph(f"{cb}Pflaster / Latex", checkbox_label_style)],
        [Paragraph(f"{cb}Pollen / Gräser", checkbox_label_style), Paragraph(f"{cb}Tierhaare", checkbox_label_style), Paragraph(f"{cb}Kontrastmittel", checkbox_label_style), Paragraph(f"{cb}Sonstige", checkbox_label_style)]
    ]
    allergy_table = Table(allergy_data, colWidths=[121, 121, 122, 123])
    allergy_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(allergy_table)
    story.append(Spacer(1, 4))
    
    allergy_text_table = Table([
        [Paragraph("Falls zutreffend: Welche Auslöser und Reaktionen (z.B. Ausschlag, Atemnot)?", label_style)],
        [""]
    ], colWidths=[487], rowHeights=[14, 18])
    allergy_text_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (0,1), 0.5, colors.HexColor("#cbd5e1")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(allergy_text_table)
    story.append(Spacer(1, 12))

    # Section 6: Vorsorge & Untersuchungen
    story.append(Paragraph("6. VORSORGEUNTERSUCHUNGEN & IMPFUNGEN", section_title))
    prev_data = [
        [Paragraph("LETZTER CHECK-UP 35 (JAHR / ARZT)", label_style), Paragraph("LETZTE DARMSSPIEGELUNG (JAHR)", label_style)],
        ["", ""],
        [Paragraph("KREBSVORSORGE (JAHR)", label_style), Paragraph("LIEGT IHR IMPFAUSWEIS HEUTE VOR?", sub_section_title)],
        ["", Paragraph(f"{cb}Ja  {cb}Nein, wird nachgereicht", checkbox_label_style)],
        [Paragraph("NUR FÜR FRAUEN: SCHWANGERSCHAFT?", sub_section_title), Paragraph("SCHWANGERSCHAFTEN / GEBURTEN (ANZAHL)", label_style)],
        [Paragraph(f"{cb}Nein  {cb}Ja (Woche: .....)  {cb}Unbekannt", checkbox_label_style), ""]
    ]
    prev_table = Table(prev_data, colWidths=[243, 244], rowHeights=[12, 16, 12, 16, 12, 16])
    prev_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (0,1), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,1), (1,1), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (0,3), (0,3), 0.5, colors.HexColor("#cbd5e1")),
        ('LINEBELOW', (1,5), (1,5), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(prev_table)
    story.append(Spacer(1, 12))

    # Section 7: Aktuelle Medikation
    story.append(Paragraph("7. AKTUELLE MEDIKATION", section_title))
    story.append(Paragraph("Nehmen Sie regelmäßig Medikamente ein? (Auch rezeptfreie, Vitamine oder Nahrungsergänzungsmittel)", label_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"{cb}Nein      {cb}Ja, siehe Tabelle unten / beigefügten Medikationsplan (BMP)", checkbox_label_style))
    story.append(Spacer(1, 6))

    # Medication Table
    med_headers = [
        Paragraph("<b>MEDIKAMENTENNAME / WIRKSTOFF</b>", bold_label_style),
        Paragraph("<b>DOSIERUNG (MG)</b>", bold_label_style),
        Paragraph("<b>MORGENS</b>", bold_label_style),
        Paragraph("<b>MITTAGS</b>", bold_label_style),
        Paragraph("<b>ABENDS</b>", bold_label_style),
        Paragraph("<b>NACHT</b>", bold_label_style)
    ]
    med_data = [med_headers]
    for _ in range(5):
        med_data.append(["", "", "", "", "", ""])
    
    med_table = Table(med_data, colWidths=[207, 100, 45, 45, 45, 45], rowHeights=[18] + [16]*5)
    med_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,1), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(med_table)

    story.append(PageBreak())

    # --- PAGE 3: OPERATIONS, FAMILY HISTORY, LEGAL PRECAUTION & SIGNATURE ---
    
    # Section 8: Operationen & Krankenhausaufenthalte
    story.append(Paragraph("8. OPERATIONEN & KRANKENHAUSAUFENTHALTE", section_title))
    op_headers = [
        Paragraph("<b>JAHR</b>", bold_label_style),
        Paragraph("<b>DIAGNOSE, OPERATION ODER GRUND DES AUFENTHALTS</b>", bold_label_style)
    ]
    op_data = [op_headers]
    for _ in range(6):
        op_data.append(["", ""])
    op_table = Table(op_data, colWidths=[80, 407], rowHeights=[18] + [16]*6)
    op_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(op_table)
    story.append(Spacer(1, 14))

    # Section 9: Familienanamnese
    story.append(Paragraph("9. FAMILIENANAMNESE", section_title))
    story.append(Paragraph("Liegen schwerwiegende Erkrankungen in Ihrer direkten Verwandtschaft (Eltern, Geschwister, Großeltern)?", label_style))
    story.append(Spacer(1, 6))
    
    fam_data = [
        [Paragraph(f"{cb}Bluthochdruck", checkbox_label_style), Paragraph(f"{cb}Krebserkrankungen", checkbox_label_style)],
        [Paragraph(f"{cb}Herzinfarkt / KHK (< 60 J.)", checkbox_label_style), Paragraph(f"{cb}Lungenerkrankungen", checkbox_label_style)],
        [Paragraph(f"{cb}Schlaganfall", checkbox_label_style), Paragraph(f"{cb}Erbkrankheiten / Plötzlicher Herztod", checkbox_label_style)],
        [Paragraph(f"{cb}Diabetes mellitus (Zuckerkrankheit)", checkbox_label_style), ""]
    ]
    fam_table = Table(fam_data, colWidths=[243, 244])
    fam_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(fam_table)
    story.append(Spacer(1, 14))

    # Section 10: Rechtliche Vorsorge
    story.append(Paragraph("10. RECHTLICHE VORSORGE", section_title))
    
    legal_data = [
        [Paragraph("PATIENTENVERFÜGUNG VORHANDEN?", label_style), Paragraph("VORSORGEVOLLMACHT VORHANDEN?", label_style)],
        [Paragraph(f"{cb}Ja      {cb}Nein", checkbox_label_style), Paragraph(f"{cb}Ja      {cb}Nein", checkbox_label_style)]
    ]
    legal_table = Table(legal_data, colWidths=[243, 244], rowHeights=[12, 16])
    legal_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(legal_table)
    story.append(Spacer(1, 20))

    # Section 11: Patientenerklärung & Unterschrift
    story.append(Paragraph("11. ERKLÄRUNG UND UNTERSCHRIFT", section_title))
    declaration_text = (
        "Ich bestätige, dass ich alle vorstehenden Angaben nach bestem Wissen und Gewissen vollständig "
        "und wahrheitsgetreu gemacht habe. Zukünftige Änderungen (z.B. neu verordnete Medikamente, andere Dosierungen "
        "oder neu aufgetretene Diagnosen) werde ich der Praxis unaufgefordert mitteilen."
    )
    story.append(Paragraph(declaration_text, body_style))
    story.append(Spacer(1, 40))

    sig_data = [
        ["", ""],
        [Paragraph("ORT, DATUM", label_style), Paragraph("UNTERSCHRIFT DES PATIENTEN / GESETZLICHEN VERTRETERS", label_style)]
    ]
    sig_table = Table(sig_data, colWidths=[200, 287], rowHeights=[20, 14])
    sig_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor("#334155")),
        ('LINEBELOW', (1,0), (1,0), 0.75, colors.HexColor("#334155")),
        ('VALIGN', (0,1), (-1,1), 'TOP'),
        ('TOPPADDING', (0,1), (-1,1), 4),
    ]))
    story.append(sig_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    out_path = r"d:\Dev\Python\Django\Clinic\static\documents\aufnahmeformular.pdf"
    logo = r"d:\Dev\Python\Django\Clinic\static\images\logo.png"
    # Ensure dir exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    create_anamnese_pdf(out_path, logo)
    print("PDF successfully generated.")
