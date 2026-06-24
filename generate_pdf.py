import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Circle, Line, String, Rect

def draw_graph(width, height, positions, edges, is_directed=False, highlight_edges=None, highlight_nodes=None, edge_labels=None, only_active_elements=False):
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#f8f9fa'), strokeColor=colors.HexColor('#e5e5e5'), strokeWidth=1))
    
    # Filter edges if only active elements are requested
    active_edges = []
    for u, v in edges:
        is_hl = False
        if highlight_edges:
            if (u, v) in highlight_edges or (not is_directed and (v, u) in highlight_edges):
                is_hl = True
        if not only_active_elements or is_hl:
            active_edges.append((u, v))
            
    for u, v in active_edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        
        is_highlight = False
        if highlight_edges:
            if (u, v) in highlight_edges or (not is_directed and (v, u) in highlight_edges):
                is_highlight = True
                
        color = colors.HexColor('#e63946') if is_highlight else colors.HexColor('#6c757d')
        stroke_w = 2.5 if is_highlight else 1.2
        
        if is_directed:
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                tx = x2 - (dx / dist) * 12
                ty = y2 - (dy / dist) * 12
                d.add(Line(x1, y1, tx, ty, strokeColor=color, strokeWidth=stroke_w))
                
                angle = math.atan2(dy, dx)
                angle1 = angle + math.pi - 0.4
                angle2 = angle + math.pi + 0.4
                ax1 = tx + 6 * math.cos(angle1)
                ay1 = ty + 6 * math.sin(angle1)
                ax2 = tx + 6 * math.cos(angle2)
                ay2 = ty + 6 * math.sin(angle2)
                
                d.add(Line(tx, ty, ax1, ay1, strokeColor=color, strokeWidth=stroke_w))
                d.add(Line(tx, ty, ax2, ay2, strokeColor=color, strokeWidth=stroke_w))
        else:
            d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=stroke_w))
            
        if edge_labels:
            label = None
            if (u, v) in edge_labels:
                label = edge_labels[(u, v)]
            elif not is_directed and (v, u) in edge_labels:
                label = edge_labels[(v, u)]
                
            if label is not None:
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2 + 4
                d.add(String(mx, my, str(label), fontName='Arial-Bold', fontSize=8, fillColor=colors.HexColor('#1d3557'), textAnchor='middle'))
                
    for i, (x, y) in enumerate(positions):
        is_hl = highlight_nodes and i in highlight_nodes
        if only_active_elements and not is_hl:
            continue
            
        fill = colors.HexColor('#ffb703') if is_hl else colors.HexColor('#8ecae6')
        stroke = colors.HexColor('#fb8500') if is_hl else colors.HexColor('#219ebc')
        
        d.add(Circle(x, y, 12, fillColor=fill, strokeColor=stroke, strokeWidth=1.5))
        d.add(String(x, y - 3, str(i), fontName='Arial-Bold', fontSize=9, fillColor=colors.HexColor('#1d3557'), textAnchor='middle'))
        
    return d

def make_pdf():
    pdf_filename = "Tai_lieu_Ly_thuyet_CTRR.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
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
        print("Falling back to Helvetica:", e)
        FONT_NAME = 'Helvetica'
        FONT_NAME_BOLD = 'Helvetica-Bold'
        FONT_NAME_ITALIC = 'Helvetica-Oblique'
        
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
        leading=13,
        textColor=colors.HexColor('#457b9d'),
        alignment=1,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1d3557'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#e63946'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2b2d42'),
        spaceAfter=6
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2b2d42')
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName=FONT_NAME_BOLD
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=FONT_NAME_BOLD,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
        alignment=1
    )
    
    story = []
    
    story.append(Spacer(1, 5))
    story.append(Paragraph("TÀI LIỆU KHẢO SÁT LÝ THUYẾT & CHẠY TỪNG BƯỚC GIẢI THUẬT ĐỒ THỊ", title_style))
    story.append(Paragraph("Hệ thống giáo trình trực quan hỗ trợ học tập môn Cấu trúc rời rạc / Lý thuyết đồ thị", subtitle_style))
    story.append(Spacer(1, 5))
    
    # ------------------ PHẦN 1: CÁC PHƯƠNG PHÁP BIỂU DIỄN ------------------
    story.append(Paragraph("1. Các phương pháp biểu diễn đồ thị và Chuyển đổi", h1_style))
    
    story.append(Paragraph("<b>Khái niệm & Định nghĩa toán học:</b> Đồ thị G = (V, E) là một cấu trúc toán học gồm tập hợp các đỉnh V và tập hợp các cạnh E nối các cặp đỉnh thuộc V. Đồ thị có thể là vô hướng (các cạnh không phân biệt hướng) hoặc có hướng (mỗi cạnh là một cặp đỉnh có thứ tự từ đỉnh đầu đến đỉnh cuối, ký hiệu là digraph). Đồ thị có trọng số là đồ thị mà mỗi cạnh được gán một giá trị số thực thể hiện chi phí, khoảng cách hoặc năng lực thông qua.", body_style))
    
    story.append(Paragraph("Để xử lý đồ thị bằng máy tính, ta sử dụng 3 phương pháp biểu diễn cơ bản:", body_style))
    story.append(Paragraph("• <b>Ma trận kề (Adjacency Matrix):</b> Mảng hai chiều kích thước |V| x |V|. Ô A[i][j] lưu giá trị trọng số cạnh (hoặc 1 nếu không trọng số) nếu có cạnh nối từ i đến j, ngược lại lưu 0 hoặc vô cực. <i>Độ phức tạp không gian:</i> O(V<sup>2</sup>). Phù hợp cho đồ thị dày, kiểm tra kết nối nhanh O(1) nhưng tốn bộ nhớ với đồ thị thưa.<br/>"
                           "• <b>Danh sách kề (Adjacency List):</b> Danh sách chứa các đỉnh kề trực tiếp của từng đỉnh. <i>Độ phức tạp không gian:</i> O(V + E). Tiết kiệm bộ nhớ tối đa cho đồ thị thưa, nhưng kiểm tra kết nối hai đỉnh mất thời gian O(bậc của đỉnh).<br/>"
                           "• <b>Danh sách cạnh (Edge List):</b> Danh sách lưu trữ trực tiếp các bộ ba (u, v, w) tương ứng với cạnh nối u, v có trọng số w. <i>Độ phức tạp không gian:</i> O(E). Cực kỳ tiện lợi cho các giải thuật duyệt cạnh trực tiếp như Kruskal.", body_style))
    
    rep_positions = [(20, 15), (100, 65), (100, 15)]
    rep_edges = [(0, 1), (0, 2), (1, 2)]
    rep_labels = {(0, 1): 4, (0, 2): 5, (1, 2): 6}
    d_rep = draw_graph(120, 80, rep_positions, rep_edges, is_directed=True, edge_labels=rep_labels)
    
    matrix_cells = [
        [Paragraph("", table_header_style), Paragraph("0", table_header_style), Paragraph("1", table_header_style), Paragraph("2", table_header_style)],
        [Paragraph("0", table_cell_bold), Paragraph("0", table_cell_style), Paragraph("4", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("1", table_cell_bold), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("6", table_cell_style)],
        [Paragraph("2", table_cell_bold), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style)]
    ]
    t_matrix = Table(matrix_cells, colWidths=[20, 20, 20, 20])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor('#1d3557')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    list_cells = [
        [Paragraph("Đỉnh", table_header_style), Paragraph("Danh sách kề (trọng số)", table_header_style)],
        [Paragraph("0", table_cell_bold), Paragraph("1 (w:4), 2 (w:5)", table_cell_style)],
        [Paragraph("1", table_cell_bold), Paragraph("2 (w:6)", table_cell_style)],
        [Paragraph("2", table_cell_bold), Paragraph("-", table_cell_style)]
    ]
    t_list = Table(list_cells, colWidths=[35, 140])
    t_list.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    edge_cells = [
        [Paragraph("Đầu", table_header_style), Paragraph("Cuối", table_header_style), Paragraph("Trọng số", table_header_style)],
        [Paragraph("0", table_cell_style), Paragraph("1", table_cell_style), Paragraph("4", table_cell_style)],
        [Paragraph("0", table_cell_style), Paragraph("2", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("2", table_cell_style), Paragraph("6", table_cell_style)]
    ]
    t_edge = Table(edge_cells, colWidths=[35, 35, 50])
    t_edge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    rep_table_data = [
        [
            Paragraph("<b>Đồ thị mẫu (3 đỉnh):</b>", h2_style),
            Paragraph("<b>Ma trận kề (Adjacency Matrix):</b>", h2_style)
        ],
        [d_rep, t_matrix],
        [
            Paragraph("<b>Danh sách kề (Adjacency List):</b>", h2_style),
            Paragraph("<b>Danh sách cạnh (Edge List):</b>", h2_style)
        ],
        [t_list, t_edge]
    ]
    t_rep_container = Table(rep_table_data, colWidths=[240, 240])
    t_rep_container.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_rep_container)
    
    # BFS/DFS Graph Config
    bfs_dfs_positions = [
        (40, 60), (140, 110), (140, 20), (280, 110), (280, 20), (380, 60)
    ]
    bfs_dfs_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (3, 5), (4, 5)]
    
    # ------------------ PHẦN 2: BFS & DFS ------------------
    story.append(PageBreak())
    story.append(Paragraph("2. Giải thuật duyệt đồ thị: BFS và DFS", h1_style))
    
    story.append(Paragraph("<b>Định nghĩa giải thuật:</b> Duyệt đồ thị là quá trình đi qua tất cả các đỉnh của đồ thị một cách hệ thống, đảm bảo mỗi đỉnh được duyệt đúng một lần.", body_style))
    story.append(Paragraph("• <b>BFS (Breadth-First Search - Duyệt theo chiều rộng):</b> Xuất phát từ đỉnh nguồn S, thuật toán loang đều ra xung quanh bằng cách duyệt qua tất cả các đỉnh có khoảng cách k cạnh trước khi chuyển sang các đỉnh kề có khoảng cách k+1 cạnh. Giải thuật sử dụng cấu trúc dữ liệu <b>Hàng đợi (Queue - FIFO)</b> để lưu trữ các đỉnh đang chờ xét kề.<br/>"
                           "• <b>DFS (Depth-First Search - Duyệt theo chiều sâu):</b> Xuất phát từ đỉnh nguồn S, thuật toán ưu tiên đi xa nhất có thể dọc theo mỗi nhánh của đồ thị trước khi thực hiện quay lui (Backtracking). Giải thuật sử dụng <b>Ngăn xếp (Stack - LIFO)</b> (hoặc cơ chế gọi hàm đệ quy của hệ thống).", body_style))
    
    story.append(Paragraph("<b>Độ phức tạp giải thuật:</b><br/>"
                           "• <i>Thời gian:</i> O(V + E) khi biểu diễn bằng danh sách kề, do mỗi đỉnh được đưa vào Queue/Stack đúng 1 lần và mỗi cạnh được xét tối đa 2 lần (với đồ thị vô hướng). Với ma trận kề, chi phí duyệt kề là O(V<sup>2</sup>).<br/>"
                           "• <i>Không gian phụ trợ:</i> O(V) để lưu trữ mảng đánh dấu `visited` và hàng đợi/ngăn xếp.", body_style))
    
    story.append(Paragraph("<b>Nhận xét & So sánh thực tế:</b><br/>"
                           "• <b>Đồ thị không trọng số:</b> BFS luôn đảm bảo tìm được đường đi ngắn nhất (ít cạnh nhất) từ nguồn tới đích vì nó loang đều theo từng tầng cạnh. DFS không có tính chất này và có thể đi vòng rất xa trước khi tới đích.<br/>"
                           "• <b>Đồ thị có trọng số:</b> Cả BFS và DFS đều <b>không thể</b> tìm được đường đi ngắn nhất do chi phí đi qua một cạnh không còn đồng nhất. Khi đó bắt buộc phải dùng thuật toán chuyên dụng như Dijkstra hoặc Bellman-Ford.", body_style))

    story.append(Paragraph("• <b>Ứng dụng thực tế:</b> BFS được dùng nhiều trong thuật toán định tuyến mạng internet, gợi ý kết nối mạng xã hội, loang màu. DFS dùng nhiều để phát hiện chu trình, phân tích liên thông mạnh, lập lịch topo công việc hoặc giải các bài toán mê cung/quay lui.", body_style))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Minh họa đồ thị vô hướng khảo sát duyệt BFS & DFS:</b>", h2_style))
    story.append(draw_graph(420, 130, bfs_dfs_positions, bfs_dfs_edges))
    
    # ------------------ BẢNG BFS & DFS ------------------
    story.append(PageBreak())
    story.append(Paragraph("<b>Bảng chạy từng bước giải thuật BFS & DFS (bắt đầu từ đỉnh 0):</b>", h2_style))
    table_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Giải thuật BFS (Bắt đầu từ 0)", table_header_style),
            Paragraph("Hàng đợi (Queue)", table_header_style),
            Paragraph("Giải thuật DFS (Bắt đầu từ 0)", table_header_style),
            Paragraph("Ngăn xếp (Stack)", table_header_style)
        ],
        [
            Paragraph("0", table_cell_style),
            Paragraph("Khởi tạo: Thăm 0", table_cell_style),
            Paragraph("[0]", table_cell_style),
            Paragraph("Khởi tạo: Thăm 0", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("Lấy 0 ra. Thăm đỉnh kề: 1, 2", table_cell_style),
            Paragraph("[1, 2]", table_cell_style),
            Paragraph("Lấy 0 ra. Thăm đỉnh kề: 1 (đi sâu)", table_cell_style),
            Paragraph("[1]", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("Lấy 1 ra. Thăm đỉnh kề: 3, 4", table_cell_style),
            Paragraph("[2, 3, 4]", table_cell_style),
            Paragraph("Lấy 1 ra. Thăm đỉnh kề: 3 (đi sâu)", table_cell_style),
            Paragraph("[3]", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("Lấy 2 ra. Đỉnh kề của 2 (4) đã được xét", table_cell_style),
            Paragraph("[3, 4]", table_cell_style),
            Paragraph("Lấy 3 ra. Thăm đỉnh kề: 5 (đi sâu)", table_cell_style),
            Paragraph("[5]", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("Lấy 3 ra. Thăm đỉnh kề: 5", table_cell_style),
            Paragraph("[4, 5]", table_cell_style),
            Paragraph("Lấy 5 ra. Thăm đỉnh kề: 4 (đi sâu)", table_cell_style),
            Paragraph("[4]", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("Lấy 4 ra. Đỉnh kề đã xét", table_cell_style),
            Paragraph("[5]", table_cell_style),
            Paragraph("Lấy 4 ra. Thăm đỉnh kề: 2 (đi sâu)", table_cell_style),
            Paragraph("[2]", table_cell_style)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("Lấy 5 ra. Hàng đợi rỗng. Kết thúc.", table_cell_style),
            Paragraph("[]", table_cell_style),
            Paragraph("Lấy 2 ra. Không còn kề chưa thăm. Quay lui.", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("KQ", table_cell_bold),
            Paragraph("Thứ tự duyệt BFS: 0, 1, 2, 3, 4, 5", table_cell_bold),
            Paragraph("-", table_cell_style),
            Paragraph("Thứ tự duyệt DFS: 0, 1, 3, 5, 4, 2", table_cell_bold),
            Paragraph("-", table_cell_style)
        ]
    ]
    
    t_bfs_dfs = Table(table_data, colWidths=[30, 140, 95, 150, 95])
    t_bfs_dfs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_bfs_dfs)
    
    # ------------------ PHẦN 3: BIPARTITE ------------------
    story.append(PageBreak())
    story.append(Paragraph("3. Kiểm tra đồ thị hai phía (Bipartite Graph Check)", h1_style))
    
    story.append(Paragraph("<b>Khái niệm & Định nghĩa toán học:</b> Một đồ thị vô hướng G = (V, E) được gọi là đồ thị hai phía (Bipartite Graph) nếu tập đỉnh V của nó có thể phân hoạch thành hai tập con độc lập V<sub>1</sub> và V<sub>2</sub> (V<sub>1</sub> giao V<sub>2</sub> bằng rỗng, V<sub>1</sub> hợp V<sub>2</sub> bằng V) sao cho mọi cạnh trong E đều kết nối một đỉnh thuộc V<sub>1</sub> với một đỉnh thuộc V<sub>2</sub>. Điều này nghĩa là không tồn tại cạnh nào nối giữa các đỉnh trong cùng một tập con.", body_style))
    
    story.append(Paragraph("<b>Định lý quyết định:</b> Một đồ thị là đồ thị hai phía <b>khi và chỉ khi đồ thị đó không chứa chu trình lẻ</b> (chu trình có số cạnh là số lẻ như C<sub>3</sub>, C<sub>5</sub>,...).", body_style))
    
    story.append(Paragraph("<b>Nguyên lý giải thuật (Tô màu đồ thị - 2-Coloring):</b><br/>"
                           "Thuật toán cố gắng tô tất cả các đỉnh của đồ thị bằng 2 màu (ví dụ Vàng và Xanh) sao cho không có hai đỉnh kề nhau nào có cùng màu. Ta khởi tạo tất cả đỉnh chưa có màu, chọn một đỉnh xuất phát tô màu Vàng (1), đưa vào Queue. Thực hiện loang BFS: Với mỗi đỉnh u lấy ra từ Queue, ta kiểm tra các đỉnh kề v của nó:<br/>"
                           "• Nếu v chưa tô màu: Tô màu v ngược với màu của u (Xanh) và đưa v vào Queue.<br/>"
                           "• Nếu v đã được tô màu: Kiểm tra màu của v. Nếu màu của v trùng với màu của u, lập tức kết luận đồ thị <b>không phải hai phía</b> và dừng thuật toán.", body_style))
    
    story.append(Paragraph("<b>Độ phức tạp thuật toán:</b> O(V + E) thời gian và O(V) không gian, tương đương một lượt duyệt BFS đầy đủ.", body_style))
    
    story.append(Paragraph("<b>Minh họa tô 2 màu trên đồ thị 2 phía (C4) và đồ thị chứa chu trình lẻ (C5):</b>", h2_style))
    
    bip_pos_1 = [(40, 20), (140, 20), (140, 100), (40, 100)]
    bip_edges_1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
    d_bip_1 = draw_graph(180, 120, bip_pos_1, bip_edges_1, highlight_nodes=[0, 2])
    
    bip_pos_2 = [(40, 20), (140, 20), (140, 100), (40, 100), (90, 60)]
    bip_edges_2 = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4)]
    d_bip_2 = draw_graph(180, 120, bip_pos_2, bip_edges_2, highlight_nodes=[0, 1, 4], highlight_edges=[(0, 1), (1, 4), (4, 0)])
    
    bip_table = Table([[d_bip_1, d_bip_2]], colWidths=[255, 255])
    bip_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(bip_table)
    story.append(Spacer(1, 5))
    story.append(Paragraph("Bên trái là đồ thị hai phía (C4) tô màu xen kẽ thành công (màu vàng/xanh lam). Bên phải là đồ thị chứa chu trình lẻ 0-1-4 (không phải hai phía) được highlight cạnh đỏ mâu thuẫn màu.", body_style))
    
    # ------------------ BẢNG BIPARTITE ------------------
    story.append(PageBreak())
    story.append(Paragraph("<b>Bảng chạy từng bước thuật toán Tô 2 màu kiểm tra Đồ thị hai phía:</b>", h2_style))
    story.append(Paragraph("<b>TH1: Chạy vết với Đồ thị hai phía C4 (bắt đầu từ đỉnh 0):</b>", h2_style))
    
    c4_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Xét U", table_header_style),
            Paragraph("Màu U", table_header_style),
            Paragraph("Đỉnh kề V của U", table_header_style),
            Paragraph("Trạng thái tô màu đỉnh kề V", table_header_style),
            Paragraph("Hàng đợi (Queue)", table_header_style)
        ],
        [
            Paragraph("0", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Khởi tạo tô đỉnh 0: Vàng (1)", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("Vàng", table_cell_style),
            Paragraph("1, 3", table_cell_style),
            Paragraph("Tô 1: Xanh (2); Tô 3: Xanh (2)", table_cell_style),
            Paragraph("[1, 3]", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("Xanh", table_cell_style),
            Paragraph("0, 2", table_cell_style),
            Paragraph("0: Vàng (đã tô); Tô 2: Vàng (1)", table_cell_style),
            Paragraph("[3, 2]", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("3", table_cell_style),
            Paragraph("Xanh", table_cell_style),
            Paragraph("0, 2", table_cell_style),
            Paragraph("0: Vàng (khớp màu); 2: Vàng (khớp màu)", table_cell_style),
            Paragraph("[2]", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("Vàng", table_cell_style),
            Paragraph("1, 3", table_cell_style),
            Paragraph("1: Xanh (khớp màu); 3: Xanh (khớp màu)", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("KQ", table_cell_bold),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Không xung đột màu. Đồ thị là HAI PHÍA.", table_cell_bold),
            Paragraph("[]", table_cell_style)
        ]
    ]
    
    t_c4 = Table(c4_data, colWidths=[35, 55, 55, 95, 180, 90])
    t_c4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_c4)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>TH2: Chạy vết với Đồ thị không hai phía C5 (bắt đầu từ đỉnh 0):</b>", h2_style))
    c5_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Xét U", table_header_style),
            Paragraph("Màu U", table_header_style),
            Paragraph("Đỉnh kề V của U", table_header_style),
            Paragraph("Trạng thái tô màu đỉnh kề V", table_header_style),
            Paragraph("Hàng đợi (Queue)", table_header_style)
        ],
        [
            Paragraph("0", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Khởi tạo tô đỉnh 0: Vàng (1)", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("Vàng", table_cell_style),
            Paragraph("1, 3, 4", table_cell_style),
            Paragraph("Tô 1: Xanh; Tô 3: Xanh; Tô 4: Xanh", table_cell_style),
            Paragraph("[1, 3, 4]", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("Xanh", table_cell_style),
            Paragraph("0, 2, 4", table_cell_style),
            Paragraph("0: Vàng; Tô 2: Vàng; 4: Xanh (Đỉnh kề 4 đã có màu Xanh trùng với màu của 1!)", table_cell_style),
            Paragraph("Dừng thuật toán", table_cell_style)
        ],
        [
            Paragraph("KQ", table_cell_bold),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Cạnh (1, 4) kết nối 2 đỉnh cùng màu Xanh -> KHÔNG PHẢI HAI PHÍA.", table_cell_bold),
            Paragraph("-", table_cell_style)
        ]
    ]
    
    t_c5 = Table(c5_data, colWidths=[35, 55, 55, 95, 180, 90])
    t_c5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f2d6d6')),
    ]))
    story.append(t_c5)
    
    # ------------------ PHẦN 4: DIJKSTRA ------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Thuật toán tìm đường đi ngắn nhất Dijkstra", h1_style))
    
    story.append(Paragraph("<b>Khái niệm toán học & Bài toán:</b> Cho đồ thị vô hướng hoặc có hướng liên thông có trọng số không âm G = (V, E, w), trong đó w(u, v) >= 0 là chi phí đi trên cạnh (u, v). Thuật toán Dijkstra dùng để tìm đường đi ngắn nhất xuất phát từ một đỉnh nguồn S cố định tới tất cả các đỉnh còn lại của đồ thị.", body_style))
    
    story.append(Paragraph("<b>Nguyên lý hoạt động (Kỹ thuật Tham lam - Greedy & Tối ưu hóa - Relaxation):</b><br/>"
                           "Giải thuật duy trì một mảng khoảng cách tạm thời `d[v]` lưu khoảng cách ngắn nhất từ nguồn S tới v tìm thấy cho tới nay. Khởi tạo `d[S] = 0` và `d[v] = vô cực` với mọi v khác S. Ở mỗi bước lặp:<br/>"
                           "1. Chọn đỉnh u chưa được cố định có giá trị `d[u]` nhỏ nhất. Đỉnh u này lúc này được <b>cố định</b> khoảng cách (không bao giờ tối ưu hơn được nữa).<br/>"
                           "2. Cập nhật (Relaxation) cho mọi đỉnh kề v chưa cố định của u: nếu `d[u] + w(u, v) < d[v]`, ta cập nhật `d[v] = d[u] + w(u, v)` và lưu vết đỉnh trước v là u (`prev[v] = u`).", body_style))
    
    story.append(Paragraph("<b>Độ phức tạp thuật toán:</b><br/>"
                           "• <i>Dùng mảng thường:</i> O(V<sup>2</sup>) thời gian. Phù hợp cho đồ thị dày kề sát nhau.<br/>"
                           "• <i>Dùng Hàng đợi ưu tiên (Binary Heap / Priority Queue):</i> O(E log V) thời gian. Cực kỳ tối ưu cho đồ thị thưa.<br/>"
                           "• <i>Không gian:</i> O(V) để lưu trữ khoảng cách, hàng đợi và vết đường đi.", body_style))
    
    story.append(Paragraph("<b>Tại sao Dijkstra không hoạt động trên đồ thị có cạnh trọng số âm?</b><br/>"
                           "Giải thuật dựa trên nguyên lý tham lam: một khi đã cố định đỉnh u có khoảng cách nhỏ nhất, thuật toán coi như đường đi tới u là ngắn nhất và không cập nhật lại. Nếu có cạnh trọng số âm, việc đi vòng qua các cạnh khác có thể mang lại tổng chi phí nhỏ hơn khoảng cách đã cố định, làm sai lệch kết quả tối ưu. Đối với đồ thị có cạnh âm, ta bắt buộc phải dùng thuật toán <b>Bellman-Ford</b>.", body_style))
    
    story.append(Paragraph("<b>Đồ thị khảo sát có trọng số mẫu (6 đỉnh):</b>", h2_style))
    
    dijkstra_positions = [
        (40, 60), (140, 110), (140, 10), (260, 110), (260, 10), (360, 60)
    ]
    dijkstra_edges = [(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5)]
    dijkstra_labels = {
        (0, 1): 4, (0, 2): 5, (1, 2): 6, (1, 3): 2, (1, 4): 7, (2, 4): 3, (3, 4): 10, (3, 5): 8, (4, 5): 4
    }
    
    d_dijkstra = draw_graph(420, 130, dijkstra_positions, dijkstra_edges, highlight_edges=[(0, 2), (2, 4), (4, 5)], edge_labels=dijkstra_labels, highlight_nodes=[0, 2, 4, 5])
    story.append(d_dijkstra)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Bảng giải bằng tay từng bước giải thuật Dijkstra (bắt đầu từ đỉnh 0):</b>", h2_style))
    dijkstra_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Đỉnh đã duyệt", table_header_style),
            Paragraph("1", table_header_style),
            Paragraph("2", table_header_style),
            Paragraph("3", table_header_style),
            Paragraph("4", table_header_style),
            Paragraph("5", table_header_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("<b>4, 0</b>", table_cell_bold),
            Paragraph("5, 0", table_cell_style),
            Paragraph("inf, -", table_cell_style),
            Paragraph("inf, -", table_cell_style),
            Paragraph("inf, -", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("0, 1", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("<b>5, 0</b>", table_cell_bold),
            Paragraph("6, 1", table_cell_style),
            Paragraph("11, 1", table_cell_style),
            Paragraph("inf, -", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("0, 1, 2", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("<b>6, 1</b>", table_cell_bold),
            Paragraph("8, 2 (min(11, 5+3))", table_cell_style),
            Paragraph("inf, -", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("0, 1, 2, 3", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("<b>8, 2</b>", table_cell_bold),
            Paragraph("14, 3 (6+8)", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("0, 1, 2, 3, 4", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("<b>12, 4</b> (min(14, 8+4))", table_cell_bold)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("0, 1, 2, 3, 4, 5", table_cell_style),
            Paragraph("4, 0", table_cell_style),
            Paragraph("5, 0", table_cell_style),
            Paragraph("6, 1", table_cell_style),
            Paragraph("8, 2", table_cell_style),
            Paragraph("12, 4", table_cell_bold)
        ]
    ]
    
    t_dijkstra = Table(dijkstra_data, colWidths=[40, 100, 74, 74, 74, 74, 74])
    t_dijkstra.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_dijkstra)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Sơ đồ đường đi ngắn nhất tối ưu tìm được:</b>", h2_style))
    d_dijk_result = draw_graph(420, 90, dijkstra_positions, dijkstra_edges, highlight_edges=[(0, 2), (2, 4), (4, 5)], edge_labels=dijkstra_labels, highlight_nodes=[0, 2, 4, 5], only_active_elements=True)
    story.append(d_dijk_result)
    story.append(Paragraph("<b>Lộ trình chi tiết:</b> 0 -> 2 -> 4 -> 5 với tổng chi phí ngắn nhất <b>d = 12</b>.", body_style))
    
    # ------------------ PHẦN 5: MST (KRUSKAL & PRIM) ------------------
    story.append(PageBreak())
    story.append(Paragraph("5. Thuật toán tìm Cây khung nhỏ nhất MST (Kruskal & Prim)", h1_style))
    
    story.append(Paragraph("<b>Khái niệm & Định nghĩa toán học:</b> Cho đồ thị vô hướng liên thông có trọng số G = (V, E, w). Cây khung (Spanning Tree) của G là một đồ thị con liên thông, chứa tất cả các đỉnh của G và không chứa chu trình. Cây khung nhỏ nhất (Minimum Spanning Tree - MST) là cây khung có tổng trọng số các cạnh của nó là nhỏ nhất. Một đồ thị có |V| đỉnh thì bất kỳ cây khung nào cũng luôn có đúng |V| - 1 cạnh.", body_style))
    
    story.append(Paragraph("Để tìm MST, ta khảo sát hai giải thuật kinh điển dùng kỹ thuật tham lam (Greedy):", body_style))
    
    story.append(Paragraph("• <b>Giải thuật Kruskal:</b> Tiếp cận dựa trên việc chọn <b>cạnh</b>. Thuật toán sắp xếp toàn bộ cạnh của đồ thị theo trọng số tăng dần. Sau đó duyệt qua từng cạnh: nếu việc đưa cạnh này vào tập cạnh hiện tại không tạo ra chu trình, ta kết nạp nó vào MST. Quá trình dừng khi đã chọn đủ |V| - 1 cạnh.<br/>"
                           "<i>Kỹ thuật kiểm tra chu trình:</i> Dùng cấu trúc dữ liệu tập hợp rời rạc <b>Disjoint Set Union (DSU)</b> với các thao tác `find` và `union` có độ phức tạp gần như O(1).<br/>"
                           "<i>Độ phức tạp:</i> O(E log E) thời gian do chi phí sắp xếp cạnh, O(V) không gian để lưu trữ cây cha DSU.", body_style))
    
    story.append(Paragraph("• <b>Giải thuật Prim:</b> Tiếp cận dựa trên việc chọn <b>đỉnh</b>. Bắt đầu từ một đỉnh gốc bất kỳ. Thuật toán xây dựng cây khung bằng cách liên tục kết nạp cạnh có trọng số nhỏ nhất nối từ một đỉnh đã nằm trong cây (V<sub>MST</sub>) tới một đỉnh chưa nằm trong cây (V \\ V<sub>MST</sub>). Quá trình lặp lại cho đến khi toàn bộ |V| đỉnh được đưa vào cây.<br/>"
                           "<i>Độ phức tạp:</i> O(V<sup>2</sup>) thời gian khi dùng mảng thường hoặc O(E log V) khi dùng Hàng đợi ưu tiên. O(V) không gian để lưu vết.", body_style))
    
    story.append(Paragraph("<b>Nhận xét & So sánh thực tế:</b> Kruskal chạy rất nhanh và trực quan trên đồ thị thưa (ít cạnh), đặc biệt thuận tiện khi danh sách cạnh đã được sắp xếp sẵn. Prim chạy hiệu quả hơn trên đồ thị dày (nhiều cạnh) khi dùng cấu trúc hàng đợi ưu tiên tối ưu.", body_style))
    
    story.append(Paragraph("<b>Đồ thị khảo sát MST mẫu (8 đỉnh):</b>", h2_style))
    
    mst_positions = [
        (40, 70), (120, 120), (120, 20), (200, 70), (280, 120), (280, 20), (360, 70), (450, 70)
    ]
    mst_edges = [
        (0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 3), (2, 5), (2, 6), (3, 6), (4, 7), (5, 6), (5, 7), (6, 7)
    ]
    mst_labels = {
        (0, 1): 4, (0, 2): 9, (0, 3): 5, (1, 4): 15, (1, 5): 2, (2, 3): 2, (2, 5): 1, (2, 6): 3,
        (3, 6): 7, (4, 7): 6, (5, 6): 2, (5, 7): 12, (6, 7): 7
    }
    mst_highlight = [(0, 1), (1, 5), (5, 2), (2, 3), (5, 6), (6, 7), (7, 4)]
    
    d_mst_initial = draw_graph(500, 140, mst_positions, mst_edges, edge_labels=mst_labels)
    story.append(d_mst_initial)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("<b>Thuật toán Kruskal (Giải bằng tay theo mẫu):</b>", h2_style))
    story.append(Paragraph("Khởi tạo ban đầu: MST = rỗng (Ø); d(MST) = 0; số đỉnh n = 8, số cạnh tối đa cần tìm là n - 1 = 7.", body_style))
    
    kruskal_data = [
        [
            Paragraph("STT", table_header_style),
            Paragraph("Sắp xếp cạnh", table_header_style),
            Paragraph("Cây khung cực tiểu (MST)", table_header_style),
            Paragraph("Chọn / Loại", table_header_style),
            Paragraph("d (tổng trọng số)", table_header_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("(2,5) : 1", table_cell_style),
            Paragraph("(2,5)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("1", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("(1,5) : 2", table_cell_style),
            Paragraph("(2,5); (1,5)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("3", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("(2,3) : 2", table_cell_style),
            Paragraph("(2,5); (1,5); (2,3)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("5", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("(5,6) : 2", table_cell_style),
            Paragraph("(2,5); (1,5); (2,3); (5,6)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("7", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("(2,6) : 3", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Loại (Tạo chu trình 2-5-6-2)", table_cell_style),
            Paragraph("-", table_cell_style)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("(0,1) : 4", table_cell_style),
            Paragraph("(2,5); (1,5); (2,3); (5,6); (0,1)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("11", table_cell_style)
        ],
        [
            Paragraph("7", table_cell_style),
            Paragraph("(0,3) : 5", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Loại (Tạo chu trình 0-1-5-2-3-0)", table_cell_style),
            Paragraph("-", table_cell_style)
        ],
        [
            Paragraph("8", table_cell_style),
            Paragraph("(4,7) : 6", table_cell_style),
            Paragraph("(2,5); (1,5); (2,3); (5,6); (0,1); (4,7)", table_cell_style),
            Paragraph("Chọn", table_cell_style),
            Paragraph("17", table_cell_style)
        ],
        [
            Paragraph("9", table_cell_style),
            Paragraph("(3,6) : 7", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Loại (Tạo chu trình 3-2-6-3)", table_cell_style),
            Paragraph("-", table_cell_style)
        ],
        [
            Paragraph("10", table_cell_style),
            Paragraph("(6,7) : 7", table_cell_style),
            Paragraph("(2,5); (1,5); (2,3); (5,6); (0,1); (4,7); (6,7)", table_cell_bold),
            Paragraph("Chọn", table_cell_style),
            Paragraph("24", table_cell_bold)
        ],
        [
            Paragraph("11", table_cell_style),
            Paragraph("(0,2) : 9", table_cell_style),
            Paragraph("Dừng vòng lặp (break) vì đã đủ |MST| = n - 1 = 7 cạnh", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style)
        ],
        [
            Paragraph("12", table_cell_style),
            Paragraph("(5,7) : 12", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style)
        ],
        [
            Paragraph("13", table_cell_style),
            Paragraph("(1,4) : 15", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style)
        ]
    ]
    
    t_kruskal = Table(kruskal_data, colWidths=[30, 75, 255, 100, 50])
    t_kruskal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-4), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-3), (-1,-1), colors.HexColor('#e5e5e5')),
    ]))
    story.append(t_kruskal)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Sơ đồ Cây khung cực tiểu MST tìm được:</b>", h2_style))
    d_mst_result = draw_graph(500, 140, mst_positions, mst_edges, highlight_edges=mst_highlight, edge_labels=mst_labels, only_active_elements=True, highlight_nodes=[0,1,2,3,4,5,6,7])
    story.append(d_mst_result)
    story.append(Paragraph("<b>Tổng trọng số cây khung cực tiểu thu được:</b> d = 24.", body_style))
    
    # ------------------ PRIM TABLE ------------------
    story.append(PageBreak())
    story.append(Paragraph("<b>Thuật toán Prim (Dựa trên tập đỉnh & lân cận):</b>", h2_style))
    story.append(Paragraph("Khác với Kruskal sắp xếp cạnh tự do, Prim loang rộng cây khung từ một đỉnh gốc bắt đầu. Lần lượt kết nạp đỉnh ngoài có khoảng cách nhỏ nhất đến tập đỉnh hiện tại của cây khung (khởi đầu từ đỉnh 0):", body_style))
    
    prim_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Đỉnh trong cây (V<sub>MST</sub>)", table_header_style),
            Paragraph("Cạnh ứng viên nối ra ngoài cây", table_header_style),
            Paragraph("Cạnh chọn", table_header_style),
            Paragraph("Trọng số", table_header_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("{0}", table_cell_style),
            Paragraph("0-1 (4), 0-2 (9), 0-3 (5)", table_cell_style),
            Paragraph("0 - 1", table_cell_style),
            Paragraph("4", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("{0, 1}", table_cell_style),
            Paragraph("0-2 (9), 0-3 (5), 1-4 (15), 1-5 (2)", table_cell_style),
            Paragraph("1 - 5", table_cell_style),
            Paragraph("2", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("{0, 1, 5}", table_cell_style),
            Paragraph("0-2 (9), 0-3 (5), 5-2 (1), 5-6 (2), 5-7 (12)", table_cell_style),
            Paragraph("5 - 2", table_cell_style),
            Paragraph("1", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("{0, 1, 2, 5}", table_cell_style),
            Paragraph("0-3 (5), 2-3 (2), 5-6 (2), 2-6 (3), 5-7 (12)", table_cell_style),
            Paragraph("2 - 3", table_cell_style),
            Paragraph("2", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("{0, 1, 2, 3, 5}", table_cell_style),
            Paragraph("5-6 (2), 2-6 (3), 3-6 (7), 5-7 (12)", table_cell_style),
            Paragraph("5 - 6", table_cell_style),
            Paragraph("2", table_cell_style)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("{0, 1, 2, 3, 5, 6}", table_cell_style),
            Paragraph("6-7 (7), 5-7 (12)", table_cell_style),
            Paragraph("6 - 7", table_cell_style),
            Paragraph("7", table_cell_style)
        ],
        [
            Paragraph("7", table_cell_style),
            Paragraph("{0..7 - trừ 4}", table_cell_style),
            Paragraph("7-4 (6), 1-4 (15)", table_cell_style),
            Paragraph("7 - 4", table_cell_bold),
            Paragraph("6", table_cell_bold)
        ],
        [
            Paragraph("KQ", table_cell_bold),
            Paragraph("Tất cả 8 đỉnh đã được đưa vào cây.", table_cell_bold),
            Paragraph("-", table_cell_style),
            Paragraph("Đầy đủ cây khung", table_cell_bold),
            Paragraph("Tổng trọng số = 24 (khớp Kruskal)", table_cell_bold)
        ]
    ]
    
    t_prim = Table(prim_data, colWidths=[30, 120, 200, 80, 80])
    t_prim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_prim)
    
    # ------------------ PHẦN 6: MAX FLOW ------------------
    story.append(PageBreak())
    story.append(Paragraph("6. Thuật toán luồng cực đại (Max Flow)", h1_style))
    
    story.append(Paragraph("<b>Khái niệm & Định nghĩa toán học:</b> Cho mạng luồng (Flow Network) là một đồ thị có hướng G = (V, E) trong đó mỗi cạnh (u, v) có dung lượng (Capacity) c(u, v) >= 0. Mạng có một đỉnh nguồn (Source) s là nơi phát luồng, và một đỉnh đích (Sink) t là nơi tiếp nhận luồng. Luồng f trên mạng G là một hàm gán cho mỗi cạnh một giá trị số thực thỏa mãn hai điều kiện:<br/>"
                           "1. <i>Ràng buộc dung lượng:</i> 0 <= f(u, v) <= c(u, v) với mọi cạnh.<br/>"
                           "2. <i>Bảo toàn luồng:</i> Tổng luồng đi vào một đỉnh bằng tổng luồng đi ra khỏi đỉnh đó (với mọi đỉnh khác s và t).", body_style))
    
    story.append(Paragraph("<b>Định lý Luồng cực đại - Lát cắt cực tiểu (Max-Flow Min-Cut Theorem):</b> Giá trị của luồng cực đại đi từ s tới t luôn bằng với dung lượng nhỏ nhất của một lát cắt (s, t-cut) phân hoạch tập đỉnh thành hai phần chứa s và t.", body_style))
    
    story.append(Paragraph("<b>Nguyên lý hoạt động thuật toán Ford-Fulkerson & Edmonds-Karp:</b><br/>"
                           "Thuật toán hoạt động trên <b>Đồ thị dư (Residual Graph) G<sub>f</sub></b>. Mỗi cạnh có hướng (u, v) trên G<sub>f</sub> biểu thị khả năng gửi thêm luồng theo chiều xuôi c<sub>f</sub>(u, v) = c(u, v) - f(u, v), và khả năng gửi trả lại luồng theo chiều ngược c<sub>f</sub>(v, u) = f(u, v). Các bước thực hiện:<br/>"
                           "1. Sử dụng giải thuật duyệt đồ thị để tìm một đường đi đơn từ s tới t trên đồ thị dư G<sub>f</sub> có dung lượng dư lớn hơn 0 (Đường tăng luồng - Augmenting Path). Giải thuật <b>Edmonds-Karp</b> sử dụng cụ thể giải thuật BFS để tìm đường đi ngắn nhất (ít cạnh nhất), giúp giới hạn số lần lặp tối đa O(VE).<br/>"
                           "2. Tìm bottleneck (df) là dung lượng dư nhỏ nhất của các cạnh trên đường đi đó.<br/>"
                           "3. Tăng luồng thực tế dọc theo đường tăng luồng thêm df (tăng luồng cạnh xuôi, giảm luồng cạnh ngược trên đồ thị dư). Lặp lại cho đến khi không còn đường đi từ s đến t.", body_style))
    
    story.append(Paragraph("<b>Độ phức tạp thuật toán:</b> O(V E<sup>2</sup>) thời gian đối với giải thuật Edmonds-Karp, độc lập với giá trị luồng tối đa, khắc phục nhược điểm lặp vô hạn của Ford-Fulkerson trên số thực.", body_style))
    
    story.append(Paragraph("<b>Minh họa đồ thị luồng tối ưu (Edmonds-Karp):</b>", h2_style))
    story.append(Paragraph("Nhãn trên cạnh biểu thị tỷ lệ luồng/dung lượng thực tế (flow/capacity). Đỉnh 0 là nguồn (Source), Đỉnh 5 là đích (Sink). Cạnh tô màu đỏ biểu thị các cạnh có luồng đi qua.", body_style))
    
    flow_edges = [
        (0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 5), (4, 3), (4, 5)
    ]
    flow_labels = {
        (0, 1): "12/16", (0, 2): "11/13", (1, 2): "0/10", (1, 3): "12/12",
        (2, 1): "0/4", (2, 4): "11/14", (3, 2): "0/9", (3, 5): "19/20",
        (4, 3): "7/7", (4, 5): "4/4"
    }
    flow_hl = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 3), (4, 5)]
    story.append(draw_graph(420, 130, bfs_dfs_positions, flow_edges, is_directed=True, highlight_edges=flow_hl, edge_labels=flow_labels))
    story.append(Spacer(1, 8))
    
    flow_data = [
        [
            Paragraph("Lần lặp", table_header_style),
            Paragraph("Đường tăng luồng tìm thấy (BFS)", table_header_style),
            Paragraph("Dung lượng dư nhỏ nhất (Bottleneck)", table_header_style),
            Paragraph("Tổng luồng tăng lũy tiến", table_header_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0 -> 1 -> 3 -> 5", table_cell_style),
            Paragraph("min(16, 12, 20) = 12", table_cell_style),
            Paragraph("12", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("0 -> 2 -> 4 -> 5", table_cell_style),
            Paragraph("min(13, 14, 4) = 4", table_cell_style),
            Paragraph("12 + 4 = 16", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("0 -> 2 -> 4 -> 3 -> 5 (Duyệt qua cạnh dư 4-3 còn 7, 3-5 còn 8)", table_cell_style),
            Paragraph("min(9, 10, 7, 8) = 7", table_cell_style),
            Paragraph("16 + 7 = 23", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("Không còn đường tăng luồng từ 0 đến 5 trên mạng dư. Kết thúc.", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Luồng cực đại = 23", table_cell_bold)
        ]
    ]
    
    t_flow = Table(flow_data, colWidths=[40, 240, 120, 110])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_flow)
    
    # ------------------ PHẦN 7: EULER ------------------
    story.append(PageBreak())
    story.append(Paragraph("7. Đường đi và chu trình Euler: Fleury vs Hierholzer", h1_style))
    
    story.append(Paragraph("<b>Khái niệm toán học & Điều kiện tồn tại:</b><br/>"
                           "• <b>Đường đi Euler (Eulerian Path):</b> Đường đi đi qua mỗi cạnh của đồ thị đúng một lần.<br/>"
                           "• <b>Chu trình Euler (Eulerian Circuit):</b> Đường đi Euler xuất phát và kết thúc tại cùng một đỉnh.<br/>"
                           "• <i>Định lý Euler vô hướng:</i> Đồ thị vô hướng liên thông G có chu trình Euler khi và chỉ khi <b>tất cả các đỉnh của đồ thị đều có bậc chẵn</b>. Đồ thị có đường đi Euler khi và chỉ khi có đúng 0 hoặc 2 đỉnh bậc lẻ.", body_style))
    
    story.append(Paragraph("Để tìm chu trình Euler, ta có hai giải thuật điển hình với phương thức tiếp cận và độ phức tạp khác nhau:", body_style))
    
    story.append(Paragraph("• <b>Giải thuật Fleury:</b> Thực hiện đi tham lam. Xuất phát tại một đỉnh, ở mỗi bước ta chọn một cạnh kề chưa đi qua để đi tiếp theo quy tắc: <b>Tránh đi qua cạnh cầu (Bridge) của đồ thị con còn lại trừ khi không còn cạnh nào khác để chọn</b> (cạnh cầu là cạnh mà nếu xóa đi sẽ làm tăng số lượng thành phần liên thông của đồ thị).<br/>"
                           "<i>Độ phức tạp:</i> O(E<sup>2</sup>) thời gian do mỗi lần chọn cạnh phải chạy thuật toán BFS/DFS để xác định xem cạnh đó có là cầu hay không.", body_style))
    
    story.append(Paragraph("• <b>Giải thuật Hierholzer:</b> Hoạt động dựa trên việc lồng ghép các chu trình con đơn giản. Bắt đầu từ một đỉnh, đi tự do theo các cạnh chưa đi cho đến khi quay về đỉnh gốc tạo thành một chu trình đơn, xóa các cạnh này và đẩy lộ trình vào một Ngăn xếp (Stack). Do tính chất bậc chẵn, nếu đồ thị còn cạnh chưa đi, ta tìm một đỉnh kề trên chu trình đã có còn cạnh chưa xét, tiếp tục đi một chu trình mới rồi ghép trực tiếp vào chu trình ban đầu bằng cơ chế pop Stack.<br/>"
                           "<i>Độ phức tạp:</i> O(E) thời gian và không gian cực kỳ tối ưu vì mỗi cạnh chỉ bị duyệt và xóa đúng một lần duy nhất.", body_style))
    
    story.append(Paragraph("<b>Minh họa đồ thị có chu trình Euler (Độ chẵn của bậc):</b>", h2_style))
    
    euler_pos = [
        (40, 60), (140, 110), (140, 10), (260, 110), (260, 10), (360, 60)
    ]
    euler_edges = [
        (0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)
    ]
    story.append(draw_graph(420, 120, euler_pos, euler_edges, highlight_edges=euler_edges))
    story.append(Spacer(1, 8))
    
    euler_compare_data = [
        [
            Paragraph("Đặc điểm", table_header_style),
            Paragraph("Giải thuật Fleury (7.4)", table_header_style),
            Paragraph("Giải thuật Hierholzer (7.5)", table_header_style)
        ],
        [
            Paragraph("Nguyên lý chính", table_cell_bold),
            Paragraph("Đi tham lam, tránh đi qua cạnh 'cầu' (bridge) của phần đồ thị còn lại trừ khi không có lựa chọn khác.", table_cell_style),
            Paragraph("Tìm các chu trình con đơn giản kề nhau và lồng chúng lại với nhau thông qua cơ chế Stack.", table_cell_style)
        ],
        [
            Paragraph("Kiểm tra cầu", table_cell_bold),
            Paragraph("Có. Đòi hỏi chạy DFS ở mỗi bước để đếm số thành phần liên thông khi thử xóa cạnh.", table_cell_style),
            Paragraph("Không. Chỉ cần quản lý danh sách cạnh kề và xóa cạnh trực tiếp.", table_cell_style)
        ],
        [
            Paragraph("Độ phức tạp", table_cell_bold),
            Paragraph("O(E<sup>2</sup>)", table_cell_style),
            Paragraph("O(E) - Rất nhanh và tối ưu", table_cell_style)
        ],
        [
            Paragraph("Kết quả lộ trình mẫu", table_cell_bold),
            Paragraph("0 -> 1 -> 2 -> 3 -> 1 -> 4 -> 3 -> 5 -> 4 -> 2 -> 0", table_cell_style),
            Paragraph("0 -> 1 -> 2 -> 3 -> 1 -> 4 -> 3 -> 5 -> 4 -> 2 -> 0", table_cell_style)
        ]
    ]
    
    t_euler = Table(euler_compare_data, colWidths=[100, 205, 205])
    t_euler.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
    ]))
    story.append(t_euler)
    
    # ------------------ BẢNG CHẠY TỪNG BƯỚC HIERHOLZER & FLEURY ------------------
    story.append(PageBreak())
    story.append(Paragraph("<b>Bảng chạy bằng tay từng bước giải thuật Tìm chu trình Euler:</b>", h2_style))
    story.append(Paragraph("<b>TH1: Chạy vết giải thuật Hierholzer (sử dụng Ngăn xếp Stack):</b>", h2_style))
    
    hier_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Đỉnh U", table_header_style),
            Paragraph("Cạnh đi tiếp khả dụng", table_header_style),
            Paragraph("Hành động", table_header_style),
            Paragraph("Stack (Ngăn xếp)", table_header_style),
            Paragraph("Chu trình Euler (Circuit)", table_header_style)
        ],
        [
            Paragraph("0", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("Tất cả", table_cell_style),
            Paragraph("Khởi tạo Stack", table_cell_style),
            Paragraph("[0]", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("(0,1), (0,2)", table_cell_style),
            Paragraph("Đi 1, xóa cạnh (0,1)", table_cell_style),
            Paragraph("[0, 1]", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("(1,2), (1,3), (1,4)", table_cell_style),
            Paragraph("Đi 2, xóa cạnh (1,2)", table_cell_style),
            Paragraph("[0, 1, 2]", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("(2,0), (2,3), (2,4)", table_cell_style),
            Paragraph("Đi 0, xóa cạnh (2,0)", table_cell_style),
            Paragraph("[0, 1, 2, 0]", table_cell_style),
            Paragraph("[]", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("Không còn", table_cell_style),
            Paragraph("Pop 0 đưa vào Circuit", table_cell_style),
            Paragraph("[0, 1, 2]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("(2,3), (2,4)", table_cell_style),
            Paragraph("Đi 3, xóa cạnh (2,3)", table_cell_style),
            Paragraph("[0, 1, 2, 3]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("3", table_cell_style),
            Paragraph("(3,1), (3,4), (3,5)", table_cell_style),
            Paragraph("Đi 1, xóa cạnh (3,1)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("7", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("(1,4)", table_cell_style),
            Paragraph("Đi 4, xóa cạnh (1,4)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("8", table_cell_style),
            Paragraph("4", table_cell_style),
            Paragraph("(4,3), (4,5)", table_cell_style),
            Paragraph("Đi 3, xóa cạnh (4,3)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4, 3]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("9", table_cell_style),
            Paragraph("3", table_cell_style),
            Paragraph("(3,5)", table_cell_style),
            Paragraph("Đi 5, xóa cạnh (3,5)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4, 3, 5]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("10", table_cell_style),
            Paragraph("5", table_cell_style),
            Paragraph("(5,4)", table_cell_style),
            Paragraph("Đi 4, xóa cạnh (5,4)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4, 3, 5, 4]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("11", table_cell_style),
            Paragraph("4", table_cell_style),
            Paragraph("(4,2)", table_cell_style),
            Paragraph("Đi 2, xóa cạnh (4,2)", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4, 3, 5, 4, 2]", table_cell_style),
            Paragraph("[0]", table_cell_style)
        ],
        [
            Paragraph("12", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("Không còn", table_cell_style),
            Paragraph("Pop 2 đưa vào Circuit", table_cell_style),
            Paragraph("[0, 1, 2, 3, 1, 4, 3, 5, 4]", table_cell_style),
            Paragraph("[0, 2]", table_cell_style)
        ],
        [
            Paragraph("13-21", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Pop dần toàn bộ Stack còn lại", table_cell_style),
            Paragraph("[]", table_cell_style),
            Paragraph("[0, 2, 4, 5, 3, 4, 1, 3, 2, 1, 0]", table_cell_bold)
        ]
    ]
    
    t_hier = Table(hier_data, colWidths=[30, 45, 115, 120, 100, 100])
    t_hier.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_hier)
    
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>TH2: Chạy vết giải thuật Fleury (Tránh chọn cạnh cầu - bridge):</b>", h2_style))
    
    fleury_data = [
        [
            Paragraph("Bước", table_header_style),
            Paragraph("Đỉnh U", table_header_style),
            Paragraph("Các cạnh đi tiếp khả dụng", table_header_style),
            Paragraph("Trạng thái Cầu (Bridge) của các cạnh kề", table_header_style),
            Paragraph("Cạnh chọn", table_header_style),
            Paragraph("Lộ trình Euler lũy tiến", table_header_style)
        ],
        [
            Paragraph("1", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("(0,1), (0,2)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (0,1), xóa", table_cell_style),
            Paragraph("0 -> 1", table_cell_style)
        ],
        [
            Paragraph("2", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("(1,2), (1,3), (1,4)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (1,2), xóa", table_cell_style),
            Paragraph("0 -> 1 -> 2", table_cell_style)
        ],
        [
            Paragraph("3", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("(2,0), (2,3), (2,4)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (2,0), xóa", table_cell_style),
            Paragraph("0 -> 1 -> 2 -> 0", table_cell_style)
        ],
        [
            Paragraph("4", table_cell_style),
            Paragraph("0", table_cell_style),
            Paragraph("(0,2)", table_cell_style),
            Paragraph("Chỉ còn 1 cạnh (bắt buộc chọn)", table_cell_style),
            Paragraph("Chọn (0,2), xóa", table_cell_style),
            Paragraph("0 -> 1 -> 2 -> 0 -> 2", table_cell_style)
        ],
        [
            Paragraph("5", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("(2,3), (2,4)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (2,4), xóa", table_cell_style),
            Paragraph("... -> 2 -> 4", table_cell_style)
        ],
        [
            Paragraph("6", table_cell_style),
            Paragraph("4", table_cell_style),
            Paragraph("(4,1), (4,3), (4,5)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (4,5), xóa", table_cell_style),
            Paragraph("... -> 4 -> 5", table_cell_style)
        ],
        [
            Paragraph("7", table_cell_style),
            Paragraph("5", table_cell_style),
            Paragraph("(5,3)", table_cell_style),
            Paragraph("Chỉ còn 1 cạnh (bắt buộc chọn)", table_cell_style),
            Paragraph("Chọn (5,3), xóa", table_cell_style),
            Paragraph("... -> 5 -> 3", table_cell_style)
        ],
        [
            Paragraph("8", table_cell_style),
            Paragraph("3", table_cell_style),
            Paragraph("(3,1), (3,4), (3,2)", table_cell_style),
            Paragraph("Không có cạnh cầu", table_cell_style),
            Paragraph("Chọn (3,4), xóa", table_cell_style),
            Paragraph("... -> 3 -> 4", table_cell_style)
        ],
        [
            Paragraph("9", table_cell_style),
            Paragraph("4", table_cell_style),
            Paragraph("(4,1)", table_cell_style),
            Paragraph("Chỉ còn 1 cạnh", table_cell_style),
            Paragraph("Chọn (4,1), xóa", table_cell_style),
            Paragraph("... -> 4 -> 1", table_cell_style)
        ],
        [
            Paragraph("10", table_cell_style),
            Paragraph("1", table_cell_style),
            Paragraph("(1,3)", table_cell_style),
            Paragraph("Chỉ còn 1 cạnh", table_cell_style),
            Paragraph("Chọn (1,3), xóa", table_cell_style),
            Paragraph("... -> 1 -> 3", table_cell_style)
        ],
        [
            Paragraph("11", table_cell_style),
            Paragraph("3", table_cell_style),
            Paragraph("(3,2)", table_cell_style),
            Paragraph("Chỉ còn 1 cạnh", table_cell_style),
            Paragraph("Chọn (3,2), xóa", table_cell_style),
            Paragraph("... -> 3 -> 2", table_cell_style)
        ],
        [
            Paragraph("12", table_cell_style),
            Paragraph("2", table_cell_style),
            Paragraph("Không còn", table_cell_style),
            Paragraph("Hoàn thành chu trình", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("0->1->2->0->2->4->5->3->4->1->3->2 (khớp Euler)", table_cell_bold)
        ]
    ]
    
    t_fl = Table(fleury_data, colWidths=[30, 45, 110, 140, 95, 90])
    t_fl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2ece9')),
    ]))
    story.append(t_fl)
    
    doc.build(story)
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    make_pdf()
