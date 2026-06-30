import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def make_table_pdf():
    pdf_filename = "bang_phan_chia_cong_viec.pdf"
    
    # Page setup with 40pt margins for a clean, balanced layout
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    try:
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_path_italic = "C:\\Windows\\Fonts\\ariali.ttf"
        
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdfmetrics.registerFont(TTFont('Arial-Bold', font_path_bold))
        pdfmetrics.registerFont(TTFont('Arial-Italic', font_path_italic))
        
        FONT_NAME = 'Arial'
        FONT_NAME_BOLD = 'Arial-Bold'
        FONT_NAME_ITALIC = 'Arial-Italic'
    except Exception as e:
        print("Falling back to standard fonts:", e)
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
        FONT_NAME_ITALIC = 'Helvetica-Oblique'
        
    styles = getSampleStyleSheet()
    
    # Theme colors
    PRIMARY_COLOR = colors.HexColor('#1e3a8a')  # Deep Indigo
    TEXT_MAIN = colors.HexColor('#1e293b')      # Slate 800
    TEXT_MUTED = colors.HexColor('#475569')     # Slate 600
    ACCENT_BLUE = '#3b82f6'                     # Royal Blue
    
    # Styles for table cells
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=10,
        leading=14,
        textColor=colors.white
    )
    
    col1_style = ParagraphStyle(
        'Col1Style',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=9.5,
        leading=14,
        textColor=PRIMARY_COLOR
    )
    
    col2_style = ParagraphStyle(
        'Col2Style',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=9.5,
        leading=14,
        textColor=TEXT_MAIN
    )
    
    col3_style = ParagraphStyle(
        'Col3Style',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14.5,
        textColor=TEXT_MUTED,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=6
    )
    
    headers = [
        Paragraph("Thành viên", header_style),
        Paragraph("Nhóm Thuật toán chịu trách nhiệm", header_style),
        Paragraph("Chi tiết phần việc (Thuật toán + GUI)", header_style)
    ]
    
    # Bullets formatted with colored bullet points and proper typography rendering
    bullet_prefix = f'<font color="{ACCENT_BLUE}"><b>•</b></font> '
    
    data = [
        headers,
        [
            Paragraph("Thành viên 1", col1_style),
            Paragraph("Duyệt đồ thị &amp;<br/>Biểu diễn đồ thị", col2_style),
            [
                Paragraph(f"{bullet_prefix}Viết mô-đun chuyển đổi cấu trúc (Ma trận kề, ds kề, ds cạnh cho cả đồ thị vô hướng &amp; có hướng) ở <font color='#0284c7'><b>utils/conversions.py</b></font>.", col3_style),
                Paragraph(f"{bullet_prefix}Cài đặt thuật toán duyệt <b>BFS &amp; DFS</b> thuần và generator.", col3_style),
                Paragraph(f"{bullet_prefix}Tích hợp tương tác vẽ đồ thị trực quan (thêm/xóa đỉnh, nối cạnh) và hoạt họa BFS/DFS lên GUI.", col3_style)
            ]
        ],
        [
            Paragraph("Thành viên 2", col1_style),
            Paragraph("Đường đi ngắn nhất &amp;<br/>Đồ thị hai phía", col2_style),
            [
                Paragraph(f"{bullet_prefix}Cài đặt giải thuật <b>Dijkstra</b> sử dụng Priority Queue (Min-Heap), kiểm soát trọng số âm.", col3_style),
                Paragraph(f"{bullet_prefix}Cài đặt thuật toán kiểm tra <b>Đồ thị 2 phía</b> (tô màu BFS/DFS), truy vết ngược lấy chu trình lẻ làm minh chứng phản ví dụ.", col3_style),
                Paragraph(f"{bullet_prefix}Tích hợp highlight lộ trình Dijkstra và vẽ màu đỏ/xanh (hoặc highlight chu trình lẻ) lên GUI.", col3_style)
            ]
        ],
        [
            Paragraph("Thành viên 3", col1_style),
            Paragraph("Cây khung nhỏ nhất<br/>(MST)", col2_style),
            [
                Paragraph(f"{bullet_prefix}Cài đặt thuật toán <b>Prim</b> (dùng Heap).", col3_style),
                Paragraph(f"{bullet_prefix}Cài đặt thuật toán <b>Kruskal</b> sắp xếp cạnh kết hợp cấu trúc dữ liệu tập hợp rời rạc (<b>DSU</b>) để phát hiện chu trình nhanh <i>O</i>(1).", col3_style),
                Paragraph(f"{bullet_prefix}Tích hợp trực quan hóa cây khung nhỏ nhất (MST) và tính tổng trọng số lên GUI.", col3_style)
            ]
        ],
        [
            Paragraph("Thành viên 4", col1_style),
            Paragraph("Luồng cực đại<br/>(Max Flow)", col2_style),
            [
                Paragraph(f"{bullet_prefix}Cài đặt thuật toán <b>Edmonds-Karp</b> (phương pháp Ford-Fulkerson tối ưu hóa đường đi ngắn nhất bằng BFS trên mạng dư).", col3_style),
                Paragraph(f"{bullet_prefix}Tích hợp hiển thị tỷ lệ <code>flow/capacity</code> thực tế trên các cạnh và highlight các đường tăng luồng qua từng bước.", col3_style),
                Paragraph(f"{bullet_prefix}Cài đặt chức năng Lưu/Tải đồ thị (JSON) và xuất ảnh Canvas (PNG/PostScript).", col3_style),
                Paragraph(f"{bullet_prefix}Phụ giúp Thành viên 1 xây dựng khung Canvas vẽ đồ thị chính.", col3_style)
            ]
        ],
        [
            Paragraph("Thành viên 5", col1_style),
            Paragraph("Đường đi &amp;<br/>Chu trình Euler", col2_style),
            [
                Paragraph(f"{bullet_prefix}Cài đặt giải thuật <b>Fleury</b> (duyệt kiểm tra và tránh các cạnh cầu - bridge).", col3_style),
                Paragraph(f"{bullet_prefix}Cài đặt giải thuật <b>Hierholzer</b> tối ưu <i>O</i>(E) sử dụng cơ chế lưu trữ Stack.", col3_style),
                Paragraph(f"{bullet_prefix}Tích hợp mô phỏng bước đi của Fleury và cơ chế push/pop đỉnh vào Stack của Hierholzer lên GUI.", col3_style)
            ]
        ]
    ]
    
    # A4 dimensions: 595.27 x 841.89
    # Left margin: 40, Right margin: 40 -> Printable width: 515.27
    col_widths = [85, 120, 310]
    
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        # Header style with deep blue color
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Zebra striping for readability
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#ffffff')),
        
        # Premium minimalist borders (only horizontal lines, no vertical lines)
        ('LINEABOVE', (0, 0), (-1, 0), 1, PRIMARY_COLOR),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, PRIMARY_COLOR),  # Thicker divider under header
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),  # Thin divider under rows
        
        # Generous cell padding for breathing room
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    
    story = [t]
    doc.build(story)
    print(f"Successfully generated premium PDF: {pdf_filename}")

if __name__ == "__main__":
    make_table_pdf()
