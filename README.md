# 🌐 Discrete Structures & Graph Algorithms Visualizer

Hệ thống giáo trình trực quan hỗ trợ giảng dạy và học tập môn **Cấu trúc rời rạc / Lý thuyết đồ thị**. Ứng dụng cung cấp giao diện tương tác (GUI) giúp vẽ đồ thị, chạy mô phỏng từng bước (animation) các thuật toán đồ thị kinh điển kèm theo log chi tiết và bảng chạy vết (trace table).

---

## 🚀 Các Tính Năng Chính

1. **Vẽ đồ thị tương tác:**
   - Tạo đỉnh mới bằng cách click chuột trái vào vùng trống.
   - Nối cạnh (vô hướng/có hướng) có trọng số bằng cách click liên tiếp 2 đỉnh.
   - Xóa đỉnh và các cạnh liên quan qua menu chuột phải.
2. **Hỗ trợ đa dạng thuật toán:** 9 giải thuật đồ thị cốt lõi được mô phỏng trực quan.
3. **Chế độ hoạt họa (Step-by-step Animation):** Cho phép xem luồng chạy của thuật toán dưới dạng hoạt ảnh chậm, highlight đỉnh/cạnh đang xét, và in log giải thích chi tiết từng bước.
4. **Biểu diễn đồ thị:** Tự động chuyển đổi và hiển thị đồ thị dưới 3 dạng: **Ma trận kề**, **Danh sách kề**, và **Danh sách cạnh**.
5. **Đồ thị mẫu (Demos):** Tích hợp sẵn các đồ thị mẫu chuẩn hóa cho từng thuật toán để người dùng nạp nhanh và thử nghiệm.
6. **Lưu trữ & Xuất bản:**
   - Lưu cấu trúc đồ thị ra file JSON (`graph.json`) và nạp lại khi cần.
   - Chụp canvas và xuất đồ thị thành ảnh dạng `.png` hoặc `.ps`.

---

## 📚 Tóm Tắt Lý Thuyết & Giải Thuật Cài Đặt

### 1. Biểu Diễn Đồ Thị (Graph Representations)
Đồ thị $G = (V, E)$ được biểu diễn bằng 3 phương pháp cơ bản trên máy tính:
* **Ma trận kề (Adjacency Matrix):** Mảng 2 chiều kích thước $|V| \times |V|$. Độ phức tạp không gian: $O(V^2)$. Kiểm tra kết nối nhanh $O(1)$ nhưng tốn bộ nhớ với đồ thị thưa.
* **Danh sách kề (Adjacency List):** Danh sách chứa các đỉnh kề của từng đỉnh. Độ phức tạp không gian: $O(V + E)$. Tiết kiệm bộ nhớ tối đa cho đồ thị thưa.
* **Danh sách cạnh (Edge List):** Lưu danh sách các bộ ba $(u, v, w)$ tương ứng với cạnh nối u và v có trọng số w. Độ phức tạp không gian: $O(E)$. Rất hữu ích cho thuật toán Kruskal.

---

### 2. Duyệt Đồ Thị: BFS và DFS
Duyệt qua tất cả các đỉnh của đồ thị một cách hệ thống:
* **BFS (Breadth-First Search - Duyệt theo chiều rộng):** Loang đều ra xung quanh theo từng tầng khoảng cách k cạnh. Sử dụng hàng đợi **Queue (FIFO)**. Tìm đường đi ngắn nhất trên đồ thị không trọng số.
* **DFS (Depth-First Search - Duyệt theo chiều sâu):** Ưu tiên đi xa nhất có thể dọc theo mỗi nhánh trước khi quay lui (Backtracking). Sử dụng **Stack (LIFO)** hoặc đệ quy hệ thống.
* **Độ phức tạp:** Thời gian $O(V + E)$, không gian phụ trợ $O(V)$.

---

### 3. Kiểm Tra Đồ Thị Hai Phía (Bipartite Graph Check)
* **Khái niệm:** Đồ thị hai phía là đồ thị mà tập đỉnh $V$ có thể phân hoạch thành hai tập con độc lập $V_1, V_2$ sao cho mọi cạnh chỉ nối một đỉnh thuộc $V_1$ với một đỉnh thuộc $V_2$.
* **Định lý:** Đồ thị là hai phía khi và chỉ khi không chứa chu trình lẻ (odd cycle).
* **Giải thuật:** Sử dụng thuật toán **Tô 2 màu (2-Coloring)** bằng DFS/BFS. Nếu phát hiện cạnh nối giữa hai đỉnh cùng màu, giải thuật kết luận đồ thị không phải hai phía và truy vết trả về chu trình lẻ làm mâu thuẫn minh chứng.
* **Độ phức tạp:** Thời gian $O(V + E)$, không gian $O(V)$.

---

### 4. Tìm Đường Đi Ngắn Nhất: Dijkstra
* **Bài toán:** Tìm đường đi ngắn nhất từ một đỉnh nguồn $S$ tới tất cả các đỉnh còn lại trên đồ thị có trọng số không âm ($w(u, v) \ge 0$).
* **Nguyên lý:** Kỹ thuật Tham lam (Greedy) kết hợp Tối ưu hóa (Relaxation). Liên tục chọn đỉnh u chưa cố định có khoảng cách tạm thời $d[u]$ nhỏ nhất, cố định khoảng cách này, sau đó cập nhật cho các đỉnh kề v:
  $$d[v] = \min(d[v], d[u] + w(u, v))$$
* **Độ phức tạp:** Sử dụng **Priority Queue (Min-Heap)** đạt hiệu năng $O(E \log V)$.
* *Lưu ý:* Dijkstra không hoạt động trên đồ thị có cạnh trọng số âm (khi đó phải dùng Bellman-Ford).

---

### 5. Cây Khung Nhỏ Nhất (Minimum Spanning Tree - MST)
Tìm cây con chứa tất cả $|V|$ đỉnh của đồ thị liên thông với đúng $|V|-1$ cạnh sao cho tổng trọng số các cạnh là nhỏ nhất.
* **Giải thuật Kruskal (Duyệt theo cạnh):**
  - Sắp xếp tất cả các cạnh theo trọng số tăng dần.
  - Lần lượt lấy từng cạnh: nếu không tạo thành chu trình với tập cạnh hiện tại, ta thêm cạnh đó vào MST.
  - Sử dụng cấu trúc dữ liệu **Disjoint Set Union (DSU)** với kỹ thuật nén đường để kiểm tra chu trình và gộp tập hợp trong thời gian gần như $O(1)$.
  - **Độ phức tạp:** $O(E \log E)$ thời gian (chủ yếu do sắp xếp cạnh).
* **Giải thuật Prim (Duyệt theo đỉnh):**
  - Khởi đầu từ một đỉnh gốc bất kỳ.
  - Liên tục kết nạp cạnh ngắn nhất nối từ tập đỉnh đã nằm trong cây sang tập đỉnh chưa nằm trong cây.
  - Sử dụng **Priority Queue** để quản lý các cạnh ứng viên nối ra ngoài cây.
  - **Độ phức tạp:** $O(E \log V)$ thời gian.

---

### 6. Luồng Cực Đại: Edmonds-Karp
* **Bài toán:** Trên mạng luồng có đỉnh nguồn $s$ và đỉnh đích $t$, tìm giá trị luồng lớn nhất truyền từ $s$ đến $t$ thỏa mãn ràng buộc dung lượng cạnh và bảo toàn luồng tại các đỉnh trung gian.
* **Giải thuật:** Là một phiên bản cụ thể của Ford-Fulkerson, Edmonds-Karp sử dụng duyệt **BFS** để tìm đường tăng luồng ngắn nhất (ít cạnh nhất) trên đồ thị dư (Residual Graph). Sau đó, tìm dung lượng dư nhỏ nhất trên đường đi (bottleneck) để cộng dồn vào luồng cực đại và cập nhật lại đồ thị dư (cạnh xuôi giảm dung lượng dư, cạnh ngược tăng dung lượng dư).
* **Độ phức tạp:** Giới hạn số lần lặp tối đa, đạt độ phức tạp thời gian cố định $O(V E^2)$, không phụ thuộc vào giá trị luồng cực đại.

---

### 7. Chu Trình và Đường Đi Euler (Eulerian Path & Circuit)
* **Khái niệm:** Đường đi Euler đi qua mỗi cạnh đúng 1 lần. Chu trình Euler là đường đi Euler khép kín.
* **Định lý:** Đồ thị vô hướng liên thông có chu trình Euler khi tất cả đỉnh có bậc chẵn; có đường đi Euler khi có đúng 0 hoặc 2 đỉnh bậc lẻ.
* **Giải thuật Fleury:** Đi tham lam, chỉ đi qua cạnh cầu (Bridge) khi không còn lựa chọn nào khác. Độ phức tạp: $O(E^2)$ thời gian do mỗi bước phải chạy DFS để kiểm tra cạnh cầu.
* **Giải thuật Hierholzer:** Xây dựng và lồng ghép các chu trình con đơn giản thông qua cơ chế **Stack**. Độ phức tạp: $O(E)$ thời gian và không gian cực kỳ tối ưu do mỗi cạnh chỉ bị duyệt và xóa đúng 1 lần.

---

## 🛠️ Hướng Dẫn Cài Đặt và Chạy

### Yêu Cầu Hệ Thống
* Python 3.8 trở lên.
* Thư viện giao diện chuẩn `tkinter` (thường đi kèm sẵn với bản cài đặt Python trên Windows).
* Thư viện xử lý ảnh `Pillow` (để chụp và xuất ảnh `.png`).

### Cài Đặt Thư Viện Phụ Thuộc
Chạy lệnh sau trong terminal để cài đặt Pillow:
```bash
pip install Pillow
```

### Chạy Ứng Dụng
Kích hoạt giao diện ứng dụng từ thư mục gốc của dự án:
```bash
python main.py
```

---

## 🖥️ Hướng Dẫn Sử Dụng Giao Diện (GUI)

1. **Vẽ đồ thị bằng tay:**
   - **Thêm Đỉnh:** Click chuột trái vào vị trí trống trên màn hình Canvas (đỉnh tự động đánh số từ 0).
   - **Thêm Cạnh:** Click chọn đỉnh xuất phát (đỉnh sẽ đổi sang màu cam), click tiếp vào đỉnh đích. Nhập trọng số của cạnh vào hộp thoại hiện lên.
   - **Xóa Đỉnh:** Click chuột phải vào đỉnh muốn xóa và chọn `Xoa dinh X`.
2. **Chọn Thuật Toán & Cấu Hình:**
   - Chọn loại đồ thị **Có hướng** hoặc **Vô hướng** tại góc trên bên phải.
   - Chọn thuật toán cần mô phỏng (Dijkstra, Kruskal, Prim, Max Flow, BFS, DFS, Đồ thị hai phía, Fleury, Hierholzer).
   - Thiết lập đỉnh bắt đầu (`Start`) và đỉnh kết thúc (`End` - bắt buộc với Dijkstra tìm đường cụ thể hoặc Max Flow).
3. **Mô Phỏng & Theo Dõi Kết Quả:**
   - Click `Chay thuat toan` để nhận ngay kết quả cuối cùng hiển thị trên canvas và hộp log.
   - Click `Chay hoat hoa tung buoc` để xem hoạt ảnh chạy của giải thuật. Click `Dung hoat hoa` để dừng animation.
   - Kết quả phân tích chi tiết (bảng chạy vết, lộ trình cụ thể, tổng trọng số, dung lượng luồng, v.v.) sẽ được in ra khung text `Ket qua` bên dưới.
4. **Biểu Diễn Đồ Thị:**
   - Click `Bieu dien Do thi` để xem ma trận kề, danh sách kề và danh sách cạnh tương ứng với đồ thị hiện tại trên Canvas.

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
├── algorithms/              # Mã nguồn cài đặt thuật toán
│   ├── pure/                # Phiên bản thuật toán thuần (không chứa generator phục vụ GUI)
│   │   ├── bipartite.py
│   │   ├── dijkstra.py
│   │   ├── fleury.py
│   │   ├── hierholzer.py
│   │   ├── kruskal.py
│   │   ├── max_flow.py
│   │   ├── prim.py
│   │   └── traversal.py
│   ├── bipartite.py         # Phiên bản generator tô màu + tìm chu trình lẻ
│   ├── dijkstra.py          # Phiên bản generator Dijkstra
│   ├── fleury.py            # Phiên bản generator Fleury
│   ├── hierholzer.py        # Phiên bản generator Hierholzer
│   ├── kruskal.py           # Phiên bản generator Kruskal
│   ├── max_flow.py          # Phiên bản generator Edmonds-Karp
│   ├── prim.py              # Phiên bản generator Prim
│   └── traversal.py         # Phiên bản generator BFS & DFS
├── utils/
│   ├── conversions.py       # Xử lý chuyển đổi qua lại giữa ma trận kề, ds kề, ds cạnh
│   └── __init__.py
├── main.py                  # Điểm khởi chạy chương trình (gọi gui.py)
├── gui.py                   # Cài đặt giao diện Tkinter và điều phối hoạt họa
├── graph.json               # Lưu trữ cấu hình đồ thị hiện tại dưới dạng JSON
└── README.md                # Tài liệu hướng dẫn sử dụng & cơ sở lý thuyết
```
