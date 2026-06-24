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
        leading_spaces = len(line) - len(line.lstrip(' '))
        # Convert leading spaces to HTML non-breaking spaces
        line_formatted = '&nbsp;' * leading_spaces + line.lstrip(' ')
        lines.append(line_formatted)
    return "<br/>".join(lines)

def make_academic_pdf():
    pdf_filename = "Bao_cao_Trien_khai_Chi_tiet_CTRR.pdf"
    
    # Page setup - Margins: 40pt
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    # Font Registration (Standard Windows Fonts)
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
        FONT_NAME_ITALIC = 'Arial-Italic'
        FONT_MONO = 'CourierNew'
    except Exception as e:
        print("Falling back to standard fonts:", e)
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
        FONT_NAME_ITALIC = 'Helvetica-Oblique'
        FONT_MONO = 'Courier'
        
    styles = getSampleStyleSheet()
    
    # Style Definitions
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=18,
        leading=24,
        textColor=colors.HexColor('#1d3557'),
        alignment=1,
        spaceAfter=15
    )
    
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
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1d3557'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#457b9d'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor('#2b2d42'),
        spaceAfter=8
    )
    
    body_bold_style = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName=FONT_NAME_BOLD
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
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

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName=FONT_MONO,
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1d3557'),
        backColor=colors.HexColor('#f8f9fa'),
        borderColor=colors.HexColor('#a8dadc'),
        borderWidth=0.5,
        borderPadding=8,
        spaceAfter=12
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2b2d42')
    )
    
    table_cell_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName=FONT_NAME_BOLD,
        textColor=colors.HexColor('#1d3557')
    )
    
    story = []
    
    # ----------------------------------------------------
    # PAGE 1: COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("BÁO CÁO PHÂN TÍCH TOÁN HỌC, PHÂN CHIA CÔNG VIỆC<br/>VÀ HƯỚNG DẪN TRIỂN KHAI CHI TIẾT", title_style))
    story.append(Paragraph("Dự án: Hệ thống trực quan hóa cấu trúc rời rạc & giải thuật đồ thị", subtitle_style))
    story.append(Spacer(1, 20))
    
    intro_text = (
        "<b>TÓM TẮT DỰ ÁN (ABSTRACT):</b><br/>"
        "Tài liệu này đóng vai trò là hướng dẫn kỹ thuật và kế hoạch phân công công việc chi tiết dành cho nhóm phát triển "
        "gồm 5 thành viên để xây dựng ứng dụng trực quan hóa 9 thuật toán đồ thị cơ bản và nâng cao của môn học Cấu trúc rời rạc. "
        "Điểm đặc biệt của dự án này là sự phân chia công bằng, trong đó cả 5 thành viên đều trực tiếp lập trình cả phần thuật toán "
        "thuần (Backend), thuật toán hoạt họa (Generator) và lập trình điều khiển giao diện (GUI) liên quan đến phần việc của mình. "
        "Tài liệu bao gồm cơ sở toán học chi tiết (dưới dạng các ký hiệu toán học Unicode chuẩn hóa để hiển thị trực quan), "
        "mã nguồn khung định hướng (Skeleton Code) cho từng vai trò, tiến độ thực hiện và các tiêu chuẩn chất lượng để đảm bảo "
        "mã nguồn đồng nhất, sạch sẽ."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 20))
    
    toc_text = (
        "<b>MỤC LỤC TÀI LIỆU:</b><br/>"
        "I. Tổng quan kiến trúc hệ thống (Trang 2)<br/>"
        "II. Phân tích toán học & Giải thuật chi tiết (Trang 2-4)<br/>"
        "III. Bảng phân chia công việc nhóm (Trang 5)<br/>"
        "IV. Chi tiết phần việc và Skeleton Code cho từng thành viên (Trang 5-9)<br/>"
        "V. Quy trình phối hợp và thứ tự triển khai (Trang 10)<br/>"
        "VI. Tiêu chuẩn hoàn thành và Clean Code (Trang 10)"
    )
    story.append(Paragraph(toc_text, body_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: SYSTEM OVERVIEW & MATH ANALYSIS (PART 1)
    # ----------------------------------------------------
    story.append(Paragraph("I. TỔNG QUAN KIẾN TRÚC HỆ THỐNG", h1_style))
    story.append(Paragraph(
        "Hệ thống áp dụng mô hình phân tách mối quan tâm (Separation of Concerns) nhằm đảm bảo code thuật toán độc lập hoàn toàn "
        "với phần giao diện hiển thị, tạo điều kiện thuận lợi cho việc tái sử dụng mã nguồn:<br/>"
        "• <b>Lớp Dữ liệu (Utils):</b> Thực hiện chuyển đổi qua lại giữa các dạng biểu diễn đồ thị (Adjacency Matrix, Adjacency List, Edge List) cho cả đồ thị có hướng và vô hướng.<br/>"
        "• <b>Lớp Thuật toán (Backend):</b> Bao gồm 2 phiên bản độc lập. Phiên bản thuần (nằm trong thư mục <code>algorithms/pure/</code>) nhận đầu vào và trả về kết quả cuối cùng theo cách tuyến tính. Phiên bản hoạt họa (nằm trong <code>algorithms/</code>) được triển khai bằng Generator (từ khóa <code>yield</code>) để trả về từng bước chạy cho giao diện hiển thị.<br/>"
        "• <b>Lớp Giao diện (GUI):</b> Viết bằng <code>tkinter</code>, nhận sự kiện từ chuột (vẽ đỉnh, vẽ cạnh) và gọi vòng lặp thời gian để liên tục lấy trạng thái từ generator để cập nhật giao diện canvas.",
        body_style
    ))
    
    story.append(Paragraph("II. PHÂN TÍCH TOÁN HỌC & GIẢI THUẬT CHI TIẾT", h1_style))
    
    story.append(Paragraph("2.1. Duyệt đồ thị (BFS & DFS)", h2_style))
    story.append(Paragraph(
        "Duyệt đồ thị là quá trình đi qua tất cả các đỉnh của đồ thị một cách hệ thống:<br/>"
        "• <b>BFS (Breadth-First Search - Duyệt rộng):</b> Sử dụng cấu trúc dữ liệu Hàng đợi <b>Queue (FIFO)</b>. Xuất phát từ đỉnh nguồn s, loang đều ra xung quanh để duyệt các đỉnh có khoảng cách k trước khi chuyển sang khoảng cách k+1. Thích hợp để tìm đường đi ngắn nhất trên đồ thị không trọng số. Độ phức tạp: O(V + E) thời gian, O(V) không gian.<br/>"
        "• <b>DFS (Depth-First Search - Duyệt sâu):</b> Sử dụng cấu trúc dữ liệu Ngăn xếp <b>Stack (LIFO)</b> (hoặc đệ quy hệ thống). Thuật toán đi sâu tối đa theo từng nhánh cho tới khi không đi được nữa thì thực hiện quay lui (Backtracking). Độ phức tạp: O(V + E) thời gian, O(V) không gian.",
        body_style
    ))
    
    story.append(Paragraph("2.2. Kiểm tra đồ thị hai phía (Bipartite Graph Check)", h2_style))
    story.append(Paragraph(
        "<b>Định nghĩa toán học:</b> Một đồ thị vô hướng G = (V, E) là đồ thị hai phía nếu tồn tại phân hoạch V = V1 ∪ V2 với V1 ∩ V2 = ∅ sao cho mọi cạnh (u, v) ∈ E đều kết nối một đỉnh thuộc V1 với một đỉnh thuộc V2.<br/>"
        "<b>Giải thuật:</b> Sử dụng thuật toán tô màu đồ thị bằng 2 màu (0 và 1). Khởi tạo tất cả đỉnh chưa có màu. Chọn một đỉnh tô màu 0. Sử dụng DFS hoặc BFS loang ra các đỉnh kề: nếu đỉnh kề chưa tô màu, tô màu ngược lại (tô màu 1 - color[u]); nếu đỉnh kề đã tô màu và trùng màu với đỉnh đang xét, kết luận đồ thị chứa chu trình lẻ (không là đồ thị hai phía) và truy vết ngược qua mảng cha <code>parent</code> để xuất chu trình lẻ làm minh chứng.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 3: MATH ANALYSIS (PART 2)
    # ----------------------------------------------------
    story.append(Paragraph("2.3. Tìm đường đi ngắn nhất (Dijkstra)", h2_style))
    story.append(Paragraph(
        "<b>Định nghĩa bài toán:</b> Cho đồ thị có trọng số không âm G = (V, E, w) với w(u, v) ≥ 0, tìm đường đi ngắn nhất từ đỉnh nguồn S tới tất cả các đỉnh khác.<br/>"
        "<b>Thuật toán:</b> Giải thuật tham lam (Greedy). Duy trì mảng khoảng cách tạm thời d[v] từ S. Ở mỗi bước lặp, chọn đỉnh u chưa cố định có khoảng cách d[u] nhỏ nhất, cố định khoảng cách này. Thực hiện nới lỏng (Relaxation) cho tất cả các đỉnh kề v chưa cố định của u: nếu d[u] + w(u, v) &lt; d[v], cập nhật d[v] = d[u] + w(u, v) và ghi nhận prev[v] = u.<br/>"
        "Công thức nới lỏng: d[v] = min(d[v], d[u] + w(u, v))<br/>"
        "<b>Độ phức tạp:</b> Sử dụng Hàng đợi ưu tiên (Binary Min-Heap) giúp thuật toán đạt hiệu năng O(E log V) thời gian và O(V) không gian.",
        body_style
    ))
    
    story.append(Paragraph("2.4. Cây khung nhỏ nhất MST (Kruskal & Prim)", h2_style))
    story.append(Paragraph(
        "<b>Định nghĩa bài toán:</b> Cho đồ thị vô hướng liên thông có trọng số G = (V, E, w). Tìm cây con chứa tất cả đỉnh của đồ thị có đúng V - 1 cạnh sao cho tổng trọng số các cạnh là nhỏ nhất.<br/>"
        "• <b>Thuật toán Kruskal (Duyệt theo cạnh):</b> Sắp xếp danh sách cạnh theo trọng số tăng dần. Duyệt qua từng cạnh: nếu hai đỉnh của cạnh nằm ở hai thành phần liên thông khác nhau, kết nạp cạnh đó vào MST. Sử dụng cấu trúc dữ liệu <b>Disjoint Set Union (DSU)</b> với kỹ thuật nén đường đi (Path Compression) để kiểm tra chu trình và hợp nhất tập hợp với độ phức tạp gần như O(1). Tổng độ phức tạp: O(E log E) thời gian (do chi phí sắp xếp cạnh).<br/>"
        "• <b>Thuật toán Prim (Duyệt theo đỉnh):</b> Bắt đầu từ một đỉnh gốc, xây dựng cây khung bằng cách liên tục kết nạp cạnh có trọng số nhỏ nhất nối từ một đỉnh đã nằm trong cây ra một đỉnh chưa nằm trong cây. Sử dụng Min-Heap để quản lý các cạnh ứng viên. Tổng độ phức tạp: O(E log V) thời gian.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 4: MATH ANALYSIS (PART 3)
    # ----------------------------------------------------
    story.append(Paragraph("2.5. Luồng cực đại (Ford-Fulkerson / Edmonds-Karp)", h2_style))
    story.append(Paragraph(
        "<b>Bài toán mạng luồng:</b> Cho mạng luồng G = (V, E) với dung lượng cạnh c(u, v) ≥ 0, đỉnh nguồn s, và đỉnh đích t. Tìm luồng có giá trị lớn nhất từ s đến t thỏa mãn ràng buộc dung lượng (0 ≤ f(u, v) ≤ c(u, v)) và bảo toàn luồng tại các đỉnh trung gian.<br/>"
        "<b>Thuật toán Edmonds-Karp:</b> Là một cải tiến của Ford-Fulkerson. Thuật toán liên tục tìm đường tăng luồng ngắn nhất (ít cạnh nhất) bằng cách duyệt **BFS** trên đồ thị dư G_f. Tìm dung lượng dư nhỏ nhất trên đường đi này (Δf = bottleneck). Tăng luồng thực tế dọc theo đường tăng luồng thêm Δf (tăng luồng cạnh xuôi, giảm luồng cạnh ngược trên đồ thị dư). Thuật toán dừng lại khi không còn đường đi từ s đến t trên đồ thị dư.<br/>"
        "<b>Độ phức tạp:</b> Đảm bảo số lần lặp tối đa và kết thúc trong O(V E^2) thời gian.",
        body_style
    ))
    
    story.append(Paragraph("2.6. Chu trình & Đường đi Euler (Fleury & Hierholzer)", h2_style))
    story.append(Paragraph(
        "<b>Định lý tồn tại Euler:</b> Đồ thị vô hướng liên thông có chu trình Euler khi tất cả các đỉnh đều có bậc chẵn; có đường đi Euler khi có đúng 0 hoặc 2 đỉnh bậc lẻ.<br/>"
        "• <b>Thuật toán Fleury:</b> Đi tham lam từ đỉnh xuất phát. Ở mỗi bước chọn cạnh đi tiếp chưa viếng thăm sao cho tránh đi qua cạnh cầu (bridge) của đồ thị con còn lại, trừ khi không còn lựa chọn nào khác. Độ phức tạp thời gian: O(E^2) do mỗi bước phải kiểm tra cầu bằng cách duyệt đồ thị phụ.<br/>"
        "• <b>Thuật toán Hierholzer:</b> Khởi hành từ đỉnh gốc, di chuyển tự do qua các cạnh chưa duyệt cho đến khi quay về đỉnh xuất phát tạo thành một chu trình đơn, xóa các cạnh đã duyệt này khỏi đồ thị và đẩy lộ trình vào một Ngăn xếp (Stack). Nếu trên đường đi có các đỉnh vẫn còn cạnh chưa duyệt, ta tìm một chu trình con từ đỉnh đó và lồng ghép ngược lại vào đường đi ban đầu thông qua thao tác pop Stack. Độ phức tạp thời gian cực kỳ tối ưu: O(E) vì mỗi cạnh chỉ bị duyệt đúng một lần.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 5: TASK ALLOCATION & MEMBER 1 SKELETON
    # ----------------------------------------------------
    story.append(Paragraph("III. BẢNG PHÂN CHIA CÔNG VIỆC NHÓM 5 NGƯỜI", h1_style))
    
    # Task assignment table
    headers = [
        Paragraph("<b>Thành viên</b>", table_cell_bold_style),
        Paragraph("<b>Nhóm Thuật toán phụ trách</b>", table_cell_bold_style),
        Paragraph("<b>Chi tiết phần việc (Thuật toán + GUI)</b>", table_cell_bold_style)
    ]
    
    table_data = [
        headers,
        [
            Paragraph("<b>Thành viên 1</b>", table_cell_bold_style),
            Paragraph("Duyệt đồ thị &<br/>Biểu diễn đồ thị", table_cell_style),
            Paragraph("• Viết chuyển đổi biểu diễn đồ thị (Ma trận kề, ds kề, ds cạnh cho cả đồ thị vô hướng & có hướng) ở <code>utils/conversions.py</code>.<br/>• Cài đặt thuật toán duyệt <b>BFS & DFS</b> thuần và generator.<br/>• Tích hợp hiển thị biểu diễn đồ thị và hoạt họa BFS/DFS lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 2</b>", table_cell_bold_style),
            Paragraph("Đường đi ngắn nhất &<br/>Đồ thị hai phía", table_cell_style),
            Paragraph("• Cài đặt giải thuật <b>Dijkstra</b> sử dụng Priority Queue (Min-Heap), kiểm soát trọng số âm.<br/>• Cài đặt thuật toán kiểm tra <b>Đồ thị 2 phía</b> (tô màu BFS/DFS), truy vết chu trình lẻ gây xung đột.<br/>• Tích hợp highlight lộ trình Dijkstra và tô màu hai phân hoạch lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 3</b>", table_cell_bold_style),
            Paragraph("Cây khung nhỏ nhất<br/>(MST)", table_cell_style),
            Paragraph("• Cài đặt thuật toán **Prim** (dùng Heap).<br/>• Cài đặt thuật toán **Kruskal** sắp xếp cạnh kết hợp cấu trúc dữ liệu **DSU** (Disjoint Set Union) để kiểm tra chu trình và hợp nhất nhanh.<br/>• Tích hợp trực quan hóa cây khung MST lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 4</b>", table_cell_bold_style),
            Paragraph("Luồng cực đại<br/>(Max Flow)", table_cell_style),
            Paragraph("• Cài đặt thuật toán luồng cực đại **Ford-Fulkerson (Edmonds-Karp)** dùng BFS tìm đường tăng luồng ngắn nhất trên đồ thị dư.<br/>• Tích hợp hiển thị dòng luồng <code>flow/capacity</code> trên các cạnh và highlight các đường tăng luồng qua từng bước.<br/>• Phụ giúp Thành viên 1 thiết kế khung Canvas chính.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 5</b>", table_cell_bold_style),
            Paragraph("Đường đi &<br/>Chu trình Euler", table_cell_style),
            Paragraph("• Cài đặt giải thuật **Fleury** (duyệt kiểm tra và tránh các cạnh cầu - bridge).<br/>• Cài đặt giải thuật **Hierholzer** tối ưu O(E) sử dụng cơ chế lưu trữ Stack.<br/>• Tích hợp mô phỏng bước đi của Fleury và cơ chế push/pop đỉnh vào Stack của Hierholzer lên GUI.", table_cell_style)
        ]
    ]
    
    t = Table(table_data, colWidths=[75, 120, 315])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2eafc')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("IV. CHI TIẾT CODE PHẢI TRIỂN KHAI CHO TỪNG THÀNH VIÊN", h1_style))
    story.append(Paragraph("4.1. Thành viên 1: Mô-đun Conversions và BFS/DFS", h2_style))
    
    code_m1 = (
        "# Tep tin: utils/conversions.py\n"
        "def to_adjacency_matrix(nodes, edges, is_directed=False):\n"
        "    n = len(nodes)\n"
        "    matrix = [[0] * n for _ in range(n)]\n"
        "    for u, v, w in edges:\n"
        "        matrix[u][v] = w\n"
        "        if not is_directed:\n"
        "            matrix[v][u] = w\n"
        "    return matrix\n\n"
        "# Tep tin: algorithms/pure/traversal.py\n"
        "from collections import deque\n"
        "def bfs(graph, start):\n"
        "    visited, visited_set = [], {start}\n"
        "    queue = deque([start])\n"
        "    edges = []\n"
        "    while queue:\n"
        "        u = queue.popleft()\n"
        "        visited.append(u)\n"
        "        for v, w in sorted(graph.get(u, []), key=lambda x: x[0]):\n"
        "            if v not in visited_set:\n"
        "                visited_set.add(v)\n"
        "                queue.append(v)\n"
        "                edges.append((u, v, w))\n"
        "    return visited, edges"
    )
    story.append(Paragraph("Mã khung lập trình (Skeleton Code):", code_title_style))
    story.append(Paragraph(format_code_to_html(code_m1), code_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 6: MEMBER 2 SKELETON
    # ----------------------------------------------------
    story.append(Paragraph("4.2. Thành viên 2: Thuật toán Dijkstra và Đồ thị hai phía", h2_style))
    
    code_m2 = (
        "# Tep tin: algorithms/pure/dijkstra.py\n"
        "import heapq\n"
        "def dijkstra(graph, start):\n"
        "    dist = {node: float('inf') for node in graph}\n"
        "    prev = {node: None for node in graph}\n"
        "    dist[start] = 0\n"
        "    pq = [(0, start)]\n"
        "    while pq:\n"
        "        current_dist, u = heapq.heappop(pq)\n"
        "        if current_dist > dist[u]: continue\n"
        "        for v, weight in graph.get(u, []):\n"
        "            if weight < 0: raise ValueError(\"Trong so am khong ho tro!\")\n"
        "            if current_dist + weight < dist[v]:\n"
        "                dist[v] = current_dist + weight\n"
        "                prev[v] = u\n"
        "                heapq.heappush(pq, (dist[v], v))\n"
        "    return dist, prev\n\n"
        "# Tep tin: algorithms/pure/bipartite.py\n"
        "def check_bipartite(graph):\n"
        "    color = {} # Luu dinh va mau cua no (0 hoac 1)\n"
        "    parent = {}\n"
        "    for start_node in graph:\n"
        "        if start_node not in color:\n"
        "            stack = [(start_node, 0)]\n"
        "            color[start_node] = 0\n"
        "            while stack:\n"
        "                u, c = stack[-1]\n"
        "                unvisited_found = False\n"
        "                for v, _ in graph[u]:\n"
        "                    if v not in color:\n"
        "                        color[v] = 1 - c\n"
        "                        parent[v] = u\n"
        "                        stack.append((v, 1 - c))\n"
        "                        unvisited_found = True; break\n"
        "                    elif color[v] == color[u]:\n"
        "                        # Phat hien chu trinh le\n"
        "                        cycle = [v, u]\n"
        "                        curr = u\n"
        "                        while curr in parent and curr != v:\n"
        "                            curr = parent[curr]\n"
        "                            cycle.append(curr)\n"
        "                        return False, cycle[::-1]\n"
        "                if not unvisited_found: stack.pop()\n"
        "    return True, color"
    )
    story.append(Paragraph("Mã khung lập trình (Skeleton Code):", code_title_style))
    story.append(Paragraph(format_code_to_html(code_m2), code_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 7: MEMBER 3 SKELETON
    # ----------------------------------------------------
    story.append(Paragraph("4.3. Thành viên 3: Cây khung nhỏ nhất MST (Prim và Kruskal)", h2_style))
    
    code_m3 = (
        "# Tep tin: algorithms/pure/kruskal.py\n"
        "def kruskal(node_count, edges):\n"
        "    parent = list(range(node_count))\n"
        "    def find(x):\n"
        "        if parent[x] != x:\n"
        "            parent[x] = find(parent[x]) # Path compression\n"
        "        return parent[x]\n"
        "    def union(x, y):\n"
        "        root_x, root_y = find(x), find(y)\n"
        "        if root_x != root_y:\n"
        "            parent[root_x] = root_y\n"
        "            return True\n"
        "        return False\n"
        "    sorted_edges = sorted(edges, key=lambda e: e[2])\n"
        "    mst = []\n"
        "    total = 0\n"
        "    for u, v, w in sorted_edges:\n"
        "        if union(u, v):\n"
        "            mst.append((u, v, w))\n"
        "            total += w\n"
        "            if len(mst) == node_count - 1:\n"
        "                break\n"
        "    return mst, total\n\n"
        "# Tep tin: algorithms/pure/prim.py\n"
        "import heapq\n"
        "def prim(node_count, graph, start=0):\n"
        "    visited = {start}\n"
        "    mst = []\n"
        "    total = 0\n"
        "    pq = []\n"
        "    for v, w in graph.get(start, []):\n"
        "        heapq.heappush(pq, (w, start, v))\n"
        "    while pq and len(visited) < node_count:\n"
        "        w, u, v = heapq.heappop(pq)\n"
        "        if v not in visited:\n"
        "            visited.add(v)\n"
        "            mst.append((u, v, w))\n"
        "            total += w\n"
        "            for next_v, next_w in graph.get(v, []):\n"
        "                if next_v not in visited:\n"
        "                    heapq.heappush(pq, (next_w, v, next_v))\n"
        "    return mst, total"
    )
    story.append(Paragraph("Mã khung lập trình (Skeleton Code):", code_title_style))
    story.append(Paragraph(format_code_to_html(code_m3), code_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 8: MEMBER 4 SKELETON
    # ----------------------------------------------------
    story.append(Paragraph("4.4. Thành viên 4: Luồng cực đại Ford-Fulkerson (Edmonds-Karp)", h2_style))
    
    code_m4 = (
        "# Tep tin: algorithms/pure/max_flow.py\n"
        "from collections import deque\n"
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
    story.append(Paragraph("Mã khung lập trình (Skeleton Code):", code_title_style))
    story.append(Paragraph(format_code_to_html(code_m4), code_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 9: MEMBER 5 SKELETON
    # ----------------------------------------------------
    story.append(Paragraph("4.5. Thành viên 5: Đường đi & Chu trình Euler (Fleury và Hierholzer)", h2_style))
    
    code_m5 = (
        "# Tep tin: algorithms/pure/hierholzer.py\n"
        "def find_eulerian_path_or_circuit_hierholzer(graph):\n"
        "    adj = {u: {} for u in graph}\n"
        "    for u in graph:\n"
        "        for v, w in graph[u]:\n"
        "            adj[u][v] = adj[u].get(v, 0) + 1\n"
        "    # Tim dinh bac le de chon diem bat dau (neu la duong di Euler)\n"
        "    start_node = next(iter(graph))\n"
        "    degrees = {u: sum(adj[u].values()) for u in graph}\n"
        "    odd_nodes = [u for u in degrees if degrees[u] % 2 != 0]\n"
        "    if len(odd_nodes) == 2:\n"
        "        start_node = odd_nodes[0]\n"
        "    stack = [start_node]\n"
        "    path = []\n"
        "    while stack:\n"
        "        u = stack[-1]\n"
        "        neighbors = [v for v in adj[u] if adj[u][v] > 0]\n"
        "        if neighbors:\n"
        "            v = neighbors[0]\n"
        "            adj[u][v] -= 1\n"
        "            adj[v][u] -= 1\n"
        "            stack.append(v)\n"
        "        else:\n"
        "            path.append(stack.pop())\n"
        "    return path[::-1]\n\n"
        "# Tep tin: algorithms/pure/fleury.py\n"
        "# (De viet Fleury, Thanh vien 5 can dinh nghia them ham kiem tra canh cau - bridge)\n"
        "def is_bridge(u, v, graph):\n"
        "    # Kiem tra xem viec xoa canh (u, v) co lam mat tinh lien thong hay khong\n"
        "    # Bang cach chay dem so thanh phan lien thong bang DFS/BFS\n"
        "    pass"
    )
    story.append(Paragraph("Mã khung lập trình (Skeleton Code):", code_title_style))
    story.append(Paragraph(format_code_to_html(code_m5), code_style))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 10: WORKFLOW & DOD
    # ----------------------------------------------------
    story.append(Paragraph("V. QUY TRÌNH PHỐI HỢP & TIẾN ĐỘ THỰC HIỆN", h1_style))
    story.append(Paragraph(
        "Nhóm tuân thủ mô hình phát triển tích hợp liên tục (CI) theo 4 bước sau:<br/>"
        "1. <b>Viết giải thuật thuần trước:</b> Viết toàn bộ code trong thư mục <code>pure/</code> và chạy kiểm thử CLI. Đảm bảo thuật toán độc lập hoàn toàn với Tkinter.<br/>"
        "2. <b>Chuyển sang generator:</b> Copy thuật toán ra thư mục ngoài, chèn các từ khóa <code>yield</code> sau mỗi chu trình lặp chính để gửi thông tin về GUI.<br/>"
        "3. <b>Liên kết giao diện:</b> Tự viết hàm vẽ kết quả trung gian nhận được từ Generator của mình lên Canvas chính của chương trình trong file <code>gui.py</code>.<br/>"
        "4. <b>Tạo đồ thị mẫu và test chéo:</b> Tự thiết kế ít nhất 1 đồ thị mẫu đặc trưng cho thuật toán của mình dưới dạng JSON để người dùng dễ kiểm thử nhanh.",
        body_style
    ))
    
    story.append(Paragraph("VI. TIÊU CHUẨN HOÀN THÀNH & CLEAN CODE (DoD)", h1_style))
    story.append(Paragraph(
        "Một phần việc được coi là hoàn thành 100% khi đáp ứng đầy đủ các tiêu chuẩn học thuật và lập trình sau:<br/>"
        "• <b>Chính xác tuyệt đối (Deterministic):</b> Các thuật toán duyệt hoặc chọn cạnh kề phải luôn thực hiện sắp xếp danh sách đỉnh kề theo nhãn tăng dần trước khi duyệt để khớp với kết quả giải tay lý thuyết.<br/>"
        "• <b>Mượt mà và Không đơ ứng dụng:</b> Hoạt họa chạy trên GUI phải sử dụng luồng generator tuần tự kết hợp hàm <code>after()</code> của Tkinter, tuyệt đối không được dùng vòng lặp vô hạn hay hàm <code>time.sleep()</code> trong luồng chính.<br/>"
        "• <b>Chuần hóa Clean Code:</b> Đặt tên biến và hàm theo chuẩn PEP 8 (tiếng Anh rõ ràng). Bắt buộc phải viết docstring mô tả chi tiết kiểu dữ liệu đầu vào và đầu ra cho tất cả các hàm.<br/>"
        "• <b>Quản lý qua Git:</b> Từng thành viên commit code lên nhánh riêng (ví dụ: <code>feature/prim-kruskal</code>), test chạy thử không có lỗi mới được gửi Pull Request gộp vào nhánh chính <code>main</code>.",
        body_style
    ))
    
    doc.build(story)
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    make_academic_pdf()
