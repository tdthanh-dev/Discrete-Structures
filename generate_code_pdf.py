import os
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def format_code_to_html(code_text):
    escaped = html.escape(code_text)
    lines = []
    for line in escaped.splitlines():
        leading_spaces = len(line) - len(line.lstrip(' '))
        # Convert leading spaces to non-breaking spaces
        line_formatted = '&nbsp;' * leading_spaces + line.lstrip(' ')
        lines.append(line_formatted)
    return "<br/>".join(lines)

def make_code_pdf():
    pdf_filename = "Ma_nguon_Giai_thuat_CTRR.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    try:
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_path_italic = "C:\\Windows\\Fonts\\ariali.ttf"
        font_path_mono = "C:\\Windows\\Fonts\\cour.ttf"
        
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdfmetrics.registerFont(TTFont('Arial-Bold', font_path_bold))
        pdfmetrics.registerFont(TTFont('Arial-Italic', font_path_italic))
        pdfmetrics.registerFont(TTFont('CourierNew', font_path_mono))
        
        FONT_NAME = 'Arial'
        FONT_NAME_BOLD = 'Arial-Bold'
        FONT_MONO = 'CourierNew'
    except Exception as e:
        print("Falling back to standard fonts:", e)
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
        FONT_MONO = 'Courier'
        
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=18,
        leading=24,
        textColor=colors.HexColor('#1d3557'),
        alignment=1,
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#457b9d'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1d3557'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2b2d42'),
        spaceAfter=8
    )
    
    code_title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#e63946'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName=FONT_MONO,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1d3557'),
        backColor=colors.HexColor('#f8f9fa'),
        borderColor=colors.HexColor('#a8dadc'),
        borderWidth=0.5,
        borderPadding=10,
        spaceAfter=15
    )
    
    story = []
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("TỔNG HỢP MÃ NGUỒN CÁC GIẢI THUẬT ĐỒ THỊ", title_style))
    story.append(Paragraph("Tài liệu đính kèm chứa mã nguồn Python chuẩn hóa của 8 giải thuật cốt lõi", subtitle_style))
    story.append(Spacer(1, 5))
    
    algorithms = [
        {
            "title": "1. Giải thuật duyệt đồ thị: BFS và DFS",
            "file": "algorithms/traversal.py",
            "desc": "Mã nguồn cài đặt hai giải thuật duyệt đồ thị cơ bản: Breadth-First Search (BFS) sử dụng Queue tuần tự và Depth-First Search (DFS) sử dụng đệ quy hệ thống. Các đỉnh lân cận được sắp xếp theo thứ tự nhãn tăng dần để đảm bảo kết quả chạy vết đồng nhất."
        },
        {
            "title": "2. Kiểm tra đồ thị hai phía (Bipartite Graph Check)",
            "file": "algorithms/bipartite.py",
            "desc": "Mã nguồn kiểm tra đồ thị hai phía sử dụng thuật toán tô hai màu (2-Coloring) thông qua duyệt DFS. Nếu phát hiện chu trình độ dài lẻ (odd cycle), giải thuật sẽ truy vết và trả về chu trình đó làm minh chứng mâu thuẫn."
        },
        {
            "title": "3. Tìm đường đi ngắn nhất: Dijkstra",
            "file": "algorithms/dijkstra.py",
            "desc": "Mã nguồn thuật toán Dijkstra tìm đường đi ngắn nhất từ một đỉnh nguồn tới mọi đỉnh khác trên đồ thị có trọng số không âm. Giải thuật sử dụng cấu trúc hàng đợi ưu tiên (Priority Queue / Heap) để đạt hiệu năng O(E log V) và kiểm tra lỗi nếu có trọng số âm."
        },
        {
            "title": "4. Cây khung nhỏ nhất: Kruskal",
            "file": "algorithms/kruskal.py",
            "desc": "Mã nguồn thuật toán Kruskal tìm cây khung cực tiểu (MST). Thuật toán tiếp cận theo hướng duyệt cạnh (Edge-based): sắp xếp các cạnh theo trọng số tăng dần và dùng cấu trúc dữ liệu Disjoint Set Union (DSU) để kiểm tra chu trình và hợp nhất tập hợp một cách tối ưu."
        },
        {
            "title": "5. Cây khung nhỏ nhất: Prim",
            "file": "algorithms/prim.py",
            "desc": "Mã nguồn thuật toán Prim tìm cây khung cực tiểu (MST). Thuật toán tiếp cận theo hướng duyệt đỉnh (Vertex-based): loang dần cây khung từ đỉnh gốc bằng cách sử dụng hàng đợi ưu tiên Heap để chọn cạnh ngắn nhất nối từ cây ra ngoài."
        },
        {
            "title": "6. Luồng cực đại: Edmonds-Karp",
            "file": "algorithms/max_flow.py",
            "desc": "Mã nguồn thuật toán Edmonds-Karp tìm luồng cực đại trên mạng luồng có hướng/vô hướng. Đây là phiên bản tối ưu của Ford-Fulkerson sử dụng duyệt BFS để tìm đường tăng luồng có ít cạnh nhất trên đồ thị dư (Residual Graph), đảm bảo dừng trong thời gian O(VE^2)."
        },
        {
            "title": "7. Chu trình Euler: Giải thuật Fleury",
            "file": "algorithms/fleury.py",
            "desc": "Mã nguồn tìm đường đi hoặc chu trình Euler sử dụng giải thuật Fleury cho đồ thị vô hướng. Giải thuật kiểm tra tính liên thông và bậc của các đỉnh trước khi đi tham lam, đảm bảo chỉ đi qua cạnh cầu (bridge) khi không còn cạnh nào khác."
        },
        {
            "title": "8. Chu trình Euler: Giải thuật Hierholzer",
            "file": "algorithms/hierholzer.py",
            "desc": "Mã nguồn tìm đường đi hoặc chu trình Euler sử dụng giải thuật Hierholzer. Đây là thuật toán tối ưu có độ phức tạp O(E) bằng cách xây dựng và lồng ghép các chu trình con đơn giản thông qua cơ chế Ngăn xếp (Stack)."
        }
    ]
    
    for i, algo in enumerate(algorithms):
        if i > 0:
            story.append(PageBreak())
            
        story.append(Paragraph(algo["title"], h1_style))
        story.append(Paragraph(algo["desc"], body_style))
        
        filepath = os.path.join("d:\\2026_For_Job\\CTRR\\CTRR", algo["file"])
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                code_content = f.read()
                
            story.append(Paragraph(f"Tệp tin nguồn: <i>{algo['file']}</i>", code_title_style))
            
            # Format and append code directly as a paragraph
            html_code = format_code_to_html(code_content)
            story.append(Paragraph(html_code, code_style))
        else:
            story.append(Paragraph(f"[Lỗi] Không tìm thấy tệp tin {algo['file']}", code_title_style))
            
    doc.build(story)
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    make_code_pdf()
