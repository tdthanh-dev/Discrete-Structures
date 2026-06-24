import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def make_plan_pdf():
    pdf_filename = "Ke_hoach_Phan_chia_Cong_viec.pdf"
    
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
        print("Falling back to standard fonts:", e)
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
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#457b9d'),
        alignment=1,
        spaceAfter=20
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
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9.5,
        leading=14,
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
    
    # Title & Subtitle
    story.append(Paragraph("KẾ HOẠCH PHÂN CHIA CÔNG VIỆC NHÓM 5 NGƯỜI", title_style))
    story.append(Paragraph("Dự án: Hệ thống trực quan hóa cấu trúc rời rạc & giải thuật đồ thị", subtitle_style))
    
    # Section 1: Phân chia công việc (5 Thành viên)
    story.append(Paragraph("I. BẢNG PHÂN CHIA CÔNG VIỆC (Mỗi thành viên làm 1 nhóm thuật toán)", h1_style))
    story.append(Paragraph("Đảm bảo tất cả 5 thành viên đều phát triển cả hai phần: <b>Cài đặt thuật toán thuần (Backend)</b> và <b>Trực quan hóa hoạt họa trên giao diện (Frontend/GUI)</b>.", body_style))
    
    # Table headers and data
    headers = [
        Paragraph("<b>Thành viên</b>", table_cell_bold_style),
        Paragraph("<b>Nhóm Thuật toán chịu trách nhiệm</b>", table_cell_bold_style),
        Paragraph("<b>Chi tiết phần việc (Thuật toán + GUI)</b>", table_cell_bold_style)
    ]
    
    data = [
        headers,
        [
            Paragraph("<b>Thành viên 1</b>", table_cell_bold_style),
            Paragraph("Duyệt đồ thị &<br/>Biểu diễn đồ thị", table_cell_style),
            Paragraph("• Viết mô-đun chuyển đổi cấu trúc (Ma trận kề, ds kề, ds cạnh cho cả đồ thị vô hướng & có hướng) ở <code>utils/conversions.py</code>.<br/>• Cài đặt thuật toán duyệt <b>BFS & DFS</b> thuần và generator.<br/>• Tích hợp hiển thị biểu diễn đồ thị và hoạt họa BFS/DFS lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 2</b>", table_cell_bold_style),
            Paragraph("Đường đi ngắn nhất &<br/>Đồ thị hai phía", table_cell_style),
            Paragraph("• Cài đặt giải thuật <b>Dijkstra</b> sử dụng Priority Queue (Min-Heap), kiểm soát trọng số âm.<br/>• Cài đặt thuật toán kiểm tra <b>Đồ thị 2 phía</b> (tô màu BFS/DFS), truy vết ngược lấy chu trình lẻ làm minh chứng phản ví dụ.<br/>• Tích hợp highlight lộ trình Dijkstra và vẽ màu đỏ/xanh (hoặc highlight chu trình lẻ) lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 3</b>", table_cell_bold_style),
            Paragraph("Cây khung nhỏ nhất<br/>(MST)", table_cell_style),
            Paragraph("• Cài đặt thuật toán <b>Prim</b> (dùng Heap).<br/>• Cài đặt thuật toán <b>Kruskal</b> sắp xếp cạnh kết hợp cấu trúc dữ liệu tập hợp rời rạc (<b>DSU</b>) để phát hiện chu trình nhanh $O(1)$.<br/>• Tích hợp trực quan hóa cây khung nhỏ nhất (MST) và tính tổng trọng số lên GUI.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 4</b>", table_cell_bold_style),
            Paragraph("Luồng cực đại<br/>(Max Flow)", table_cell_style),
            Paragraph("• Cài đặt thuật toán <b>Edmonds-Karp</b> (phương pháp Ford-Fulkerson tối ưu hóa đường đi ngắn nhất bằng BFS trên mạng dư).<br/>• Tích hợp hiển thị tỷ lệ <code>flow/capacity</code> thực tế trên các cạnh và highlight các đường tăng luồng qua từng bước.<br/>• Phụ giúp Thành viên 1 xây dựng khung Canvas vẽ đồ thị chính.", table_cell_style)
        ],
        [
            Paragraph("<b>Thành viên 5</b>", table_cell_bold_style),
            Paragraph("Đường đi &<br/>Chu trình Euler", table_cell_style),
            Paragraph("• Cài đặt giải thuật **Fleury** (duyệt kiểm tra và tránh các cạnh cầu - bridge).<br/>• Cài đặt giải thuật **Hierholzer** tối ưu $O(E)$ sử dụng cơ chế lưu trữ Stack.<br/>• Tích hợp mô phỏng bước đi của Fleury và cơ chế push/pop đỉnh vào Stack của Hierholzer lên GUI.", table_cell_style)
        ]
    ]
    
    # Render table
    col_widths = [75, 120, 315]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2eafc')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1d3557')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a8dadc')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # Section 2: Quy trình triển khai
    story.append(Paragraph("II. HƯỚNG DẪN TRIỂN KHAI THEO THỨ TỰ (4 Giai đoạn)", h1_style))
    
    story.append(Paragraph("<b>Giai đoạn 1: Xây dựng nền tảng và Thuật toán thuần (Tuần 1 - 2)</b>", body_bold_style))
    story.append(Paragraph("• <i>Thứ tự thực hiện:</i> Thành viên 1 thiết lập các cấu trúc dữ liệu đồ thị chung và hàm chuyển đổi trong <code>utils/conversions.py</code>. Thành viên 4 cùng lúc thiết lập khung giao diện cơ bản (cửa sổ chính, các nút chức năng, bảng kết quả log).", bullet_style))
    story.append(Paragraph("• <i>Triển khai thuật toán:</i> Tất cả các thành viên viết giải thuật thuần túy của mình bên trong thư mục <code>algorithms/pure/</code>. Các thuật toán này chỉ nhận tham số đầu vào và trả về kết quả cuối cùng, kiểm thử trực tiếp bằng CLI.", bullet_style))
    
    story.append(Paragraph("<b>Giai đoạn 2: Phát triển các bộ sinh Hoạt họa (Tuần 3)</b>", body_bold_style))
    story.append(Paragraph("• <i>Thứ tự thực hiện:</i> Chuyển đổi thuật toán từ dạng hàm thông thường sang dạng **Generator (sử dụng <code>yield</code>)** trong thư mục <code>algorithms/</code>.", bullet_style))
    story.append(Paragraph("• <i>Mục tiêu:</i> Ở mỗi bước lặp chính (ví dụ: duyệt qua một cạnh, tô màu một đỉnh, tìm thấy một đường đi), thuật toán sẽ <code>yield</code> ra trạng thái hiện tại (danh sách đỉnh đã thăm, tập cạnh tích lũy, các biến trung gian).", bullet_style))
    
    story.append(Paragraph("<b>Giai đoạn 3: Thiết kế Giao diện Canvas và Liên kết hoạt họa (Tuần 4)</b>", body_bold_style))
    story.append(Paragraph("• <i>Thứ tự thực hiện:</i> Thành viên 1 hoàn thiện Canvas vẽ đồ thị. Từng thành viên thực hiện viết hàm điều khiển vẽ trạng thái của thuật toán mình trên Canvas (dùng các màu khác nhau để biểu thị trạng thái đỉnh/cạnh) và in log giải thích tương ứng.", bullet_style))
    story.append(Paragraph("• <i>Mục tiêu:</i> Khi chọn thuật toán và click 'Chạy hoạt họa', GUI sẽ liên tục lấy trạng thái tiếp theo từ Generator và vẽ lại đồ thị sau mỗi khoảng thời gian delay nhất định.", bullet_style))
    
    story.append(Paragraph("<b>Giai đoạn 4: Tích hợp Đồ thị mẫu, Thử nghiệm & Kiểm thử (Tuần 5)</b>", body_bold_style))
    story.append(Paragraph("• <i>Thứ tự thực hiện:</i> Cài đặt chức năng nạp đồ thị mẫu cho mỗi thuật toán (mỗi thành viên tự vẽ một đồ thị mẫu chuẩn mực nhất để nạp mặc định cho giải thuật của mình, giúp người dùng dễ dàng thử nghiệm nhanh mà không cần vẽ tay).", bullet_style))
    story.append(Paragraph("• <i>Mục tiêu:</i> Thực hiện test chéo (cross-testing) giữa các thành viên, sửa các lỗi giao diện và tối ưu hóa code.", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # Section 3: Yêu cầu đạt được
    story.append(Paragraph("III. YÊU CẦU ĐẠT ĐƯỢC (Định nghĩa Hoàn thành - Definition of Done)", h1_style))
    
    story.append(Paragraph("<b>1. Yêu cầu về thuật toán (Backend)</b>", body_bold_style))
    story.append(Paragraph("• <b>Đúng đắn và tối ưu:</b> Thuật toán phải giải quyết đúng bài toán, đạt độ phức tạp thời gian tiêu chuẩn (Dijkstra/Prim đạt $O(E \\log V)$, Kruskal $O(E \\log E)$, Hierholzer $O(E)$).", bullet_style))
    story.append(Paragraph("• <b>Tính nhất quán (Deterministic):</b> Các đỉnh kề phải được sắp xếp theo số thứ tự tăng dần trước khi duyệt để kết quả chạy vết bằng tay và bằng máy trùng khớp hoàn toàn.", bullet_style))
    story.append(Paragraph("• <b>Bẫy lỗi đầy đủ:</b> Kiểm tra và ném ra các ngoại lệ thích hợp (ví dụ: Dijkstra có trọng số âm, Kruskal cho đồ thị có hướng, Max Flow không chọn đỉnh đích...).", bullet_style))
    
    story.append(Paragraph("<b>2. Yêu cầu về trực quan hóa (Frontend)</b>", body_bold_style))
    story.append(Paragraph("• <b>Hoạt họa mượt mà:</b> Chạy hoạt họa từng bước không được gây đơ/treo giao diện (phải dùng giải pháp Generator lấy dữ liệu tuần tự kết hợp hàm <code>after()</code> của Tkinter).", bullet_style))
    story.append(Paragraph("• <b>Màu sắc trực quan:</b> Sử dụng màu sắc tương phản rõ ràng để phân biệt trạng thái (ví dụ: cam cho đỉnh được chọn, xanh lá cho đỉnh/cạnh đang xét, đỏ cho kết quả đường đi/MST cuối cùng).", bullet_style))
    story.append(Paragraph("• <b>Nhãn thông tin rõ ràng:</b> In chi tiết log từng bước (bước hiện tại đang xét đỉnh nào, cạnh nào được chọn, tại sao bỏ qua...) để phục vụ mục đích tự học lý thuyết.", bullet_style))
    
    story.append(Paragraph("<b>3. Yêu cầu về mã nguồn và tài liệu</b>", body_bold_style))
    story.append(Paragraph("• <b>Mã nguồn sạch (Clean Code):</b> Đặt tên biến, hàm theo đúng chuẩn toán học. Viết docstring giải thích tham số đầu vào và đầu ra cho tất cả các hàm thuật toán.", bullet_style))
    story.append(Paragraph("• <b>Tích hợp Git liên tục:</b> Các thành viên làm việc trên các nhánh (branch) riêng biệt và merge vào nhánh <code>main</code> thông qua Pull Request sau khi đã kiểm thử kỹ lưỡng.", bullet_style))
    
    doc.build(story)
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    make_plan_pdf()
