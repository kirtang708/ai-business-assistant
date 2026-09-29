import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import tempfile
import os
from datetime import datetime



matplotlib.use('Agg')
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors

def get_data_from_db():
    conn = sqlite3.connect('retail.db')
    query = "SELECT * FROM sales"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def create_sales_chart(monthly_data, filename):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_data['Month'], monthly_data['Sales'], marker='o', linewidth=2, markersize=6, color='#6366f1')
    ax.fill_between(range(len(monthly_data)), monthly_data['Sales'], alpha=0.3, color='#6366f1')
    ax.set_xlabel('Month', fontsize=10)
    ax.set_ylabel('Sales ($)', fontsize=10)
    ax.set_title('Monthly Sales Trend', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate(rotation=45)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

def create_category_chart(df, filename):
    category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_list = ['#6366f1', '#8b5cf6', '#d946ef']
    ax.bar(category_sales.index, category_sales.values, color=colors_list)
    ax.set_ylabel('Revenue ($)', fontsize=10)
    ax.set_title('Revenue by Category', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(category_sales.values):
        ax.text(i, v + 10000, f'${v:,.0f}', ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

def create_region_chart(df, filename):
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_list = ['#6366f1', '#8b5cf6', '#d946ef', '#ec4899']
    ax.bar(region_sales.index, region_sales.values, color=colors_list[:len(region_sales)])
    ax.set_ylabel('Revenue ($)', fontsize=10)
    ax.set_title('Revenue by Region', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(region_sales.values):
        ax.text(i, v + 10000, f'${v:,.0f}', ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_pdf_report(monthly_data, ai_summary, filename):
    df = get_data_from_db()
    
    import tempfile
    temp_dir = tempfile.gettempdir()
    sales_chart_path = os.path.join(temp_dir, "sales_chart.png")
    category_chart_path = os.path.join(temp_dir, "category_chart.png")
    region_chart_path = os.path.join(temp_dir, "region_chart.png")
    
    create_sales_chart(monthly_data, sales_chart_path)
    create_category_chart(df, category_chart_path)
    create_region_chart(df, region_chart_path)
    
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        fontName='Helvetica-Bold',
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#6366f1'),
        fontName='Helvetica-Bold',
        spaceAfter=10,
        spaceBefore=10
    )
    
    story.append(Paragraph("Sales Analysis Report", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Executive Summary", heading_style))
    total_revenue = monthly_data['Sales'].sum()
    avg_monthly = monthly_data['Sales'].mean()
    best_month = monthly_data.loc[monthly_data['Sales'].idxmax()]
    worst_month = monthly_data.loc[monthly_data['Sales'].idxmin()]
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Revenue', f'${total_revenue:,.0f}'],
        ['Average Monthly Sales', f'${avg_monthly:,.0f}'],
        ['Best Month', f'{best_month["Month"]} (${best_month["Sales"]:,.0f})'],
        ['Worst Month', f'{worst_month["Month"]} (${worst_month["Sales"]:,.0f})']
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Sales Trend", heading_style))
    if os.path.exists(sales_chart_path):
        story.append(Image(sales_chart_path, width=6*inch, height=3*inch))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("Revenue by Category", heading_style))
    if os.path.exists(category_chart_path):
        story.append(Image(category_chart_path, width=6*inch, height=3*inch))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    story.append(Paragraph("Revenue by Region", heading_style))
    if os.path.exists(region_chart_path):
        story.append(Image(region_chart_path, width=6*inch, height=3*inch))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("AI-Powered Insights", heading_style))
    story.append(Paragraph(ai_summary, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("---", styles['Normal']))
    story.append(Paragraph("Generated by AI Business Assistant | Powered by Claude AI", styles['Normal']))
    
    doc.build(story)
    
    for path in [sales_chart_path, category_chart_path, region_chart_path]:
        if os.path.exists(path):
            os.remove(path)
    
    return filename