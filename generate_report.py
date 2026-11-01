#!/usr/bin/env python3
"""
PDF Report Generator for EV Charging Station Placement and Route Planning System
Uses ReportLab to create a professional NIST University style academic report.
Fixed the <br> tag issue in ReportLab Paragraphs.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.venv', 'lib', 'python3.11', 'site-packages'))

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Custom styles matching NIST reference
styles = getSampleStyleSheet()
nist_blue = colors.HexColor("#003366")

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=nist_blue,
    alignment=1,
    spaceAfter=30
)

heading1_style = ParagraphStyle(
    'Heading1Style',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=nist_blue,
    borderWidth=1,
    borderColor=nist_blue,
    borderPadding=5,
    spaceAfter=15
)

heading2_style = ParagraphStyle(
    'Heading2Style',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.black,
    spaceAfter=10
)

body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontSize=11,
    leading=14,
    justify=True
)

def add_header_footer(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFont('Times-Bold', 12)
    canvas.setFillColor(nist_blue)
    canvas.drawString(inch, A4[1] - 0.5 * inch, "NIST UNIVERSITY")
    canvas.line(inch, A4[1] - 0.6 * inch, A4[0] - inch, A4[1] - 0.6 * inch)
    
    # Footer
    canvas.setFont('Times-Roman', 9)
    canvas.setFillColor(colors.black)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(A4[0] - inch, 0.5 * inch, f"Page {page_num} of 30 | NIST University | EV Charging Station Placement and Route Planning")
    canvas.restoreState()

def generate_report():
    doc = SimpleDocTemplate(
        "EV_Charging_Station_Placement_and_Route_Planning_Report.pdf",
        pagesize=A4,
        rightMargin=inch, leftMargin=inch,
        topMargin=1.5 * inch, bottomMargin=inch
    )
    
    story = []
    
    # --- PAGE 1: COVER ---
    story.append(Paragraph("NIST UNIVERSITY", heading1_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Department of Computer Science and Engineering", styles['Normal']))
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("DESIGN AND ANALYSIS OF ALGORITHMS (DAA) · B.Tech 3rd Semester Project", styles['Normal']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("EV CHARGING STATION PLACEMENT AND ROUTE PLANNING SYSTEM", title_style))
    story.append(Spacer(1, 0.5 * inch))
    
    # Student Info Table
    data = [
        ["Course:", "Design and Analysis of Algorithms"],
        ["Programme:", "B.Tech in Computer Science & Engineering (Data Science)"],
        ["Academic Year:", "2026–27"],
        ["Place:", "NIST University, Berhampur, Odisha"]
    ]
    t = Table(data, colWidths=[2*inch, 3*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(Spacer(1, 1 * inch))
    
    story.append(Paragraph("Submitted To", styles['Heading3']))
    story.append(Paragraph("Faculty Guide: Prof. __________________________", styles['Normal']))
    story.append(Paragraph("Department of Computer Science and Engineering", styles['Normal']))
    story.append(Paragraph("NIST University", styles['Normal']))
    story.append(Spacer(1, 0.5 * inch))
    
    story.append(Paragraph("Submitted By", styles['Heading3']))
    story.append(Paragraph("<strong>Om Prakash Sahu</strong><br/>Roll No: 202556339<br/>B.Tech CSE (Data Science), 3rd Semester", styles['Normal']))
    story.append(Paragraph("<strong>Prasant Nayak</strong><br/>Roll No: 202556393<br/>B.Tech CSE (Data Science), 3rd Semester", styles['Normal']))
    
    story.append(PageBreak())
    
    # --- PAGE 2: CERTIFICATE ---
    story.append(Paragraph("Certificate", heading1_style))
    story.append(Paragraph("This is to certify that the project report entitled <strong>EV Charging Station Placement and Route Planning System</strong> has been prepared by <strong>Om Prakash Sahu (202556339)</strong> and <strong>Prasant Nayak (202556393)</strong>, students of B.Tech CSE (Data Science), 3rd Semester, NIST University, Berhampur, Odisha, for the academic session 2026–27.", body_style))
    story.append(Paragraph("The project demonstrates the implementation of Kruskal's MST, 0/1 Knapsack DP, and Dijkstra's Shortest Path algorithms in a professional web application environment.", body_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("<h3>Internal / External Viva-Voce Examiner Evaluation</h3>", styles['Normal']))
    story.append(Paragraph("Evaluated on Date: ______________________", body_style))
    story.append(Paragraph("Remarks:<br/>________________________________________<br/>________________________________________", body_style))
    story.append(Paragraph("Signature of Examiner & Date<br/>________________________________________", body_style))
    
    story.append(PageBreak())
    
    # --- PAGE 3: DECLARATION ---
    story.append(Paragraph("Declaration", heading1_style))
    story.append(Paragraph("We hereby declare that this project report on <strong>EV Charging Station Placement and Route Planning System</strong> is the result of our original academic work for the Design and Analysis of Algorithms course. The algorithms (Kruskal, Knapsack, Dijkstra) were implemented manually by the students. No fabricated results are included; experimental results are generated from the implemented system.", body_style))
    
    # Student Boxes
    story.append(Spacer(1, 0.5 * inch))
    data_decl = [
        ["Student 1", "Student 2", "Guide / Faculty"],
        ["Om Prakash Sahu\nRoll No: 202556339\nB.Tech CSE (Data Science), 3rd Sem\n\nSignature:\n________________",
         "Prasant Nayak\nRoll No: 202556393\nB.Tech CSE (Data Science), 3rd Sem\n\nSignature:\n________________",
         "Name: __________________________\nDate: __________________________\nSignature: __________________________"]
    ]
    t_decl = Table(data_decl, colWidths=[2*inch, 2*inch, 2*inch])
    t_decl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    story.append(t_decl)
    
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("<strong>Statement of Originality</strong>", styles['Normal']))
    story.append(Paragraph("The work presented herein is original and adheres to NIST University academic standards.", body_style))
    
    story.append(PageBreak())
    
    # --- PAGE 4: ACKNOWLEDGEMENT ---
    story.append(Paragraph("Acknowledgement", heading1_style))
    story.append(Paragraph("We express our sincere gratitude to the Department of Computer Science and Engineering, NIST University, for providing the laboratory resources and academic environment. We thank the open-source community for technologies like Python, Flask, and Leaflet. Special thanks to our classmates for technical support during algorithm testing.", body_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("<h3>Institutional & Academic Submission Summary</h3>", styles['Normal']))
    
    data_ack = [
        ["Project Attribute", "Institutional & Academic Details"],
        ["Project Title", "EV Charging Station Placement and Route Planning System"],
        ["Subject", "Design and Analysis of Algorithms"],
        ["Programme", "B.Tech CSE (Data Science)"],
        ["Semester", "3rd"],
        ["Institution", "NIST University"],
        ["Academic Session", "2026–27"],
        ["Students", "Om Prakash Sahu & Prasant Nayak"],
        ["Roll Numbers", "202556339 & 202556393"],
        ["Core Algorithms", "Kruskal, Dijkstra, 0/1 Knapsack"]
    ]
    t_ack = Table(data_ack, colWidths=[2.5*inch, 3.5*inch])
    t_ack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), nist_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    story.append(t_ack)
    
    story.append(PageBreak())
    
    # --- PAGE 5: ABSTRACT ---
    story.append(Paragraph("Abstract", heading1_style))
    story.append(Paragraph("This report documents the design and implementation of an EV Charging Station Placement and Route Planning System. The system models road networks as weighted graphs and utilizes Kruskal's Minimum Spanning Tree for network analysis, 0/1 Knapsack Dynamic Programming for budget-constrained station selection, and Dijkstra's Shortest Path for route calculation. The application integrates real-world data sources and provides a professional product-grade UI/UX interface.", body_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("<h3>Executive Technical Profile</h3>", styles['Normal']))
    
    data_abs = [
        ["Technical Dimension", "Implementation Specification"],
        ["Application Type", "Deployable Web Application"],
        ["Backend", "Python Flask"],
        ["Frontend", "HTML/CSS/JavaScript (Professional UI)"],
        ["Graph Model", "Weighted Graph"],
        ["MST Algorithm", "Kruskal (Manual)"],
        ["Station Optimization", "0/1 Knapsack (Manual DP)"],
        ["Route Algorithm", "Dijkstra (Manual)"],
        ["Visualization", "Interactive Map (Leaflet/MapLibre)"],
        ["Deployment", "Render (Gunicorn)"],
        ["Testing", "Automated Unit + Integration Tests"]
    ]
    t_abs = Table(data_abs, colWidths=[2.5*inch, 3.5*inch])
    t_abs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), nist_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    story.append(t_abs)
    
    story.append(Paragraph("<h3>Keywords</h3>", styles['Normal']))
    story.append(Paragraph("EV infrastructure, Graph Algorithms, Kruskal, Dijkstra, 0/1 Knapsack, Dynamic Programming, Minimum Spanning Tree, Shortest Path, Route Planning, Optimization.", body_style))
    
    story.append(PageBreak())
    
    # --- PAGE 6: TABLE OF CONTENTS ---
    story.append(Paragraph("Table of Contents", heading1_style))
    toc_data = [
        ["PART 1 — FRONT MATTER", ""],
        ["Cover Page", "1"],
        ["Certificate", "2"],
        ["Declaration", "3"],
        ["Acknowledgement", "4"],
        ["Abstract", "5"],
        ["Table of Contents", "6"],
        ["PART 2 — PROJECT INTRODUCTION AND REQUIREMENT ANALYSIS", ""],
        ["1. Introduction", "7"],
        ["2. Problem Statement and Objectives", "8"],
        ["3. Scope and Feasibility Analysis", "9"],
        ["4. Software and Hardware Requirements", "10"],
        ["PART 3 — ALGORITHMIC DESIGN AND SYSTEM MODELING", ""],
        ["5. System Architecture and Data Flow", "11"],
        ["6. Use-Case Diagram and Functional Specifications", "12"],
        ["7. Graph Model and Network Representation", "13"],
        ["8. Algorithm Design", "14"],
        ["9. Algorithm Complexity Analysis", "15"],
        ["PART 4 — IMPLEMENTATION", ""],
        ["10. Kruskal MST Implementation", "16"],
        ["11. 0/1 Knapsack Implementation", "17"],
        ["12. Dijkstra Shortest Path Implementation", "18"],
        ["13. Integrated Optimization Pipeline", "19"],
        ["PART 5 — APPLICATION AND RESULTS", ""],
        ["14. Web Application Interface", "20"],
        ["15. Graph Visualization and Network Analysis", "21"],
        ["16. Charging Station Optimization Results", "22"],
        ["17. Route Planning Results", "23"],
        ["PART 6 — TESTING, CONCLUSION AND REFERENCES", ""],
        ["18. System Testing", "24"],
        ["19. Results and Discussion", "25"],
        ["20. Limitations and Future Scope", "26"],
        ["21. Conclusion", "27"],
        ["22. References", "28"],
        ["List of Figures", "29"],
        ["List of Tables", "30"]
    ]
    t_toc = Table(toc_data, colWidths=[4.5*inch, 1.5*inch])
    t_toc.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_toc)
    
    # --- CHAPTER 1: INTRODUCTION ---
    story.append(PageBreak())
    story.append(Paragraph("1. Introduction", heading1_style))
    story.append(Paragraph("The adoption of Electric Vehicles (EVs) necessitates robust charging infrastructure. This project models road networks as weighted graphs to optimize station placement under budget constraints and calculate efficient routes using classical DAA algorithms. The system serves as a decision-support platform for urban planners and infrastructure analysts.", body_style))
    
    # --- CHAPTER 8: ALGORITHM DESIGN ---
    story.append(PageBreak())
    story.append(Paragraph("8. Algorithm Design", heading1_style))
    story.append(Paragraph("8.1 Kruskal", heading2_style))
    story.append(Paragraph("Objective: Find Minimum Spanning Tree (MST) of the road network. The manual implementation uses Union-Find with path compression and union by rank.", body_style))
    story.append(Paragraph("<font face='Courier'>def kruskal_mst(nodes, edges): ...</font>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("8.2 0/1 Knapsack", heading2_style))
    story.append(Paragraph("Objective: Maximize benefit within budget constraint. Dynamic Programming table construction and backtracking are used.", body_style))
    story.append(Paragraph("<font face='Courier'>def knapsack(stations, budget): ...</font>", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("8.3 Dijkstra", heading2_style))
    story.append(Paragraph("Objective: Calculate shortest path between source and destination. Priority queue and relaxation are used.", body_style))
    story.append(Paragraph("<font face='Courier'>def dijkstra(graph, source, destination): ...</font>", body_style))
    
    # --- CHAPTER 9: COMPLEXITY ANALYSIS ---
    story.append(PageBreak())
    story.append(Paragraph("9. Complexity Analysis", heading1_style))
    data_comp = [
        ["Algorithm", "Time Complexity", "Space Complexity", "Main Operation"],
        ["Kruskal", "O(E log E)", "O(V+E)", "Edge sorting + Union-Find"],
        ["Dijkstra", "O((V+E) log V)", "O(V+E)", "Relaxation + Min Heap"],
        ["0/1 Knapsack", "O(nW)", "O(nW)", "DP table"]
    ]
    t_comp = Table(data_comp, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), nist_blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black)
    ]))
    story.append(t_comp)
    
    # --- CHAPTER 22: REFERENCES ---
    story.append(PageBreak())
    story.append(Paragraph("22. References", heading1_style))
    refs = [
        "Cormen et al., Introduction to Algorithms",
        "Kleinberg & Tardos, Algorithm Design",
        "Flask Official Documentation (https://flask.palletsprojects.com)",
        "Python Official Documentation (https://python.org)",
        "Render Deployment Documentation (https://render.com)"
    ]
    for ref in refs:
        story.append(Paragraph(f"• {ref}", body_style))
        story.append(Spacer(1, 0.1 * inch))
    
    # Build PDF
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print("PDF Report Generated: EV_Charging_Station_Placement_and_Route_Planning_Report.pdf")

if __name__ == "__main__":
    generate_report()
