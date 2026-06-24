import json
import math
import heapq
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageGrab

from algorithms.dijkstra import dijkstra, dijkstra_generator
from algorithms.kruskal import kruskal, kruskal_generator
from algorithms.traversal import bfs, dfs, bfs_generator, dfs_generator
from algorithms.bipartite import check_bipartite, check_bipartite_generator
from algorithms.prim import prim, prim_generator
from algorithms.fleury import find_eulerian_path_or_circuit_fleury, find_eulerian_path_or_circuit_fleury_generator
from algorithms.hierholzer import find_eulerian_path_or_circuit_hierholzer, find_eulerian_path_or_circuit_hierholzer_generator
from algorithms.max_flow import max_flow, max_flow_generator
from utils.conversions import (
    to_adjacency_matrix, to_adjacency_list, to_edge_list,
    parse_adjacency_matrix, parse_adjacency_list, parse_edge_list
)


RADIUS = 18
NODE_FILL = "#8ecae6"
NODE_SELECTED = "#ffb703"
EDGE_NORMAL = "#6c757d"
EDGE_ACTIVE = "#2a9d8f"
EDGE_PATH = "#d62828"
BG_COLOR = "#f8f9fa"


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ung dung Do thi - Dijkstra va Kruskal")
        self.root.geometry("1180x760")

        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.active_edges = set()
        self.path_edges = set()
        self.active_nodes = set()
        self.node_colors = {}
        self.edge_flows = {}
        self.graph_file = "graph.json"
        self.is_animating = False
        self.animation_job = None
        self.current_generator = None

        self.is_directed = tk.BooleanVar(value=False)
        self.algorithm_choice = tk.StringVar(value="dijkstra")
        self.start_node_var = tk.StringVar(value="0")
        self.end_node_var = tk.StringVar(value="")

        self._build_ui()
        self._refresh_node_selectors()
        self.log(
            "Huong dan nhanh:\n"
            "- Click vao vung trong de tao dinh.\n"
            "- Click 2 dinh lien tiep de tao canh, sau do nhap trong so.\n"
            "- Chon che do co huong neu muon tao do thi co huong.\n"
            "- Dijkstra ho tro tim duong di ngan nhat; Kruskal tim cay khung nho nhat."
        )

    def _build_ui(self):
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        left_panel = tk.Frame(container, bg=BG_COLOR, padx=12, pady=12)
        left_panel.pack(side="left", fill="both", expand=True)

        right_panel = tk.Frame(container, bg="#ffffff", width=340, padx=12, pady=12)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        self.canvas = tk.Canvas(
            left_panel,
            width=780,
            height=680,
            bg="white",
            highlightthickness=1,
            highlightbackground="#ced4da",
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        tk.Label(
            right_panel,
            text="Dieu khien",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        mode_frame = tk.LabelFrame(right_panel, text="Loai do thi", bg="#ffffff", padx=8, pady=8)
        mode_frame.pack(fill="x", pady=(0, 10))
        tk.Checkbutton(
            mode_frame,
            text="Do thi co huong",
            variable=self.is_directed,
            bg="#ffffff",
            command=self.redraw,
        ).pack(anchor="w")

        algo_frame = tk.LabelFrame(right_panel, text="Thuat toan", bg="#ffffff", padx=8, pady=8)
        algo_frame.pack(fill="x", pady=(0, 10))

        ttk.Radiobutton(algo_frame, text="Dijkstra", value="dijkstra", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Kruskal", value="kruskal", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Prim", value="prim", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Fleury (Euler)", value="fleury", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Hierholzer (Euler)", value="hierholzer", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Max Flow", value="max_flow", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="BFS (Duyệt rộng)", value="bfs", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="DFS (Duyệt sâu)", value="dfs", variable=self.algorithm_choice).pack(anchor="w")
        ttk.Radiobutton(algo_frame, text="Đồ thị hai phía", value="bipartite", variable=self.algorithm_choice).pack(anchor="w")

        selector_frame = tk.Frame(algo_frame, bg="#ffffff")
        selector_frame.pack(fill="x", pady=(8, 0))
        tk.Label(selector_frame, text="Start:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        tk.Label(selector_frame, text="End:", bg="#ffffff").grid(row=1, column=0, sticky="w")

        self.start_combo = ttk.Combobox(selector_frame, textvariable=self.start_node_var, state="readonly")
        self.start_combo.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 6))
        self.end_combo = ttk.Combobox(selector_frame, textvariable=self.end_node_var, state="readonly")
        self.end_combo.grid(row=1, column=1, sticky="ew", padx=(8, 0))
        selector_frame.columnconfigure(1, weight=1)

        demo_frame = tk.LabelFrame(right_panel, text="Nap do thi mau", bg="#ffffff", padx=8, pady=8)
        demo_frame.pack(fill="x", pady=(0, 10))

        self.demo_choice = ttk.Combobox(
            demo_frame,
            values=["Dijkstra", "Kruskal/Prim", "BFS/DFS", "Đồ thị hai phía", "Max Flow", "Euler"],
            state="readonly",
        )
        self.demo_choice.set("Dijkstra")
        self.demo_choice.pack(side="left", fill="x", expand=True, padx=(0, 6))

        def load_selected_demo():
            val = self.demo_choice.get()
            if val == "Dijkstra":
                self.load_dijkstra_demo_graph()
            elif val == "Kruskal/Prim":
                self.load_kruskal_demo_graph()
            elif val == "BFS/DFS":
                self.load_traversal_demo_graph()
            elif val == "Đồ thị hai phía":
                self.load_bipartite_demo_graph()
            elif val == "Max Flow":
                self.load_max_flow_demo_graph()
            elif val == "Euler":
                self.load_euler_demo_graph()

        tk.Button(
            demo_frame,
            text="Nap",
            command=load_selected_demo,
            bg="#e9ecef",
            relief="flat",
            padx=8,
        ).pack(side="right")

        button_frame = tk.LabelFrame(right_panel, text="Thao tac", bg="#ffffff", padx=8, pady=8)
        button_frame.pack(fill="x", pady=(0, 10))

        buttons = [
            ("Chay thuat toan", self.run_selected_algorithm),
            ("Chay hoat hoa tung buoc", self.run_animation),
            ("Dung hoat hoa", self.stop_animation),
            ("Kiem tra Do thi 2 phia", self.run_bipartite_check),
            ("Bieu dien Do thi", self.show_representations),
            ("Tai tu JSON", self.load_graph),
            ("Luu JSON", self.save_graph_json),
            ("Luu hinh .png", self.save_canvas_png),
            ("Luu hinh .ps", self.save_canvas_postscript),
            ("Xoa ket qua", self.clear_highlights),
            ("Xoa tat ca", self.clear_all),
        ]

        for label, command in buttons:
            tk.Button(
                button_frame,
                text=label,
                command=command,
                bg="#e9ecef",
                relief="flat",
                padx=8,
                pady=6,
            ).pack(fill="x", pady=3)

        info_frame = tk.LabelFrame(right_panel, text="Ket qua", bg="#ffffff", padx=8, pady=8)
        info_frame.pack(fill="both", expand=True)

        self.output = ScrolledText(info_frame, height=18, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

    def log(self, text):
        self.output.insert("end", text + "\n\n")
        self.output.see("end")

    def log_and_print(self, text):
        self.log(text)
        print(text)
        print()

    def distance(self, p1, p2):
        return int(round(math.hypot(p1[0] - p2[0], p1[1] - p2[1])))

    def get_node_index(self, x, y):
        for i, (nx, ny) in enumerate(self.nodes):
            if (nx - x) ** 2 + (ny - y) ** 2 <= (RADIUS + 6) ** 2:
                return i
        return None

    def on_canvas_click(self, event):
        node_index = self.get_node_index(event.x, event.y)

        if node_index is None:
            self.nodes.append((event.x, event.y))
            self.selected_node = None
            self._refresh_node_selectors()
            self.clear_highlights(redraw=False)
            self.redraw()
            self.log(f"Da tao dinh {len(self.nodes) - 1} tai ({event.x}, {event.y}).")
            return

        if self.selected_node is None:
            self.selected_node = node_index
            self.redraw()
            return

        if self.selected_node == node_index:
            self.selected_node = None
            self.redraw()
            return

        default_weight = self.distance(self.nodes[self.selected_node], self.nodes[node_index])
        weight = simpledialog.askinteger(
            "Trong so canh",
            f"Nhap trong so cho canh {self.selected_node} -> {node_index}:",
            initialvalue=default_weight,
            minvalue=-999999,
            maxvalue=999999,
            parent=self.root,
        )

        if weight is not None:
            self.add_edge(self.selected_node, node_index, weight)
            direction_text = "co huong" if self.is_directed.get() else "vo huong"
            self.log(f"Da tao canh {self.selected_node} -> {node_index} (w={weight}, {direction_text}).")

        self.selected_node = None
        self.redraw()

    def on_right_click(self, event):
        node_index = self.get_node_index(event.x, event.y)
        if node_index is None:
            return

        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=f"Xoa dinh {node_index}", command=lambda: self.remove_node(node_index))
        menu.tk_popup(event.x_root, event.y_root)

    def add_edge(self, u, v, w):
        for idx, (a, b, _) in enumerate(self.edges):
            same_direct = a == u and b == v
            same_undirect = not self.is_directed.get() and a == v and b == u
            if same_direct or same_undirect:
                self.edges[idx] = (u, v, w)
                return
        self.edges.append((u, v, w))

    def remove_node(self, node_index):
        self.nodes.pop(node_index)
        new_edges = []
        for u, v, w in self.edges:
            if u == node_index or v == node_index:
                continue
            if u > node_index:
                u -= 1
            if v > node_index:
                v -= 1
            new_edges.append((u, v, w))
        self.edges = new_edges
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(f"Da xoa dinh {node_index} va cac canh lien quan.")

    def _edge_key(self, u, v):
        return (u, v) if self.is_directed.get() else tuple(sorted((u, v)))

    def clear_highlights(self, redraw=True):
        self.active_edges.clear()
        self.path_edges.clear()
        self.active_nodes.clear()
        self.node_colors.clear()
        self.edge_flows.clear()
        if redraw:
            self.redraw()

    def redraw(self):
        self.canvas.delete("all")

        for u, v, w in self.edges:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            key = self._edge_key(u, v)

            color = EDGE_NORMAL
            width = 2
            if key in self.active_edges:
                color = EDGE_ACTIVE
                width = 4
            if key in self.path_edges:
                color = EDGE_PATH
                width = 4

            self._draw_edge(x1, y1, x2, y2, color, width, directed=self.is_directed.get())
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            
            flow_val = self.edge_flows.get((u, v), 0)
            if not self.is_directed.get():
                if (u, v) in self.edge_flows:
                    flow_val = self.edge_flows[(u, v)]
                elif (v, u) in self.edge_flows:
                    flow_val = self.edge_flows[(v, u)]
            label = f"{flow_val}/{w}" if self.edge_flows else str(w)
            
            self.canvas.create_text(mx, my - 10, text=label, fill="#d00000", font=("Segoe UI", 10, "bold"))

        for i, (x, y) in enumerate(self.nodes):
            fill = NODE_FILL
            outline = "#264653"
            width = 2
            if self.node_colors and i in self.node_colors:
                fill = "#ffadad" if self.node_colors[i] == 0 else "#9bf6ff"
            if i == self.selected_node:
                fill = NODE_SELECTED
            if i in self.active_nodes:
                outline = EDGE_PATH
                width = 3

            self.canvas.create_oval(
                x - RADIUS,
                y - RADIUS,
                x + RADIUS,
                y + RADIUS,
                fill=fill,
                outline=outline,
                width=width,
            )
            self.canvas.create_text(x, y, text=str(i), font=("Segoe UI", 11, "bold"))

    def _draw_edge(self, x1, y1, x2, y2, color, width, directed=False):
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return

        ux = dx / length
        uy = dy / length
        start_x = x1 + ux * RADIUS
        start_y = y1 + uy * RADIUS
        end_x = x2 - ux * RADIUS
        end_y = y2 - uy * RADIUS

        if directed:
            self.canvas.create_line(
                start_x,
                start_y,
                end_x,
                end_y,
                fill=color,
                width=width,
                arrow=tk.LAST,
                arrowshape=(12, 14, 5),
            )
        else:
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=width)

    def build_graph(self):
        graph = {i: [] for i in range(len(self.nodes))}
        for u, v, w in self.edges:
            graph[u].append((v, w))
            if not self.is_directed.get():
                graph[v].append((u, w))
        return graph

    def dijkstra(self, start):
        graph = self.build_graph()
        return dijkstra(graph, start)

    def kruskal(self):
        if self.is_directed.get():
            raise ValueError("Kruskal chi ap dung cho do thi vo huong.")
        return kruskal(len(self.nodes), self.edges)

    def reconstruct_path(self, prev, start, end):
        if end is None or end == "":
            return []
        end = int(end)
        if start == end:
            return [start]
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        if not path or path[0] != start:
            return []
        return path

    def highlight_path(self, path):
        self.path_edges.clear()
        self.active_nodes = set(path)
        for i in range(len(path) - 1):
            self.path_edges.add(self._edge_key(path[i], path[i + 1]))

    def highlight_edges(self, edge_list):
        self.active_edges = {self._edge_key(u, v) for u, v, _ in edge_list}
        self.active_nodes = {u for u, _, _ in edge_list} | {v for _, v, _ in edge_list}

    def run_selected_algorithm(self):
        if not self.nodes:
            messagebox.showwarning("Thieu du lieu", "Hay ve it nhat mot dinh.")
            return

        self.clear_highlights(redraw=False)
        algorithm = self.algorithm_choice.get()

        try:
            start = int(self.start_node_var.get()) if self.start_node_var.get() != "" else 0
        except ValueError:
            messagebox.showerror("Loi", "Gia tri start khong hop le.")
            return

        if start < 0 or start >= len(self.nodes):
            messagebox.showerror("Loi", "Dinh bat dau khong ton tai.")
            return

        try:
            if algorithm == "dijkstra":
                dist, prev = self.dijkstra(start)
                target_text = self.end_node_var.get().strip()
                path = self.reconstruct_path(prev, start, target_text) if target_text else []
                if path:
                    self.highlight_path(path)
                else:
                    self.active_nodes = {node for node, value in dist.items() if value < float("inf")}

                lines = [f"Dijkstra tu dinh {start}:"]
                for node in sorted(dist):
                    value = "INF" if dist[node] == float("inf") else dist[node]
                    lines.append(f"  d({start}, {node}) = {value}")
                if target_text:
                    target = int(target_text)
                    if path:
                        lines.append(f"Duong di ngan nhat {start} -> {target}: {' -> '.join(map(str, path))}")
                    else:
                        lines.append(f"Khong tim thay duong di tu {start} den {target}.")
                self.log_and_print("\n".join(lines))

            elif algorithm == "kruskal":
                mst, total = self.kruskal()
                self.highlight_edges(mst)
                lines = ["Kruskal - Cay khung nho nhat:"]
                lines.extend(f"  ({u}, {v}, {w})" for u, v, w in mst)
                lines.append(f"Tong trong so = {total}")
                self.log_and_print("\n".join(lines))

            elif algorithm == "prim":
                graph = self.build_graph()
                mst, total = prim(len(self.nodes), graph, start)
                self.highlight_edges(mst)
                lines = [f"Prim - Cay khung nho nhat bat dau tu dinh {start}:"]
                lines.extend(f"  ({u}, {v}, {w})" for u, v, w in mst)
                lines.append(f"Tong trong so = {total}")
                self.log_and_print("\n".join(lines))

            elif algorithm == "max_flow":
                target_text = self.end_node_var.get().strip()
                if not target_text:
                    messagebox.showerror("Loi", "Max Flow yeu cau phai chon dinh ket thuc (End).")
                    return
                try:
                    target = int(target_text)
                except ValueError:
                    messagebox.showerror("Loi", "Dinh ket thuc khong hop le.")
                    return
                
                if target < 0 or target >= len(self.nodes):
                    messagebox.showerror("Loi", "Dinh ket thuc khong ton tai.")
                    return
                    
                if start == target:
                    messagebox.showerror("Loi", "Dinh bat dau va ket thuc khong duoc trung nhau.")
                    return
                    
                val, flow_dict, paths = max_flow(len(self.nodes), self.edges, start, target, self.is_directed.get())
                self.edge_flows = flow_dict
                self.active_edges = {self._edge_key(u, v) for (u, v) in flow_dict if flow_dict[(u, v)] > 0}
                self.active_nodes = {start, target}
                
                lines = [f"Edmonds-Karp - Luong cuc dai tu {start} den {target}:"]
                lines.append(f"  Gia tri luong cuc dai = {val}")
                if paths:
                    lines.append("  Cac duong tang luong (Augmenting paths):")
                    for p, f in paths:
                        lines.append(f"    {' -> '.join(map(str, p))} (tang luong: {f})")
                else:
                    lines.append("  Khong co duong tang luong nao.")
                self.log_and_print("\n".join(lines))

            elif algorithm in ("fleury", "hierholzer"):
                graph = self.build_graph()
                is_directed = self.is_directed.get()
                if algorithm == "fleury":
                    res = find_eulerian_path_or_circuit_fleury(graph, is_directed)
                else:
                    res = find_eulerian_path_or_circuit_hierholzer(graph, is_directed)

                if res[0] is None:
                    messagebox.showerror("Khong co duong di/chu trinh Euler", res[1])
                    return
                else:
                    path, path_type = res
                    self.path_edges = {self._edge_key(path[i], path[i+1]) for i in range(len(path)-1)}
                    self.active_nodes = set(path)
                    
                    lines = [
                        f"Tim thay {path_type}:",
                        f"  Lo trinh: {' -> '.join(map(str, path))}"
                    ]
                    self.log_and_print("\n".join(lines))

            elif algorithm in ("bfs", "dfs"):
                graph = self.build_graph()
                if algorithm == "bfs":
                    visited_nodes, traversal_edges = bfs(graph, start)
                    name = "BFS (Duyet rong)"
                else:
                    visited_nodes, traversal_edges = dfs(graph, start)
                    name = "DFS (Duyet sau)"

                self.active_nodes = set(visited_nodes)
                self.active_edges = {self._edge_key(u, v) for u, v, _ in traversal_edges}

                lines = [f"{name} bat dau tu dinh {start}:"]
                lines.append(f"  Thu tu duyet: {' -> '.join(map(str, visited_nodes))}")
                if traversal_edges:
                    lines.append("  Cac canh di qua:")
                    lines.extend(f"    ({u} -> {v})" for u, v, _ in traversal_edges)
                self.log_and_print("\n".join(lines))

            elif algorithm == "bipartite":
                self.run_bipartite_check()

        except ValueError as exc:
            messagebox.showerror("Khong the chay", str(exc))
            return

        self.redraw()

    def run_animation(self):
        if self.is_animating:
            self.stop_animation()
            return

        if not self.nodes:
            messagebox.showwarning("Thieu du lieu", "Hay ve it nhat mot dinh.")
            return

        self.clear_highlights(redraw=False)
        algorithm = self.algorithm_choice.get()

        if algorithm not in ("dijkstra", "bfs", "dfs", "bipartite", "prim", "kruskal", "max_flow", "fleury", "hierholzer"):
            messagebox.showinfo("Hoat hoa", f"Thuat toan '{algorithm}' chua ho tro Hoat hoa.")
            return

        try:
            start = int(self.start_node_var.get()) if self.start_node_var.get() != "" else 0
        except ValueError:
            messagebox.showerror("Loi", "Gia tri start khong hop le.")
            return

        if start < 0 or start >= len(self.nodes):
            messagebox.showerror("Loi", "Dinh bat dau khong ton tai.")
            return

        self.is_animating = True
        self.log(f"--- BAT DAU HOAT HOA THUAT TOAN: {algorithm.upper()} ---")

        if algorithm == "dijkstra":
            graph = self.build_graph()
            self.current_generator = dijkstra_generator(graph, start)
        elif algorithm == "bfs":
            graph = self.build_graph()
            self.current_generator = bfs_generator(graph, start)
        elif algorithm == "dfs":
            graph = self.build_graph()
            self.current_generator = dfs_generator(graph, start)
        elif algorithm == "bipartite":
            graph = self.build_graph()
            self.current_generator = check_bipartite_generator(graph)
        elif algorithm == "prim":
            graph = self.build_graph()
            self.current_generator = prim_generator(len(self.nodes), graph, start)
        elif algorithm == "kruskal":
            if self.is_directed.get():
                messagebox.showerror("Loi", "Kruskal chi ho tro do thi vo huong.")
                self.is_animating = False
                return
            self.current_generator = kruskal_generator(len(self.nodes), self.edges)
        elif algorithm == "max_flow":
            target_text = self.end_node_var.get().strip()
            if not target_text:
                messagebox.showerror("Loi", "Max Flow yeu cau chon dinh ket thuc (End).")
                self.is_animating = False
                return
            target = int(target_text)
            if start == target:
                messagebox.showerror("Loi", "Dinh bat dau va ket thuc khong duoc trung nhau.")
                self.is_animating = False
                return
            self.current_generator = max_flow_generator(len(self.nodes), self.edges, start, target, self.is_directed.get())
        elif algorithm == "fleury":
            graph = self.build_graph()
            self.current_generator = find_eulerian_path_or_circuit_fleury_generator(graph, self.is_directed.get())
        elif algorithm == "hierholzer":
            graph = self.build_graph()
            self.current_generator = find_eulerian_path_or_circuit_hierholzer_generator(graph, self.is_directed.get())

        self.animate_next_step()

    def animate_next_step(self):
        if not self.is_animating:
            return

        try:
            step_type, data = next(self.current_generator)
        except StopIteration:
            self.log("--- HOAT HOA KET THUC THUAT TOAN ---")
            self.is_animating = False
            return
        except Exception as e:
            messagebox.showerror("Loi", f"Loi trong qua trinh chay thuat toan: {e}")
            self.is_animating = False
            return

        algorithm = self.algorithm_choice.get()
        
        self.active_edges.clear()
        self.path_edges.clear()
        self.active_nodes.clear()
        
        if algorithm == "dijkstra":
            if step_type == "START":
                dist, prev, start_node = data
                self.active_nodes = {start_node}
                self.log(f"Bat dau Dijkstra tu dinh {start_node}. Khoi tao khoang cach.")
            elif step_type == "EXAMINE":
                dist, prev, u = data
                self.active_nodes = {u}
                self.log(f"Lay dinh {u} co khoang cach nho nhat tu hang doi uu tien (d={dist[u]}).")
            elif step_type in ("RELAX", "SKIP"):
                dist, prev, edge_data = data
                if step_type == "RELAX":
                    u, v, weight, new_dist = edge_data
                    self.active_edges.add(self._edge_key(u, v))
                    self.active_nodes = {u, v}
                    self.log(f"  -> Cap nhat (Relax) canh {u} -> {v}: d({v}) = d({u}) + {weight} = {new_dist}")
                else:
                    u, v, weight = edge_data
                    self.log(f"  -> Bo qua canh {u} -> {v} vi khong toi uu hon.")
            elif step_type == "FINISHED":
                dist, prev = data
                self.log(f"Dijkstra hoan thanh.")
                start = int(self.start_node_var.get()) if self.start_node_var.get() != "" else 0
                target_text = self.end_node_var.get().strip()
                path = self.reconstruct_path(prev, start, target_text) if target_text else []
                if path:
                    self.highlight_path(path)
                    self.log(f"  Duong di ngan nhat den {target_text}: {' -> '.join(map(str, path))}")
                else:
                    self.active_nodes = {node for node, val in dist.items() if val < float("inf")}
                self.is_animating = False

        elif algorithm in ("bfs", "dfs"):
            if step_type == "START":
                visited, edges, structure = data
                self.active_nodes = set(visited)
                self.log(f"Bat dau duyet {algorithm.upper()}.")
            elif step_type == "STEP":
                visited, edges, structure, u, current_edge = data
                self.active_nodes = set(visited)
                for mu, mv, mw in edges:
                    self.path_edges.add(self._edge_key(mu, mv))
                if current_edge:
                    su, sv, sw = current_edge
                    self.active_edges.add(self._edge_key(su, sv))
                    self.log(f"Duyet qua canh {su} -> {sv}. Day {sv} vao {'Queue' if algorithm == 'bfs' else 'Stack'}.")
                else:
                    self.log(f"Ghe tham va danh dau dinh {u}.")
                self.log(f"  {'Queue' if algorithm == 'bfs' else 'Stack'} hien tai: {structure}")
            elif step_type == "FINISHED":
                visited, edges = data
                self.active_nodes = set(visited)
                for mu, mv, mw in edges:
                    self.path_edges.add(self._edge_key(mu, mv))
                self.log(f"Hoan thanh duyet {algorithm.upper()}. Thu tu duyet: {visited}")
                self.is_animating = False

        elif algorithm == "bipartite":
            if step_type == "START":
                color, _ = data
                self.log("Bat dau kiem tra do thi hai phia (Bipartite).")
            elif step_type == "COLOR":
                color, node, color_val, edge = data
                self.node_colors = color
                if edge:
                    self.active_edges.add(self._edge_key(edge[0], edge[1]))
                self.log(f"To dinh {node} bang mau {'Do' if color_val == 0 else 'Xanh'}.")
            elif step_type == "CONFLICT":
                color, odd_cycle, edge = data
                self.node_colors = color
                self.active_edges.add(self._edge_key(edge[0], edge[1]))
                self.highlight_path(odd_cycle)
                self.log(f"PHAT HIEN XUNG DOT! Canh {edge[0]} - {edge[1]} co cung mau. Tim thay chu trinh le: {' -> '.join(map(str, odd_cycle))}")
            elif step_type == "FINISHED":
                is_bipartite, result = data
                if is_bipartite:
                    self.node_colors = result
                    self.log("Hoan thanh. Do thi la do thi hai phia.")
                else:
                    self.log("Hoan thanh. Do thi KHONG phai do thi hai phia.")
                self.is_animating = False

        elif algorithm == "prim":
            if step_type == "START":
                visited, mst, total = data
                self.active_nodes = set(visited)
                self.log(f"Bat dau Prim tu dinh {self.start_node_var.get()}. Khoi tao visited = {visited}")
            elif step_type in ("EXAMINE", "STEP", "SKIP"):
                visited, mst, (u, v, w) = data
                self.active_nodes = set(visited)
                for mu, mv, mw in mst:
                    self.path_edges.add(self._edge_key(mu, mv))
                self.active_edges.add(self._edge_key(u, v))
                
                if step_type == "EXAMINE":
                    self.log(f"Xem xet canh co trong so nho nhat tu hang doi uu tien: ({u} - {v}) voi w={w}")
                elif step_type == "STEP":
                    self.log(f"  -> Chap nhan canh ({u} - {v}). Them vao MST. Visited them dinh {v}.")
                elif step_type == "SKIP":
                    self.log(f"  -> Bo qua canh ({u} - {v}) vi dinh {v} da duoc tham (tranh chu trinh).")
            elif step_type == "FINISHED":
                visited, mst, total = data
                self.active_nodes = set(visited)
                for mu, mv, mw in mst:
                    self.path_edges.add(self._edge_key(mu, mv))
                self.log(f"Prim hoan thanh. Tong trong so MST = {total}")
                self.is_animating = False
                
        elif algorithm == "kruskal":
            if step_type == "START":
                mst, total, _ = data
                self.log("Bat dau Kruskal. Sap xep tat ca cac canh theo thu tu tang dan cua trong so...")
            elif step_type == "STEP":
                mst, total, (u, v, w), accepted = data
                for mu, mv, mw in mst:
                    self.path_edges.add(self._edge_key(mu, mv))
                self.active_edges.add(self._edge_key(u, v))
                if accepted:
                    self.log(f"Xem xet canh ({u} - {v}, w={w}): Chap nhan. Khong tao chu trinh.")
                else:
                    self.log(f"Xem xet canh ({u} - {v}, w={w}): Bo qua. Tao chu trinh voi MST hien tai.")
            elif step_type == "FINISHED":
                mst, total, _ = data
                for mu, mv, mw in mst:
                    self.path_edges.add(self._edge_key(mu, mv))
                self.log(f"Kruskal hoan thanh. Tong trong so MST = {total}")
                self.is_animating = False
                
        elif algorithm == "max_flow":
            if step_type == "START":
                self.log("Bat dau Edmonds-Karp Max Flow. Khoi tao luong = 0 tren tat ca cac canh.")
            elif step_type == "STEP":
                max_flow_val, flow_dict, path, path_flow = data
                self.edge_flows = flow_dict
                self.highlight_path(path)
                self.log(f"Tim thay duong tang luong: {' -> '.join(map(str, path))} | Luong tang them = {path_flow} (Luong cuc dai hien tai = {max_flow_val})")
            elif step_type == "FINISHED":
                max_flow_val, orig_flow, paths = data
                self.edge_flows = orig_flow
                self.log(f"Edmonds-Karp hoan thanh. Luong cuc dai = {max_flow_val}")
                self.is_animating = False
                
        elif algorithm == "fleury":
            if step_type == "START":
                path, path_type, _ = data
                self.log(f"Khoi chay Fleury. Loai lo trinh du kien: {path_type}")
            elif step_type == "STEP":
                path, curr, next_node, eid = data
                for i in range(len(path)-1):
                    self.path_edges.add(self._edge_key(path[i], path[i+1]))
                self.active_nodes = {curr, next_node}
                self.log(f"Di chuyen: {curr} -> {next_node} (xoa canh de tranh di qua lai)")
            elif step_type == "FINISHED":
                path, path_type, _ = data
                for i in range(len(path)-1):
                    self.path_edges.add(self._edge_key(path[i], path[i+1]))
                self.log(f"Fleury hoan thanh. Lo trinh Euler: {' -> '.join(map(str, path))}")
                self.is_animating = False
                
        elif algorithm == "hierholzer":
            if step_type == "START":
                stack, path, path_type = data
                self.log(f"Khoi chay Hierholzer. Stack bat dau: {stack}. Loai: {path_type}")
            elif step_type == "PUSH":
                stack, path, (u, v) = data
                self.active_nodes = set(stack)
                self.active_edges.add(self._edge_key(u, v))
                self.log(f"Di tu {u} den {v}. Day {v} vao Stack: {stack}")
            elif step_type == "POP":
                stack, path, popped = data
                self.active_nodes = set(stack)
                self.log(f"Dinh {popped} khong con canh ke chua di. Pop {popped} khoi Stack dua vao Path: {path}")
            elif step_type == "FINISHED":
                path, path_type = data
                self.log(f"Hierholzer hoan thanh. Lo trinh Euler: {' -> '.join(map(str, path))}")
                self.is_animating = False

        self.redraw()
        if self.is_animating:
            self.animation_job = self.root.after(1000, self.animate_next_step)

    def stop_animation(self):
        self.is_animating = False
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.clear_highlights()
        self.log("Da dung va xoa hoat hoa.")

    def run_bipartite_check(self):
        if not self.nodes:
            messagebox.showwarning("Thieu du lieu", "Hay ve it nhat mot dinh.")
            return

        self.clear_highlights(redraw=False)
        graph = self.build_graph()
        is_bipartite, result = check_bipartite(graph)

        if is_bipartite:
            self.node_colors = result
            set_a = [node for node, col in result.items() if col == 0]
            set_b = [node for node, col in result.items() if col == 1]
            
            lines = [
                "KHOI CHAY: Kiem tra do thi 2 phia",
                "KET QUA: Do thi la do thi 2 phia (Bipartite).",
                f"  Tap A (Mau Do nhat): {set_a}",
                f"  Tap B (Mau Xanh nhat): {set_b}"
            ]
            self.log_and_print("\n".join(lines))
        else:
            # Result is an odd cycle
            self.active_nodes = set(result)
            self.active_edges = {self._edge_key(result[i], result[i+1]) for i in range(len(result)-1)}
            
            lines = [
                "KHOI CHAY: Kiem tra do thi 2 phia",
                "KET QUA: Do thi KHONG phai la do thi 2 phia.",
                f"  Phat hien chu trinh le: {' -> '.join(map(str, result))}"
            ]
            self.log_and_print("\n".join(lines))

        self.redraw()

    def show_representations(self):
        window = tk.Toplevel(self.root)
        window.title("Bieu dien Do thi (Chuyen doi qua lai)")
        window.geometry("600x480")
        window.grab_set()
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        nodes_count = len(self.nodes)
        is_directed = self.is_directed.get()
        
        matrix_text = to_adjacency_matrix(nodes_count, self.edges, is_directed)
        list_text = to_adjacency_list(nodes_count, self.edges, is_directed)
        edges_text = to_edge_list(self.edges, is_directed)
        
        # 1. Adjacency Matrix Tab
        tab_matrix = tk.Frame(notebook)
        notebook.add(tab_matrix, text="Ma tran ke")
        
        txt_matrix = ScrolledText(tab_matrix, height=15, font=("Consolas", 10))
        txt_matrix.insert("1.0", matrix_text)
        txt_matrix.pack(fill="both", expand=True, padx=5, pady=5)
        
        def apply_matrix():
            try:
                content = txt_matrix.get("1.0", "end")
                n, edges = parse_adjacency_matrix(content)
                self.load_parsed_graph(n, edges)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Loi", f"Loi cu phap ma tran ke: {e}")
                
        tk.Button(tab_matrix, text="Ap dung (Ve lai do thi)", command=apply_matrix, bg="#e9ecef", relief="flat", pady=6).pack(fill="x", padx=5, pady=5)
        
        # 2. Adjacency List Tab
        tab_list = tk.Frame(notebook)
        notebook.add(tab_list, text="Danh sach ke")
        
        txt_list = ScrolledText(tab_list, height=15, font=("Consolas", 10))
        txt_list.insert("1.0", list_text)
        txt_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        def apply_list():
            try:
                content = txt_list.get("1.0", "end")
                n, edges = parse_adjacency_list(content)
                self.load_parsed_graph(n, edges)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Loi", f"Loi cu phap danh sach ke: {e}")
                
        tk.Button(tab_list, text="Ap dung (Ve lai do thi)", command=apply_list, bg="#e9ecef", relief="flat", pady=6).pack(fill="x", padx=5, pady=5)
        
        # 3. Edge List Tab
        tab_edges = tk.Frame(notebook)
        notebook.add(tab_edges, text="Danh sach canh")
        
        txt_edges = ScrolledText(tab_edges, height=15, font=("Consolas", 10))
        txt_edges.insert("1.0", edges_text)
        txt_edges.pack(fill="both", expand=True, padx=5, pady=5)
        
        def apply_edges():
            try:
                content = txt_edges.get("1.0", "end")
                n, edges = parse_edge_list(content)
                self.load_parsed_graph(n, edges)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Loi", f"Loi cu phap danh sach canh: {e}")
                
        tk.Button(tab_edges, text="Ap dung (Ve lai do thi)", command=apply_edges, bg="#e9ecef", relief="flat", pady=6).pack(fill="x", padx=5, pady=5)

    def load_parsed_graph(self, n, edges):
        import math
        cx, cy = 390, 340
        r = 200
        self.nodes = []
        for i in range(n):
            angle = 2 * math.pi * i / n if n > 0 else 0
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            self.nodes.append((int(x), int(y)))
            
        self.edges = []
        seen = set()
        for u, v, w in edges:
            if not self.is_directed.get():
                key = tuple(sorted((u, v)))
            else:
                key = (u, v)
            if key not in seen:
                seen.add(key)
                self.edges.append((u, v, w))
                
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(f"Da tai do thi moi tu bieu dien van ban ({n} dinh).")

    def save_graph_json(self):
        path = filedialog.asksaveasfilename(
            title="Luu do thi dang JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=self.graph_file,
        )
        if not path:
            return

        data = {
            "directed": self.is_directed.get(),
            "nodes": self.nodes,
            "edges": self.edges,
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        self.graph_file = path
        self.log(f"Da luu do thi vao: {path}")

    def load_graph(self):
        path = filedialog.askopenfilename(
            title="Tai do thi tu JSON",
            filetypes=[("JSON files", "*.json")],
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.nodes = [tuple(node) for node in data.get("nodes", [])]
        self.edges = [tuple(edge) for edge in data.get("edges", [])]
        self.is_directed.set(bool(data.get("directed", False)))
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.graph_file = path
        self.log(f"Da tai do thi tu: {path}")

    def save_canvas_postscript(self):
        path = filedialog.asksaveasfilename(
            title="Luu hinh do thi",
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps")],
            initialfile="graph_output.ps",
        )
        if not path:
            return
        self.canvas.postscript(file=path, colormode="color")
        self.log(f"Da luu hinh do thi dang .ps vao: {path}")

    def save_canvas_png(self):
        path = filedialog.asksaveasfilename(
            title="Luu hinh do thi dang PNG",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile="graph_output.png",
        )
        if not path:
            return

        self.root.update_idletasks()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        image = ImageGrab.grab(bbox=(x, y, x1, y1))
        image.save(path)
        self.log(f"Da luu hinh do thi dang .png vao: {path}")

    def _refresh_node_selectors(self):
        values = [str(i) for i in range(len(self.nodes))]
        self.start_combo["values"] = values
        self.end_combo["values"] = [""] + values
        if values:
            if self.start_node_var.get() not in values:
                self.start_node_var.set(values[0])
            if self.end_node_var.get() not in self.end_combo["values"]:
                self.end_node_var.set("")
        else:
            self.start_node_var.set("")
            self.end_node_var.set("")

    def clear_all(self):
        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log("Da xoa toan bo do thi.")

    def load_dijkstra_demo_graph(self):
        self.nodes = [
            (90, 200),
            (240, 90),
            (240, 310),
            (450, 90),
            (450, 310),
            (620, 200),
        ]
        self.edges = [
            (0, 1, 4),
            (0, 2, 5),
            (1, 2, 6),
            (1, 3, 2),
            (1, 4, 7),
            (2, 4, 3),
            (3, 4, 10),
            (3, 5, 8),
            (4, 5, 4),
        ]
        self.is_directed.set(False)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau cho Dijkstra theo hinh a-b-c-d-e-z.\n"
            "Quy uoc nhan: 0=a, 1=b, 2=e, 3=c, 4=d, 5=z.\n"
            "Goi y demo: start=0, end=5."
        )

    def load_kruskal_demo_graph(self):
        self.nodes = [
            (80, 230),
            (190, 110),
            (290, 230),
            (190, 360),
            (540, 110),
            (390, 230),
            (390, 360),
            (630, 230),
        ]
        self.edges = [
            (0, 1, 4),
            (0, 2, 9),
            (0, 3, 5),
            (1, 4, 15),
            (1, 5, 2),
            (2, 3, 2),
            (2, 5, 1),
            (2, 6, 3),
            (3, 6, 7),
            (5, 6, 2),
            (5, 7, 12),
            (6, 7, 7),
            (4, 7, 6),
        ]
        self.is_directed.set(False)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau cho Kruskal theo hinh 2.\n"
            "Quy uoc nhan: 0=V1, 1=V2, 2=V3, 3=V4, 4=V5, 5=V6, 6=V7, 7=V8.\n"
            "Goi y demo: chon Kruskal roi bam Chay thuat toan."
        )

    def load_traversal_demo_graph(self):
        self.nodes = [
            (90, 200),
            (240, 90),
            (240, 310),
            (450, 90),
            (450, 310),
            (620, 200),
        ]
        self.edges = [
            (0, 1, 1),
            (0, 2, 1),
            (1, 3, 1),
            (1, 4, 1),
            (2, 4, 1),
            (3, 5, 1),
            (4, 5, 1),
        ]
        self.is_directed.set(False)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau cho BFS/DFS khao sat trong tai lieu.\n"
            "Goi y demo: chon BFS hoac DFS, dat start=0 va chay hoat hoa."
        )

    def load_bipartite_demo_graph(self):
        self.nodes = [
            (250, 150),
            (450, 150),
            (450, 350),
            (250, 350),
        ]
        self.edges = [
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (3, 0, 1),
        ]
        self.is_directed.set(False)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau C4 (Square) cho khao sat do thi hai phia.\n"
            "Goi y demo: chay Kiem tra do thi 2 phia de xem to mau. Co the ve them mot canh cheo de tao chu trinh le."
        )

    def load_max_flow_demo_graph(self):
        self.nodes = [
            (90, 200),
            (240, 90),
            (240, 310),
            (450, 90),
            (450, 310),
            (620, 200),
        ]
        self.edges = [
            (0, 1, 16),
            (0, 2, 13),
            (1, 2, 10),
            (1, 3, 12),
            (2, 1, 4),
            (2, 4, 14),
            (3, 2, 9),
            (3, 5, 20),
            (4, 3, 7),
            (4, 5, 4),
        ]
        self.is_directed.set(True)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau khao sat Max Flow (co huong).\n"
            "Goi y demo: chon Max Flow, dat start=0, end=5, roi chay hoat hoa."
        )

    def load_euler_demo_graph(self):
        self.nodes = [
            (90, 200),
            (240, 90),
            (240, 310),
            (450, 90),
            (450, 310),
            (620, 200),
        ]
        self.edges = [
            (0, 1, 1),
            (0, 2, 1),
            (1, 2, 1),
            (1, 3, 1),
            (1, 4, 1),
            (2, 3, 1),
            (2, 4, 1),
            (3, 4, 1),
            (3, 5, 1),
            (4, 5, 1),
        ]
        self.is_directed.set(False)
        self.selected_node = None
        self.clear_highlights(redraw=False)
        self._refresh_node_selectors()
        self.redraw()
        self.log(
            "Da nap do thi mau khao sat Chu trinh Euler (tat ca cac dinh deu bac chan).\n"
            "Goi y demo: chon Fleury hoac Hierholzer roi chay hoat hoa."
        )


def main():
    root = tk.Tk()
    app = GraphApp(root)
    app.redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
