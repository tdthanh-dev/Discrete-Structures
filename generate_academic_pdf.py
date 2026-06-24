import os
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def format_code_to_html(code_text):
    escaped = html.escape(code_text)
    lines = []
    for line in escaped.splitlines():
        # Replace spaces with non-breaking spaces to preserve formatting in monospaced block
        line_formatted = line.replace(' ', '\u00A0')
        lines.append(line_formatted)
    return "<br/>".join(lines)

def make_comprehensive_pdf():
    pdf_filename = "Cam_nang_Chi_tiet_Giai_thuat_Do_thi_ReportLab.pdf"
    
    # SimpleDocTemplate with A4 and Margins set to 54pt (approx. 2cm)
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    # Font Registration (Standard Windows Fonts)
    try:
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
        font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_path_italic = "C:\\Windows\\Fonts\\ariali.ttf"
        font_path_mono = "C:\\Windows\\Fonts\\cour.ttf"
        font_path_mono_bold = "C:\\Windows\\Fonts\\courbd.ttf"
        
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdfmetrics.registerFont(TTFont('Arial-Bold', font_path_bold))
        pdfmetrics.registerFont(TTFont('Arial-Italic', font_path_italic))
        pdfmetrics.registerFont(TTFont('Courier', font_path_mono))
        pdfmetrics.registerFont(TTFont('Courier-Bold', font_path_mono_bold))
        
        FONT_NAME = 'Arial'
        FONT_NAME_BOLD = 'Arial-Bold'
        FONT_NAME_ITALIC = 'Arial-Italic'
        FONT_MONO = 'Courier'
        FONT_MONO_BOLD = 'Courier-Bold'
    except Exception as e:
        print("Falling back to standard Helvetica/Courier:", e)
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
        FONT_NAME_ITALIC = 'Helvetica-Oblique'
        FONT_MONO = 'Courier'
        FONT_MONO_BOLD = 'Courier-Bold'
        
    styles = getSampleStyleSheet()
    
    # ----------------------------------------------------
    # DESIGN STYLES DEFINITION
    # ----------------------------------------------------
    
    # Document Title Style
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=22,
        leading=28,
        textColor=colors.HexColor('#1A365D'), # Navy Blue
        alignment=1,
        spaceAfter=15
    )
    
    # Subtitle Style
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#457b9d'),
        alignment=1,
        spaceAfter=30
    )
    
    # Main Section Heading (H1) - Roman Numerals
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=13.5,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    # H2 Text Style (Inside Table Heading wrapper)
    h2_text_style = ParagraphStyle(
        'H2Text',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#005A70'), # Teal
    )
    
    # Body Text Style
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#2D3748'), # Dark charcoal
        spaceAfter=8
    )
    
    # Bold Body Text
    body_bold_style = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName=FONT_NAME_BOLD
    )
    
    # Bullet List Style
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    # Math & Callout Box Text Style (Inside Table wrapper)
    callout_text_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
    )
    
    # Code Title Style
    code_title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#e63946'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    # Monospaced Code Block Text Style (Inside Table wrapper)
    code_text_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName=FONT_MONO,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#F8F9FA'), # White text
    )
    
    # Table Content Styles
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2D3748')
    )
    
    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName=FONT_NAME_BOLD,
        textColor=colors.HexColor('#1A365D')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=table_cell_style,
        fontName=FONT_NAME_BOLD,
        fontSize=9,
        leading=12,
        textColor=colors.white
    )
    
    # ----------------------------------------------------
    # TABLE WRAPPER HELPER FUNCTIONS (PREVENT OVERLAPS)
    # ----------------------------------------------------
    
    def make_h2_heading(text):
        p = Paragraph(text, h2_text_style)
        t = Table([[p]], colWidths=[487.27])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
            ('LINELEFT', (0,0), (-1,-1), 3, colors.HexColor('#005A70')), # Left Teal Border Accent
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        t.spaceBefore = 12
        t.spaceAfter = 8
        t.keepWithNext = True
        return t

    def make_callout_box(text):
        p = Paragraph(text, callout_text_style)
        t = Table([[p]], colWidths=[487.27])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF9E6')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FFE0B2')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        t.spaceBefore = 6
        t.spaceAfter = 10
        return t

    def make_code_block(code_text):
        formatted_html = format_code_to_html(code_text)
        p = Paragraph(formatted_html, code_text_style)
        t = Table([[p]], colWidths=[487.27])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E1E1E')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        t.spaceBefore = 6
        t.spaceAfter = 12
        return t

    story = []
    
    # ----------------------------------------------------
    # PAGE 1: COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("CẨM NANG KỸ THUẬT & HƯỚNG DẪN THỰC HÀNH HỌC THUẬT", title_style))
    story.append(Paragraph("Thiết kế, Phân tích Toán học, Phân chia Công việc và Phát triển Hệ thống Trực quan hóa Đồ thị", subtitle_style))
    story.append(Spacer(1, 15))
    
    abstract_text = (
        "<b>TÓM TẮT TÀI LIỆU (ABSTRACT):</b><br/>"
        "Tài liệu này được biên soạn bởi Chuyên gia Giáo dục Công nghệ và Kỹ sư Lập trình Python cấp cao làm cẩm nang học thuật "
        "toàn diện cho dự án xây dựng ứng dụng trực quan hóa giải thuật đồ thị phục vụ giảng dạy môn Cấu trúc rời rạc. "
        "Tài liệu cung cấp cơ sở toán học chặt chẽ bằng ký hiệu Unicode trực quan, phân tích chi tiết ý tưởng cốt lõi và độ phức tạp "
        "của 9 thuật toán đồ thị cơ bản & nâng cao. Đồng thời, tài liệu cung cấp mã khung (Skeleton Code) chuẩn hóa kèm theo giải thích "
        "từng dòng code, bảng phân chia công việc tối ưu cho nhóm 5 người, và hướng dẫn chi tiết quy trình chuyển đổi mã nguồn thuần "
        "sang hoạt họa (Generator yield) tích hợp với mô hình xử lý bất đồng bộ của tkinter (tkinter.after). Đây là cẩm nang hướng dẫn "
        "chuẩn mực để triển khai hệ thống phần mềm giáo dục đạt chất lượng học thuật cao nhất."
    )
    story.append(Paragraph(abstract_text, body_style))
    story.append(Spacer(1, 20))
    
    toc_text = (
        "<b>MỤC LỤC TÀI LIỆU:</b><br/>"
        "I. Kiến trúc Hệ thống Trực quan hóa Đồ thị (Trang 2)<br/>"
        "II. Phân tích Toán học & Hướng dẫn Cài đặt 9 Giải thuật Cốt lõi (Trang 2-10)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. Duyệt đồ thị theo chiều rộng (BFS) (Trang 2-3)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. Duyệt đồ thị theo chiều sâu (DFS) (Trang 3-4)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. Kiểm tra đồ thị hai phía (Bipartite Graph) (Trang 4-5)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;4. Tìm đường đi ngắn nhất (Dijkstra) (Trang 5-6)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5. Cây khung nhỏ nhất - Thuật toán Prim (Trang 6-7)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;6. Cây khung nhỏ nhất - Thuật toán Kruskal (Trang 7-8)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;7. Luồng cực đại trên mạng - Edmonds-Karp (Trang 8-9)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8. Chu trình Euler - Thuật toán Fleury (Trang 9)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;9. Chu trình Euler - Thuật toán Hierholzer (Trang 10)<br/>"
        "III. Bảng phân công công việc nhóm 5 người (Trang 11)<br/>"
        "IV. Quy trình phối hợp, Pipeline CI & Tiêu chuẩn hoàn thành (DoD) (Trang 11-12)"
    )
    story.append(Paragraph(toc_text, body_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: SYSTEM ARCHITECTURE & ALGORITHM 1: BFS
    # ----------------------------------------------------
    story.append(Paragraph("I. KIẾN TRÚC HỆ THỐNG TRỰC QUAN HÓA ĐỒ THỊ", h1_style))
    story.append(Paragraph(
        "Hệ thống được thiết kế theo nguyên lý phân tách mối quan tâm (Separation of Concerns) để đảm bảo tính độc lập tối đa "
        "giữa logic nghiệp vụ (thuật toán đồ thị) và tầng hiển thị tương tác (GUI):<br/>"
        "1. <b>Tầng Utility (Biểu diễn đồ thị):</b> Cài đặt trong <code>utils/conversions.py</code> để chuyển đổi tự động qua lại giữa "
        "Ma trận kề, Danh sách kề, Danh sách cạnh. Hỗ trợ cho cả đồ thị vô hướng và có hướng nhằm tối ưu dữ liệu đầu vào cho các thuật toán khác nhau.<br/>"
        "2. <b>Tầng Core Algorithm (Độc lập):</b> Đặt trong <code>algorithms/pure/</code>. Các thuật toán ở đây chỉ thực hiện tính toán thuần túy trên cấu trúc dữ liệu cơ bản, không có bất kỳ thư viện giao diện nào, rất phù hợp để kiểm thử đơn vị (Unit Test) và chấm điểm tự động.<br/>"
        "3. <b>Tầng Generator (Animation):</b> Đặt trong <code>algorithms/</code>. Đây là các hàm đồng hành cùng thuật toán thuần, được sửa đổi cấu trúc sử dụng từ khóa <code>yield</code> ở các điểm chốt của giải thuật nhằm trả dữ liệu trạng thái hiện tại (Đỉnh đang xét, Cạnh đang duyệt, Khoảng cách) về cho giao diện cập nhật thời gian thực.<br/>"
        "4. <b>Tầng Giao diện (Tkinter GUI):</b> Nằm ở <code>gui.py</code>, lắng nghe các tương tác chuột để vẽ đồ thị, sau đó liên kết bộ lặp thời gian bất đồng bộ của Tkinter để lấy dữ liệu từ Generator vẽ hoạt họa.",
        body_style
    ))
    
    story.append(Paragraph("II. PHÂN TÍCH TOÁN HỌC & HƯỚNG DẪN CÀI ĐẶT 9 GIẢI THUẬT CỐT LÕI", h1_style))
    
    story.append(make_h2_heading("1. Duyệt đồ thị theo chiều rộng (BFS)"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> BFS hoạt động theo nguyên lý loang đều. Từ đỉnh nguồn s, thuật toán duyệt qua các đỉnh kề trực tiếp "
        "của s, sau đó mới di chuyển sang các đỉnh kề có khoảng cách xa hơn. Thuật toán sử dụng cấu trúc dữ liệu <b>Hàng đợi (Queue)</b> "
        "để quản lý thứ tự các đỉnh chuẩn bị duyệt theo nguyên tắc FIFO (Vào trước, ra trước).",
        body_style
    ))
    
    bfs_math = (
        "<b>Cơ sở Toán học:</b><br/>"
        "Cho đồ thị G = (V, E) và đỉnh nguồn s ∈ V. Khởi tạo mảng đã thăm: visited[v] = False với mọi v ∈ V, riêng visited[s] = True.<br/>"
        "Hàng đợi Q ban đầu chứa s. Ở mỗi bước, lấy u ra khỏi đầu Q. Với mỗi v ∈ Adj(u):<br/>"
        "Nếu visited[v] == False ⇒ visited[v] = True, đẩy v vào cuối Q, ghi nhận cạnh (u, v) thuộc cây duyệt BFS."
    )
    story.append(make_callout_box(bfs_math))
    
    code_bfs = (
        "from collections import deque\n\n"
        "def bfs(graph, start):\n"
        "    visited = []\n"
        "    visited_set = {start}\n"
        "    queue = deque([start])\n"
        "    traversal_edges = []\n"
        "    while queue:\n"
        "        u = queue.popleft() # Lay dinh u khoi dau queue\n"
        "        visited.append(u)\n"
        "        # Sorting de dam bao tinh deterministic (thu tu duyet dong nhat)\n"
        "        for v, w in sorted(graph.get(u, []), key=lambda x: x[0]):\n"
        "            if v not in visited_set:\n"
        "                visited_set.add(v)\n"
        "                queue.append(v) # Day dinh kề v vao cuoi queue\n"
        "                traversal_edges.append((u, v, w))\n"
        "    return visited, traversal_edges"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Pure BFS):", code_title_style))
    story.append(make_code_block(code_bfs))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 3: BFS DETAILS & ALGORITHM 2: DFS
    # ----------------------------------------------------
    bfs_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 1:</i> Sử dụng <code>collections.deque</code> để tối ưu hóa thời gian POP ở đầu hàng đợi trong O(1).<br/>"
        "• <i>Dòng 5:</i> Đăng ký cấu trúc Queue lưu trữ đỉnh nguồn ban đầu.<br/>"
        "• <i>Dòng 10:</i> Duyệt các đỉnh lân cận và sử dụng hàm <code>sorted</code> theo tên nhãn để kết quả duyệt không bị thay đổi phụ thuộc vào thứ tự nhập cạnh ban đầu, đảm bảo tính nhất quán (deterministic) khi chấm điểm.<br/>"
        "• <i>Dòng 13:</i> Đẩy đỉnh kề chưa thăm vào cuối queue, ghi nhận vết cạnh duyệt đồ thị phục vụ trực quan hóa."
    )
    story.append(Paragraph(bfs_explain, body_style))
    
    bfs_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> Tốt nhất = Xấu nhất = O(V + E) vì thuật toán phải kiểm tra mọi đỉnh và mọi cạnh kề.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V) để lưu trữ hàng đợi Q và tập hợp visited_set chứa tối đa V đỉnh."
    )
    story.append(make_callout_box(bfs_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("2. Duyệt đồ thị theo chiều sâu (DFS)"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> DFS đi theo nguyên lý tìm kiếm ưu tiên chiều sâu. Xuất phát từ một đỉnh nguồn s, thuật toán chọn "
        "đi xa nhất có thể dọc theo mỗi nhánh của đồ thị trước khi thực hiện quay lui (Backtracking). Thuật toán sử dụng cơ chế "
        "<b>Ngăn xếp (Stack)</b>, thường được cài đặt một cách tự nhiên thông qua Đệ quy hệ thống.",
        body_style
    ))
    
    dfs_math = (
        "<b>Cơ sở Toán học:</b><br/>"
        "Cho đồ thị G = (V, E) và đỉnh nguồn s. Đặt visited[v] = False với mọi v ∈ V.<br/>"
        "Định nghĩa hàm đệ quy DFS(u): đánh dấu visited[u] = True. Với mỗi v ∈ Adj(u) sao cho visited[v] == False,<br/>"
        "ghi nhận cạnh (u, v) thuộc cây duyệt DFS, sau đó gọi đệ quy DFS(v)."
    )
    story.append(make_callout_box(dfs_math))
    
    code_dfs = (
        "def dfs(graph, start):\n"
        "    visited = []\n"
        "    visited_set = set()\n"
        "    traversal_edges = []\n"
        "    \n"
        "    def dfs_recursive(u):\n"
        "        visited_set.add(u)\n"
        "        visited.append(u)\n"
        "        # Sap xep dinh ke de ket qua nhat quan\n"
        "        for v, w in sorted(graph.get(u, []), key=lambda x: x[0]):\n"
        "            if v not in visited_set:\n"
        "                traversal_edges.append((u, v, w))\n"
        "                dfs_recursive(v) # Goi de quy di sau xuong dinh v\n"
        "                \n"
        "    dfs_recursive(start)\n"
        "    return visited, traversal_edges"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Pure DFS):", code_title_style))
    story.append(make_code_block(code_dfs))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 4: DFS DETAILS & ALGORITHM 3: BIPARTITE CHECK
    # ----------------------------------------------------
    dfs_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 5:</i> Định nghĩa hàm đệ quy lồng (closure) <code>dfs_recursive</code> để truy cập trực tiếp các biến chung mà không cần truyền tham chiếu đồ thị.<br/>"
        "• <i>Dòng 11:</i> Ghi nhận vết cạnh đi xuôi theo chiều sâu trước khi thực hiện gọi đệ quy ở dòng tiếp theo.<br/>"
        "• <i>Dòng 12:</i> Gọi đệ quy chuyển quyền điều khiển sang đỉnh kề v, cơ chế stack hệ thống sẽ lưu vết đỉnh u để quay lui khi nhánh v duyệt xong."
    )
    story.append(Paragraph(dfs_explain, body_style))
    
    dfs_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> Tốt nhất = Xấu nhất = O(V + E) do phải viếng thăm mọi đỉnh và duyệt qua danh sách kề.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V) phụ thuộc vào độ sâu tối đa của ngăn xếp đệ quy trong trường hợp đồ thị dạng đường thẳng."
    )
    story.append(make_callout_box(dfs_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("3. Kiểm tra đồ thị hai phía (Bipartite Graph Check)"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Sử dụng giải thuật tô 2 màu (2-Coloring). Ta xuất phát từ một đỉnh chưa tô màu, tô màu 0. "
        "Duyệt qua các đỉnh kề của nó và tô màu nghịch đảo là 1. Nếu phát hiện một đỉnh kề đã được tô màu và màu của nó "
        "trùng với màu của đỉnh hiện tại, đồ thị không phải là hai phía. Để tăng tính học thuật, thuật toán thực hiện "
        "truy vết mảng cha để tìm ra <b>chu trình lẻ (odd cycle)</b> làm minh chứng phản ví dụ.",
        body_style
    ))
    
    bip_math = (
        "<b>Cơ sở Toán học:</b><br/>"
        "Đồ thị G = (V, E) là đồ thị hai phía khi và chỉ khi G không chứa chu trình độ dài lẻ.<br/>"
        "Hàm tô màu c: V → {0, 1}. Nếu tồn tại cạnh (u, v) ∈ E sao cho c(u) == c(v) ⇒ đồ thị chứa chu trình lẻ "
        "độ dài 2k + 1 kết nối u, v và đỉnh tổ tiên chung gần nhất."
    )
    story.append(make_callout_box(bip_math))
    
    code_bip = (
        "def check_bipartite(graph):\n"
        "    color = {} # Map luu mau cua tung dinh\n"
        "    parent = {}\n"
        "    for start_node in graph:\n"
        "        if start_node not in color:\n"
        "            color[start_node] = 0\n"
        "            stack = [(start_node, 0)]\n"
        "            while stack:\n"
        "                u, c = stack[-1]\n"
        "                unvisited_found = False\n"
        "                for v, _ in graph.get(u, []):\n"
        "                    if v not in color:\n"
        "                        color[v] = 1 - c # To mau nguoc lai cho dinh ke\n"
        "                        parent[v] = u\n"
        "                        stack.append((v, 1 - c))\n"
        "                        unvisited_found = True\n"
        "                        break\n"
        "                    elif color[v] == color[u]:\n"
        "                        # Phat hien xung dot, truy vet lay chu trinh le\n"
        "                        cycle = [v, u]\n"
        "                        curr = u\n"
        "                        while curr in parent and curr != v:\n"
        "                            curr = parent[curr]\n"
        "                            cycle.append(curr)\n"
        "                        return False, cycle[::-1]\n"
        "                if not unvisited_found: stack.pop()\n"
        "    return True, color"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Bipartite Check):", code_title_style))
    story.append(make_code_block(code_bip))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 5: BIPARTITE DETAILS & ALGORITHM 4: DIJKSTRA
    # ----------------------------------------------------
    bip_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 11:</i> Sử dụng kỹ thuật tô màu đảo <code>1 - c</code> (nếu màu hiện tại là 0 thì tô 1, ngược lại nếu là 1 thì tô 0).<br/>"
        "• <i>Dòng 16:</i> Khi phát hiện <code>color[v] == color[u]</code>, ta tìm thấy cạnh vi phạm điều kiện đồ thị hai phía.<br/>"
        "• <i>Dòng 18-21:</i> Dùng mảng <code>parent</code> đi ngược từ u về v để thu thập danh sách các đỉnh tạo nên chu trình lẻ gây mâu thuẫn làm minh chứng hiển thị lên giao diện."
    )
    story.append(Paragraph(bip_explain, body_style))
    
    bip_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(V + E) do duyệt qua các đỉnh và cạnh để tô màu.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V) để lưu trữ bảng màu và cây khung cha của mảng parent."
    )
    story.append(make_callout_box(bip_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("4. Tìm đường đi ngắn nhất (Dijkstra)"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Dijkstra giải bài toán đường đi ngắn nhất từ một nguồn trên đồ thị có trọng số không âm. "
        "Thuật toán duy trì tập các đỉnh đã tìm ra đường đi ngắn nhất cố định. Ở mỗi bước, chọn một đỉnh u chưa cố định "
        "có khoảng cách ước lượng nhỏ nhất, cố định nó, và thực hiện nới lỏng các cạnh kề của u.",
        body_style
    ))
    
    dijkstra_math = (
        "<b>Cơ sở Toán học (Nguyên lý nới lỏng - Relaxation):</b><br/>"
        "Gọi d[v] là khoảng cách ngắn nhất ước lượng từ nguồn S tới v. Với mọi cạnh (u, v) ∈ E:<br/>"
        "Nếu d[u] + w(u, v) &lt; d[v] ⇒ Cập nhật d[v] = d[u] + w(u, v) và đặt prev[v] = u.<br/>"
        "Để tối ưu hóa bước tìm min{d[u]}, sử dụng cấu trúc Min-Heap với khóa là d[u]."
    )
    story.append(make_callout_box(dijkstra_math))
    
    code_dijkstra = (
        "import heapq\n\n"
        "def dijkstra(graph, start):\n"
        "    dist = {node: float('inf') for node in graph}\n"
        "    prev = {node: None for node in graph}\n"
        "    dist[start] = 0\n"
        "    pq = [(0, start)] # Min-heap chua cap (khoang_cach, dinh)\n"
        "    while pq:\n"
        "        d, u = heapq.heappop(pq)\n"
        "        if d > dist[u]:\n"
        "            continue # Dinh da duoc toi uu tu truoc, bo qua\n"
        "        for v, w in graph.get(u, []):\n"
        "            if w < 0:\n"
        "                raise ValueError(\"Do thi chua canh am, Dijkstra khong ho tro!\")\n"
        "            if dist[u] + w < dist[v]:\n"
        "                dist[v] = dist[u] + w\n"
        "                prev[v] = u\n"
        "                heapq.heappush(pq, (dist[v], v))\n"
        "    return dist, prev"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Dijkstra):", code_title_style))
    story.append(make_code_block(code_dijkstra))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 6: DIJKSTRA DETAILS & ALGORITHM 5: PRIM
    # ----------------------------------------------------
    dijkstra_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 7:</i> Hàm <code>heapq.heappop</code> lấy ra đỉnh u có đường đi ngắn nhất tạm thời trong O(log V) thời gian.<br/>"
        "• <i>Dòng 8:</i> Kiểm tra <code>d > dist[u]</code> để loại bỏ các trạng thái cũ đã được tối ưu trước đó trong hàng đợi.<br/>"
        "• <i>Dòng 11-12:</i> Kiểm tra lỗi trọng số âm để dừng chương trình một cách an toàn, tránh vòng lặp vô hạn.<br/>"
        "• <i>Dòng 13-16:</i> Thực hiện phép nới lỏng và đẩy cập nhật mới vào heap."
    )
    story.append(Paragraph(dijkstra_explain, body_style))
    
    dijkstra_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(E log V) do mỗi cạnh được nới lỏng tối đa một lần và chi phí heap là log V.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V) để lưu trữ khoảng cách, vết và cấu trúc dữ liệu của Min-Heap."
    )
    story.append(make_callout_box(dijkstra_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("5. Cây khung nhỏ nhất - Thuật toán Prim"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Thuật toán Prim tiếp cận bài toán tìm cây khung nhỏ nhất (MST) theo hướng duyệt đỉnh. "
        "Bắt đầu từ một đỉnh nguồn bất kỳ, cây khung được mở rộng bằng cách liên tục chọn cạnh có trọng số nhỏ nhất "
        "kết nối giữa một đỉnh đã nằm trong cây với một đỉnh chưa nằm trong cây.",
        body_style
    ))
    
    prim_math = (
        "<b>Cơ sở Toán học:</b><br/>"
        "Gọi T là tập các đỉnh đã kết nạp vào cây khung (ban đầu T = {start}).<br/>"
        "Tại mỗi bước, chọn cạnh (u, v) ∈ E sao cho u ∈ T, v ∉ T và w(u, v) = min{w(x, y) | x ∈ T, y ∉ T}.<br/>"
        "Đưa v vào T, thêm cạnh (u, v) vào tập cạnh MST. Lặp lại cho đến khi T chứa tất cả các đỉnh."
    )
    story.append(make_callout_box(prim_math))
    
    code_prim = (
        "import heapq\n\n"
        "def prim(node_count, graph, start=0):\n"
        "    visited = {start}\n"
        "    mst = []\n"
        "    total_weight = 0\n"
        "    pq = [] # Heap luu cac canh ung vien dang (trong_so, u, v)\n"
        "    for v, w in graph.get(start, []):\n"
        "        heapq.heappush(pq, (w, start, v))\n"
        "    while pq and len(visited) < node_count:\n"
        "        w, u, v = heapq.heappop(pq)\n"
        "        if v not in visited:\n"
        "            visited.add(v)\n"
        "            mst.append((u, v, w))\n"
        "            total_weight += w\n"
        "            for next_v, next_w in graph.get(v, []):\n"
        "                if next_v not in visited:\n"
        "                    heapq.heappush(pq, (next_w, v, next_v))\n"
        "    return mst, total_weight"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Prim):", code_title_style))
    story.append(make_code_block(code_prim))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 7: PRIM DETAILS & ALGORITHM 6: KRUSKAL
    # ----------------------------------------------------
    prim_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 7-8:</i> Đẩy tất cả các cạnh kề của đỉnh gốc xuất phát vào Min-Heap làm tập ứng viên ban đầu.<br/>"
        "• <i>Dòng 11:</i> Lấy ra cạnh có trọng số nhỏ nhất. Kiểm tra <code>v not in visited</code> để tránh kết nạp cạnh tạo chu trình với các đỉnh đã nằm trong cây.<br/>"
        "• <i>Dòng 15-17:</i> Khi đưa v vào cây, bổ sung các cạnh kết nối từ v tới các đỉnh bên ngoài cây vào Heap."
    )
    story.append(Paragraph(prim_explain, body_style))
    
    prim_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(E log V) vì mỗi đỉnh được duyệt một lần và các cạnh được thêm/bớt khỏi Heap.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V + E) để lưu trữ thông tin các cạnh kề trong Heap."
    )
    story.append(make_callout_box(prim_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("6. Cây khung nhỏ nhất - Thuật toán Kruskal"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Thuật toán Kruskal tiếp cận tìm MST theo hướng duyệt cạnh. Thuật toán sắp xếp toàn bộ cạnh "
        "của đồ thị theo trọng số tăng dần, sau đó duyệt qua từng cạnh để thêm vào cây khung nếu cạnh đó không tạo thành "
        "chu trình với các cạnh đã chọn. Để kiểm tra chu trình tối ưu, ta dùng cấu trúc dữ liệu <b>Disjoint Set Union (DSU)</b>.",
        body_style
    ))
    
    krus_math = (
        "<b>Cơ sở Toán học (DSU & Path Compression):</b><br/>"
        "Mỗi đỉnh đại diện cho một tập hợp. Hàm find(x) trả về đại diện nhóm của x kết hợp nén đường đi:<br/>"
        "parent[x] = find(parent[x]) giúp độ sâu cây giảm còn xấp xỉ hằng số.<br/>"
        "Cạnh (u, v) được kết nạp khi và chỉ khi find(u) != find(v). Sau đó, thực hiện union(u, v) bằng cách đặt parent[find(u)] = find(v)."
    )
    story.append(make_callout_box(krus_math))
    
    code_krus = (
        "def kruskal(node_count, edges):\n"
        "    parent = list(range(node_count))\n"
        "    def find(x):\n"
        "        if parent[x] != x:\n"
        "            parent[x] = find(parent[x]) # Path compression (Nen duong di)\n"
        "        return parent[x]\n"
        "    def union(x, y):\n"
        "        root_x, root_y = find(x), find(y)\n"
        "        if root_x != root_y:\n"
        "            parent[root_x] = root_y # Union\n"
        "            return True\n"
        "        return False\n"
        "    sorted_edges = sorted(edges, key=lambda e: e[2])\n"
        "    mst = []\n"
        "    total_weight = 0\n"
        "    for u, v, w in sorted_edges:\n"
        "        if union(u, v):\n"
        "            mst.append((u, v, w))\n"
        "            total_weight += w\n"
        "            if len(mst) == node_count - 1:\n"
        "                break\n"
        "    return mst, total_weight"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Kruskal):", code_title_style))
    story.append(make_code_block(code_krus))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 8: KRUSKAL DETAILS & ALGORITHM 7: EDMONDS-KARP
    # ----------------------------------------------------
    krus_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 4-5:</i> Hàm <code>find</code> thực hiện đệ quy tìm gốc của phần tử, đồng thời gán trực tiếp cha của nút con về nút gốc đại diện (Path Compression), giảm chi phí truy vấn lần sau về O(α(V)) ≈ O(1).<br/>"
        "• <i>Dòng 13:</i> Sắp xếp toàn bộ danh sách cạnh theo trọng số tăng dần làm cơ sở cho tiếp cận tham lam.<br/>"
        "• <i>Dòng 20:</i> Dừng thuật toán sớm khi đã tìm đủ V - 1 cạnh, giúp tối ưu hiệu năng đối với đồ thị dày cạnh."
    )
    story.append(Paragraph(krus_explain, body_style))
    
    krus_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(E log E) phụ thuộc vào thời gian sắp xếp danh sách các cạnh.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V) để lưu trữ mảng parent quản lý các tập hợp liên thông của DSU."
    )
    story.append(make_callout_box(krus_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("7. Luồng cực đại trên mạng - Edmonds-Karp"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Thuật toán Edmonds-Karp tìm luồng cực đại bằng cách liên tục tìm đường tăng luồng ngắn nhất "
        "từ nguồn s tới đích t trên đồ thị dư bằng thuật toán duyệt BFS. Sau đó, nó nới lỏng luồng bằng giá trị bottleneck "
        "nhỏ nhất tìm được trên đường đi này và cập nhật lại dung lượng trên các cạnh xuôi và ngược của đồ thị dư.",
        body_style
    ))
    
    flow_math = (
        "<b>Cơ sở Toán học (Mạng dư & Đường tăng luồng):</b><br/>"
        "Mạng dư G_f chứa các cạnh có dung lượng dư r(u, v) = c(u, v) - f(u, v) &gt; 0.<br/>"
        "BFS tìm đường đi P từ s đến t có số cạnh ít nhất trên G_f. Bottleneck Δf = min{r(u, v) | (u, v) ∈ P}.<br/>"
        "Với mỗi cạnh (u, v) ∈ P: cập nhật f(u, v) = f(u, v) + Δf và f(v, u) = f(v, u) - Δf."
    )
    story.append(make_callout_box(flow_math))
    
    code_flow = (
        "from collections import deque\n\n"
        "def bfs_augmenting_path(graph, capacity, flow, s, t, parent):\n"
        "    visited = {s}\n"
        "    queue = deque([s])\n"
        "    while queue:\n"
        "        u = queue.popleft()\n"
        "        for v in graph[u]:\n"
        "            residual = capacity[(u, v)] - flow.get((u, v), 0)\n"
        "            if v not in visited and residual > 0:\n"
        "                visited.add(v)\n"
        "                parent[v] = u\n"
        "                if v == t: return True\n"
        "                queue.append(v)\n"
        "    return False\n\n"
        "def edmonds_karp(node_count, edges, s, t, is_directed=False):\n"
        "    graph = {i: set() for i in range(node_count)}\n"
        "    capacity = {}\n"
        "    for u, v, w in edges:\n"
        "        graph[u].add(v)\n"
        "        capacity[(u, v)] = capacity.get((u, v), 0) + w\n"
        "        if not is_directed:\n"
        "            graph[v].add(u)\n"
        "            capacity[(v, u)] = capacity.get((v, u), 0) + w\n"
        "    flow = {}\n"
        "    max_flow_val = 0\n"
        "    parent = {}\n"
        "    while bfs_augmenting_path(graph, capacity, flow, s, t, parent):\n"
        "        path_flow = float('inf')\n"
        "        curr = t\n"
        "        while curr != s:\n"
        "            p = parent[curr]\n"
        "            residual = capacity[(p, curr)] - flow.get((p, curr), 0)\n"
        "            path_flow = min(path_flow, residual)\n"
        "            curr = p\n"
        "        curr = t\n"
        "        while curr != s:\n"
        "            p = parent[curr]\n"
        "            flow[(p, curr)] = flow.get((p, curr), 0) + path_flow\n"
        "            flow[(curr, p)] = flow.get((curr, p), 0) - path_flow\n"
        "            curr = p\n"
        "        max_flow_val += path_flow\n"
        "        parent = {}\n"
        "    return max_flow_val, flow"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Edmonds-Karp):", code_title_style))
    story.append(make_code_block(code_flow))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 9: EDMONDS-KARP DETAILS & ALGORITHM 8: FLEURY
    # ----------------------------------------------------
    flow_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 3-14:</i> Hàm <code>bfs_augmenting_path</code> tìm đường tăng luồng ngắn nhất trên đồ thị dư. Chỉ duyệt qua các cạnh có <code>residual &gt; 0</code>.<br/>"
        "• <i>Dòng 31-36:</i> Duyệt ngược qua mảng <code>parent</code> từ t về s để tìm giá trị dung lượng dư nhỏ nhất (bottleneck) trên đường đi.<br/>"
        "• <i>Dòng 38-43:</i> Thực hiện cập nhật luồng: cộng luồng thực tế cho chiều đi và trừ luồng (luồng ảo) cho chiều ngược lại để cho phép giải thuật tự sửa sai ở các bước lặp sau."
    )
    story.append(Paragraph(flow_explain, body_style))
    
    flow_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(V E^2) thời gian. Việc sử dụng BFS đảm bảo số đường tăng luồng tối đa là O(VE), mỗi lần tìm mất O(E).<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V + E) để lưu trữ cấu trúc mạng và các bản đồ luồng/dung lượng cạnh."
    )
    story.append(make_callout_box(flow_comp))
    story.append(Spacer(1, 10))
    
    story.append(make_h2_heading("8. Chu trình Euler - Thuật toán Fleury"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Thuật toán Fleury xây dựng chu trình Euler bằng cách duyệt tham lam trên các cạnh. "
        "Từ đỉnh hiện tại, ta chọn một cạnh chưa đi qua để di chuyển sang đỉnh tiếp theo. Quy tắc cốt lõi là ta phải **tránh "
        "đi qua cạnh cầu** (bridge) của phần đồ thị chưa duyệt còn lại, trừ khi ta không còn sự lựa chọn nào khác.",
        body_style
    ))
    
    fleury_math = (
        "<b>Cơ sở Toán học (Khái niệm cạnh cầu):</b><br/>"
        "Cạnh e = (u, v) thuộc đồ thị liên thông G là cạnh cầu khi và chỉ khi xóa e làm tăng số thành phần liên thông của G.<br/>"
        "Fleury kiểm tra tính cầu bằng cách chạy DFS đếm số đỉnh có thể đi tới trước và sau khi xóa cạnh tạm thời.<br/>"
        "Nếu count_before &gt; count_after ⇒ e là cầu. Ta chỉ đi qua e khi bậc của u bằng 1."
    )
    story.append(make_callout_box(fleury_math))
    
    code_fleury = (
        "# Phuong thuc bo tro kiem tra canh cau cua Thanh vien 5\n"
        "def is_bridge(u, v, graph):\n"
        "    # Dem so dinh lien thong tu u tren do thi hien tai\n"
        "    count1 = dfs_count_reachable(u, graph)\n"
        "    \n"
        "    # Xoa canh (u, v) va kiem tra lai\n"
        "    remove_edge(u, v, graph)\n"
        "    count2 = dfs_count_reachable(u, graph)\n"
        "    \n"
        "    # Khoi phuc canh\n"
        "    add_edge(u, v, graph)\n"
        "    \n"
        "    # Neu so dinh reachable giam di, (u, v) la canh cau\n"
        "    return count1 > count2"
    )
    story.append(Paragraph("Mã nguồn thuật toán kiểm tra cầu (Fleury Helper):", code_title_style))
    story.append(make_code_block(code_fleury))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 10: ALGORITHM 9: HIERHOLZER & DETAILS
    # ----------------------------------------------------
    story.append(make_h2_heading("9. Chu trình Euler - Thuật toán Hierholzer"))
    story.append(Paragraph(
        "<b>Ý tưởng cốt lõi:</b> Hierholzer là một giải thuật cực kỳ hiệu quả để tìm chu trình/đường đi Euler bằng cách "
        "lồng ghép các chu trình con đơn giản. Xuất phát từ một đỉnh, ta đi tự do qua các cạnh chưa duyệt đến khi tạo thành "
        "một chu trình khép kín, đẩy các đỉnh đi qua vào Ngăn xếp (Stack). Nếu đỉnh ở đỉnh Stack vẫn còn cạnh chưa duyệt, "
        "ta tiếp tục đi để tìm chu trình con mới và lồng vào chu trình lớn bằng cách pop Stack.",
        body_style
    ))
    
    hier_math = (
        "<b>Cơ sở Toán học:</b><br/>"
        "Vì mỗi đỉnh trong chu trình Euler đều có bậc chẵn, nên khi ta đi tự do và xóa các cạnh đã đi qua, ta chắc chắn "
        "sẽ quay về đỉnh xuất phát ban đầu tạo thành chu trình khép kín. Các cạnh còn dư trên đồ thị sẽ tạo thành "
        "các chu trình con liên kết với chu trình chính. Thuật toán hoạt động trong thời gian tuyến tính O(E)."
    )
    story.append(make_callout_box(hier_math))
    
    code_hier = (
        "def hierholzer(graph, start):\n"
        "    # graph: Adjacency list bieu dien do thi\n"
        "    adj = {u: [v for v, w in graph[u]] for u in graph} # Copy danh sach canh\n"
        "    stack = [start]\n"
        "    circuit = []\n"
        "    while stack:\n"
        "        u = stack[-1]\n"
        "        if adj[u]:\n"
        "            v = adj[u].pop(0) # Lay va xoa canh khoi do thi\n"
        "            if u in adj[v]:\n"
        "                adj[v].remove(u) # Xoa chieu nguoc lai (doi voi do thi vo huong)\n"
        "            stack.append(v)\n"
        "        else:\n"
        "            # Neu dinh u khong con canh kề chua duyet, pop ra ghi nhan vao ket qua\n"
        "            circuit.append(stack.pop())\n"
        "    return circuit[::-1]"
    )
    story.append(Paragraph("Mã nguồn thuật toán thuần (Hierholzer):", code_title_style))
    story.append(make_code_block(code_hier))
    
    hier_explain = (
        "<b>Giải thích chi tiết mã nguồn:</b><br/>"
        "• <i>Dòng 3:</i> Sao chép cấu trúc cạnh ra biến cục bộ <code>adj</code> để thực hiện xóa dần cạnh khi đi qua.<br/>"
        "• <i>Dòng 9-11:</i> Xóa cạnh hai chiều đối với đồ thị vô hướng ngay lập tức để tránh duyệt lại cạnh đó.<br/>"
        "• <i>Dòng 14:</i> Khi đỉnh u hết cạnh kề khả dụng, ta thực hiện trích xuất đỉnh u khỏi Stack đưa vào mảng kết quả. "
        "Mảng kết quả đảo ngược chính là chu trình Euler khép kín cần tìm."
    )
    story.append(Paragraph(hier_explain, body_style))
    
    hier_comp = (
        "<b>Đánh giá Độ phức tạp:</b><br/>"
        "• <b>Thời gian (Time Complexity):</b> O(E) do duyệt qua mỗi cạnh đúng một lần để thêm/xóa.<br/>"
        "• <b>Không gian (Space Complexity):</b> O(V + E) để lưu trữ bản sao danh sách kề và ngăn xếp Stack."
    )
    story.append(make_callout_box(hier_comp))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 11: TASK ALLOCATION TABLE & CI WORKFLOW
    # ----------------------------------------------------
    story.append(Paragraph("III. BẢNG PHÂN CÔNG CÔNG VIỆC NHÓM 5 NGƯỜI", h1_style))
    story.append(Paragraph(
        "Bảng dưới đây thiết lập chi tiết phân công công việc cân bằng cho cả 5 thành viên. Mỗi người phụ trách một phân hệ "
        "chức năng bao gồm thiết kế thuật toán thuần, thuật toán hoạt họa generator và lập trình tích hợp hiển thị GUI.",
        body_style
    ))
    
    # Header row
    headers = [
        Paragraph("<b>Thành viên</b>", table_header_style),
        Paragraph("<b>Mô-đun phụ trách</b>", table_header_style),
        Paragraph("<b>Tệp tin mã nguồn</b>", table_header_style),
        Paragraph("<b>Đầu ra giao diện (GUI Output)</b>", table_header_style)
    ]
    
    table_data = [
        headers,
        [
            Paragraph("<b>Thành viên 1</b>", table_cell_bold_style),
            Paragraph("Quản lý biểu diễn đồ thị & Duyệt cơ bản", table_cell_style),
            Paragraph("• utils/conversions.py<br/>• algorithms/traversal.py<br/>• algorithms/pure/traversal.py", table_cell_style),
            Paragraph("Bảng biểu diễn ma trận/danh sách kề; hoạt họa tô màu đỉnh/cạnh duyệt BFS/DFS.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 2</b>", table_cell_bold_style),
            Paragraph("Đường đi ngắn nhất & Đồ thị hai phía", table_cell_style),
            Paragraph("• algorithms/dijkstra.py<br/>• algorithms/bipartite.py<br/>• algorithms/pure/...", table_cell_style),
            Paragraph("Vẽ đường đi ngắn nhất màu đỏ; tô màu 2 phân hoạch (Hồng/Xanh) hoặc highlight chu trình lẻ.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 3</b>", table_cell_bold_style),
            Paragraph("Cây khung nhỏ nhất (MST)", table_cell_style),
            Paragraph("• algorithms/prim.py<br/>• algorithms/kruskal.py<br/>• algorithms/pure/...", table_cell_style),
            Paragraph("Highlight cạnh MST đỏ đậm; hiển thị bảng sắp xếp cạnh (Kruskal) và thông số tổng trọng số.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 4</b>", table_cell_bold_style),
            Paragraph("Luồng cực đại trên mạng", table_cell_style),
            Paragraph("• algorithms/max_flow.py<br/>• algorithms/pure/max_flow.py<br/>• Hỗ trợ gui.py", table_cell_style),
            Paragraph("Vẽ nhãn dòng luồng flow/capacity trên cạnh; highlight đường tăng luồng; khung Canvas chính.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 5</b>", table_cell_bold_style),
            Paragraph("Đường đi & Chu trình Euler", table_cell_style),
            Paragraph("• algorithms/fleury.py<br/>• algorithms/hierholzer.py<br/>• algorithms/pure/...", table_cell_style),
            Paragraph("Chạy nét chu trình Euler động; hiển thị ngăn xếp Stack (Hierholzer) ở góc log.", table_cell_style)
        ]
    ]
    
    # Table initialization with column widths and styles (Zebra striping)
    t = Table(table_data, colWidths=[70, 110, 140, 165])
    t_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])
    
    # Apply Zebra striping starting from row index 1
    for row in range(1, len(table_data)):
        bg_color = colors.HexColor('#F7FAFC') if row % 2 == 1 else colors.white
        t_style.add('BACKGROUND', (0, row), (-1, row), bg_color)
        
    t.setStyle(t_style)
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("IV. QUY TRÌNH PHỐI HỢP, PIPELINE CI & TIÊU CHUẨN HOÀN THÀNH", h1_style))
    story.append(make_h2_heading("1. Quy trình chuyển đổi từ mã nguồn thuần sang Hoạt họa Generator"))
    story.append(Paragraph(
        "Để giao diện không bị treo khi thực thi thuật toán lâu, hệ thống không sử dụng vòng lặp vô hạn hay hàm trì hoãn "
        "đồng bộ (<code>time.sleep</code>). Thay vào đó, mỗi thuật toán thuần được chuyển đổi sang dạng <b>Generator</b> "
        "bằng cách thay các điểm chốt trạng thái bằng từ khóa <code>yield</code>.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 12: CI WORKFLOW DETAILS & DOD
    # ----------------------------------------------------
    code_yield = (
        "# Vi du cach chuyen doi sang Generator trong algorithms/dijkstra.py\n"
        "def dijkstra_generator(graph, start):\n"
        "    dist = {node: float('inf') for node in graph}\n"
        "    dist[start] = 0\n"
        "    pq = [(0, start)]\n"
        "    yield \"START\", {\"dist\": dist.copy(), \"curr\": start}\n"
        "    \n"
        "    while pq:\n"
        "        d, u = heapq.heappop(pq)\n"
        "        yield \"EXAMINE_NODE\", {\"node\": u, \"dist\": dist.copy()}\n"
        "        ...\n"
        "        # Sau moi lan noi long canh v thanh cong:\n"
        "        yield \"RELAX_EDGE\", {\"edge\": (u, v), \"dist\": dist.copy()}\n"
        "    yield \"FINISHED\", {\"dist\": dist, \"prev\": prev}"
    )
    story.append(Paragraph("Minh họa mẫu chuyển đổi sang Generator:", code_title_style))
    story.append(make_code_block(code_yield))
    
    story.append(make_h2_heading("2. Cơ chế tích hợp hoạt họa với vòng lặp bất đồng bộ của tkinter (after)"))
    story.append(Paragraph(
        "Giao diện Tkinter chạy đơn luồng. Để thực hiện vẽ hoạt họa từng bước, GUI sẽ khởi tạo Generator của thuật toán "
        "và đăng ký một hàm lặp lại sau mỗi khoảng thời gian <code>delay</code> thông qua hàm <code>tkinter.after</code>:",
        body_style
    ))
    
    code_after = (
        "# Tich hop trong gui.py\n"
        "def run_animation_step(self):\n"
        "    try:\n"
        "        # Lay trang thai tiep theo tu generator\n"
        "        step_type, data = next(self.current_generator)\n"
        "        self.redraw_graph_canvas(step_type, data)\n"
        "        self.update_log_panel(step_type, data)\n"
        "        \n"
        "        if step_type != \"FINISHED\":\n"
        "            # Dang ky goi lai chinh no sau self.delay miliseconds\n"
        "            self.anim_job = self.root.after(self.delay, self.run_animation_step)\n"
        "    except StopIteration:\n"
        "        self.log(\"Thuat toan ket thuc.\")"
    )
    story.append(make_code_block(code_after))
    
    story.append(make_h2_heading("3. Tiêu chuẩn hoàn thành (Definition of Done - DoD)"))
    story.append(Paragraph(
        "Một phần việc được coi là hoàn thành 100% khi đáp ứng đầy đủ các tiêu chuẩn học thuật và lập trình sau:<br/>"
        "• <b>Tính nhất quán lý thuyết (Deterministic):</b> BFS/DFS và các lựa chọn đỉnh lân cận bắt buộc phải thực hiện sắp xếp nhãn tăng dần trước khi đưa vào hàng đợi/ngăn xếp. Kết quả chạy trên máy phải trùng khớp tuyệt đối với việc làm bài tập bằng tay.<br/>"
        "• <b>Bẫy ngoại lệ và Tính toàn vẹn:</b> Đồ thị có hướng/vô hướng được kiểm tra tính hợp lệ trước khi bấm chạy thuật toán (Ví dụ: Kruskal chỉ chạy trên vô hướng, Edmonds-Karp yêu cầu chọn rõ đỉnh nguồn và đỉnh đích).<br/>"
        "• <b>Clean Code & Tài liệu:</b> Đặt tên biến rõ ràng theo tiếng Anh học thuật. Có docstring mô tả chi tiết đầu vào và đầu ra. Tất cả code gộp vào main phải được kiểm thử chéo và không gây lỗi xung đột mã nguồn.",
        body_style
    ))
    
    doc.build(story)
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    make_comprehensive_pdf()
