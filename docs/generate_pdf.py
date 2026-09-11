import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Only on page 2 and later)
        if self._pageNumber > 1:
            self.drawString(54, 800, "CivicPulse Monsoon — Technical Project Documentation")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        # Footer (On all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 30, page_text)
        self.drawString(54, 30, "Smart India Hackathon (SIH) — Municipal Decision-Support Platform | Confidential & Proprietary")
        self.restoreState()

def build_pdf(filename="CivicPulse_Monsoon_Project_Details.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")      # Dark Slate/Navy
    ACCENT = colors.HexColor("#0284C7")       # Ocean Blue
    TEAL = colors.HexColor("#0D9488")         # Vibrant Teal
    DARK_TEXT = colors.HexColor("#1E293B")    # Slate 800
    MUTED_TEXT = colors.HexColor("#475569")   # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")     # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#CBD5E1") # Slate 300

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner Block
    story.append(Paragraph("🌧️ CivicPulse Monsoon", title_style))
    story.append(Paragraph("AI-Based Predictive Waterlogging & Drainage Risk Management System", subtitle_style))
    
    # Badges / Meta bar table
    meta_data = [
        [
            Paragraph("<b>Target Domain:</b> Municipal Waterlogging & Urban Disaster Support", body_style),
            Paragraph("<b>Event:</b> Smart India Hackathon (SIH)", body_style),
            Paragraph("<b>Status:</b> Production-Ready Prototype", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 150, 157])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Executive Overview
    story.append(Paragraph("1. Executive Overview & Core Objective", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))
    
    exec_text = (
        "<b>CivicPulse Monsoon</b> is an end-to-end AI-powered geospatial platform engineered for municipal corporations "
        "and urban disaster management authorities. Existing municipal systems operate <i>reactively</i> — citizen complaint apps "
        "record waterlogging only after streets flood, paralyzing traffic and impeding emergency services. "
        "<b>CivicPulse Monsoon</b> shifts municipal operations from reactive firefighting to <b>proactive predictive management</b>."
    )
    story.append(Paragraph(exec_text, body_style))

    # Reactive vs Proactive Table
    comp_data = [
        [Paragraph("Feature / Aspect", table_header_style), Paragraph("Traditional Municipal Systems", table_header_style), Paragraph("CivicPulse Monsoon Platform", table_header_style)],
        [Paragraph("Operational Mode", table_cell_bold), Paragraph("Reactive (Post-event complaint logs)", table_cell_style), Paragraph("Proactive (24h/48h/72h predictive forecasting)", table_cell_style)],
        [Paragraph("Risk Insights", table_cell_bold), Paragraph("Historical complaints only", table_cell_style), Paragraph("SHAP Explainable AI rationale for risk drivers", table_cell_style)],
        [Paragraph("Spatial Awareness", table_cell_bold), Paragraph("Isolated ward points", table_cell_style), Paragraph("Drainage Dependency Graph & PostGIS Overlaps", table_cell_style)],
        [Paragraph("Resource Allocation", table_cell_bold), Paragraph("Manual / ad-hoc crew dispatch", table_cell_style), Paragraph("Google OR-Tools MILP Crew & Budget Optimizer", table_cell_style)],
        [Paragraph("Scenario Planning", table_cell_bold), Paragraph("None (Trial and error during storms)", table_cell_style), Paragraph("Interactive What-If Scenario Simulator", table_cell_style)],
    ]
    comp_table = Table(comp_data, colWidths=[110, 180, 197])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 14))

    # Architecture Section
    story.append(Paragraph("2. System Architecture & Tech Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))
    
    arch_desc = (
        "The architecture is decoupled into a high-performance <b>FastAPI Backend</b>, a geospatial <b>PostgreSQL/PostGIS Database</b>, "
        "a machine learning & optimization engine, and a <b>Next.js 14 Web Command Center</b>."
    )
    story.append(Paragraph(arch_desc, body_style))

    # Tech Stack Table
    tech_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technologies", table_header_style), Paragraph("Key Purpose & Responsibilities", table_header_style)],
        [Paragraph("Frontend App", table_cell_bold), Paragraph("Next.js 14, React 18, TypeScript, Tailwind CSS, Leaflet", table_cell_style), Paragraph("Interactive Command Center map, SHAP visual charts, resource planners, and simulator dashboard.", table_cell_style)],
        [Paragraph("Backend REST API", table_cell_bold), Paragraph("Python 3.12, FastAPI, Uvicorn, Pydantic v2", table_cell_style), Paragraph("High-throughput REST API serving predictions, spatial GeoJSON layers, priorities, and optimizations.", table_cell_style)],
        [Paragraph("Database & GIS", table_cell_bold), Paragraph("PostgreSQL 15 + PostGIS 3.3, SQLAlchemy 2.0, GeoAlchemy2", table_cell_style), Paragraph("Spatial data store for wards, roads, drainage channels, waterbodies, and historical incidents (with SQLite fallback).", table_cell_style)],
        [Paragraph("ML & Explainability", table_cell_bold), Paragraph("XGBoost, LightGBM, scikit-learn, SHAP, Joblib", table_cell_style), Paragraph("Multi-horizon risk probability classification (24h/48h/72h) and SHAP directional feature attribution.", table_cell_style)],
        [Paragraph("Optimization Solver", table_cell_bold), Paragraph("Google OR-Tools (MILP Solver)", table_cell_style), Paragraph("Optimal municipal crew and budget allocation under capacity, skill, and location constraints.", table_cell_style)],
    ]
    tech_table = Table(tech_data, colWidths=[100, 160, 227])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # 10 Core Functional Modules
    story.append(Paragraph("3. Core Platform Modules (10 Functional Systems)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))

    modules = [
        ("1. Geospatial Command Center Map", "Interactive map interface supporting 8 switchable GIS layers: Wards, Roads, Drains, Waterbodies, Historical Incidents, Critical Facilities, Population Heatmaps, and Risk Propagation dependencies."),
        ("2. Historical Pattern Analysis Engine", "Calculates rolling 1h to 72h rainfall aggregations, 7d/30d/90d incident counters, and ward-level recurrence hotspot metrics (HIGH / MEDIUM / LOW)."),
        ("3. Rainfall Analytics & Gauge Tracker", "Monitors rainfall intensity, spatial interpolation across municipal zones, and forecasts versus observed rainfall deviations."),
        ("4. Multi-Horizon Risk Prediction Models", "Versioned XGBoost & LightGBM classifiers predicting waterlogging event probabilities for 24-hour, 48-hour, and 72-hour forecasting windows."),
        ("5. SHAP Explainable AI (XAI)", "Generates directional feature contribution progress bars and human-readable evidence summaries explaining exact rationale for high risk predictions."),
        ("6. Drainage Network Dependency Graph", "Spatial graph modeling topological relationships between drainage channels, road culverts, low-lying zones, and critical infrastructure to locate bottlenecks."),
        ("7. Population & Infrastructure Exposure Estimator", "PostGIS spatial overlap calculations estimating exposed population density and counts of nearby critical facilities (hospitals, schools, transit)."),
        ("8. Civic Priority Engine", "Configurable weighted scoring matrix assigning municipal urgency levels: P1 — CRITICAL, P2 — HIGH, P3 — MEDIUM, and P4 — LOW."),
        ("9. Municipal Crew & Budget Optimizer", "Google OR-Tools MILP solver allocating maintenance crews, working hours, equipment, and budgets to maximize risk reduction under strict operational bounds."),
        ("10. What-If Scenario Simulator", "Multi-stage analytical simulation engine evaluating hypothetical storm intensity spikes and resource re-allocations without altering live database records.")
    ]

    for title, desc in modules:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))

    # Repository & API Structure
    story.append(Paragraph("4. Project Structure & API Endpoints", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))

    repo_summary = (
        "The project repository is structured into distinct, modular subsystems:<br/>"
        "• <b>backend/</b>: FastAPI application, database schemas, ORM models, and service business logic.<br/>"
        "• <b>frontend/</b>: Next.js 14 application with MapLibre/Leaflet rendering and analytics dashboards.<br/>"
        "• <b>ml/</b>: Training pipelines, dataset generators, model artifacts, and SHAP explainers.<br/>"
        "• <b>pipeline/</b>: ETL and data processing scripts.<br/>"
        "• <b>tests/</b>: Comprehensive automated test suite with over 44 unit and integration tests."
    )
    story.append(Paragraph(repo_summary, body_style))

    api_endpoints_data = [
        [Paragraph("Endpoint Group", table_header_style), Paragraph("REST Path", table_header_style), Paragraph("Description", table_header_style)],
        [Paragraph("Health", table_cell_bold), Paragraph("/health", code_style), Paragraph("System status & DB connectivity check", table_cell_style)],
        [Paragraph("Predictions", table_cell_bold), Paragraph("/api/v1/predictions", code_style), Paragraph("24h, 48h, 72h risk probability predictions", table_cell_style)],
        [Paragraph("XAI Explanations", table_cell_bold), Paragraph("/api/v1/explanations/{ward_id}", code_style), Paragraph("SHAP feature importance & rationale", table_cell_style)],
        [Paragraph("Spatial GeoJSON", table_cell_bold), Paragraph("/api/v1/geojson/{layer}", code_style), Paragraph("GIS vector layers for map UI", table_cell_style)],
        [Paragraph("Dependency Graph", table_cell_bold), Paragraph("/api/v1/graph", code_style), Paragraph("Drainage network graph nodes & edges", table_cell_style)],
        [Paragraph("Priority Scoring", table_cell_bold), Paragraph("/api/v1/priority", code_style), Paragraph("P1-P4 municipal urgency ranking", table_cell_style)],
        [Paragraph("Optimization", table_cell_bold), Paragraph("/api/v1/optimization", code_style), Paragraph("OR-Tools crew & budget allocation plan", table_cell_style)],
        [Paragraph("Simulation", table_cell_bold), Paragraph("/api/v1/simulation", code_style), Paragraph("What-If scenario simulation execution", table_cell_style)],
    ]
    api_table = Table(api_endpoints_data, colWidths=[100, 170, 217])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(Spacer(1, 6))
    story.append(api_table)
    story.append(Spacer(1, 14))

    # Setup & Execution Guide
    story.append(Paragraph("5. Local Execution & Automated Verification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))

    setup_box = [
        [Paragraph("<b>Backend Startup (Powershell):</b>", body_bold)],
        [Paragraph("<font face='Courier'>cd backend<br/>python -m venv venv<br/>.\\venv\\Scripts\\Activate.ps1<br/>pip install -r requirements.txt<br/>$env:PYTHONPATH=\"..;.\"<br/>python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload</font>", body_style)],
        [Paragraph("<b>Frontend Startup:</b>", body_bold)],
        [Paragraph("<font face='Courier'>cd frontend<br/>npm install<br/>npm run dev</font>", body_style)],
        [Paragraph("<b>Automated Test Suite (44+ Pytest Tests):</b>", body_bold)],
        [Paragraph("<font face='Courier'>$env:PYTHONPATH=\".;backend\"; .\\backend\\venv\\Scripts\\pytest.exe tests/</font>", body_style)],
    ]
    setup_table = Table(setup_box, colWidths=[487])
    setup_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(setup_table)
    story.append(Spacer(1, 14))

    # Data Provenance & Disclaimers
    story.append(Paragraph("6. Data Provenance & Decision Support Disclaimer", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=0, spaceAfter=8))

    disc_text = (
        "• <b>Data Provenance:</b> Spatial boundaries (wards, roads, elevation) form the core geographic baseline. Synthetic demonstration records carry explicit tags: <i>'DEMO PROTOTYPE — SYNTHETIC DATA & HISTORICAL CIVIC DATA'</i>.<br/>"
        "• <b>Decision Support Scope:</b> Machine learning predictions, priority rankings, and OR-Tools optimization outputs serve as analytical decision-support signals for municipal engineers. They assist in resource prioritization and do not replace physical site inspections.<br/>"
        "• <b>Simulation Isolation:</b> All What-If scenario simulations execute in an isolated analytical memory layer and never overwrite or mutate live production database records."
    )
    story.append(Paragraph(disc_text, body_style))
    story.append(Spacer(1, 15))

    # Footer note block
    footer_note = [
        [Paragraph("Developed for the <b>Smart India Hackathon (SIH)</b>. All rights reserved. | CivicPulse Monsoon Platform", ParagraphStyle('FN', parent=body_style, textColor=MUTED_TEXT, alignment=1))]
    ]
    footer_table = Table(footer_note, colWidths=[487])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ]))
    story.append(footer_table)

    # Build PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "CivicPulse_Monsoon_Project_Details.pdf"
    build_pdf(out_path)
