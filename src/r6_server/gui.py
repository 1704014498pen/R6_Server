"""tkinter GUI."""

import tkinter as tk
from tkinter import messagebox

from r6_server import __version__, settings
from r6_server.servers import DEFAULT_CODE, build_server_list

FONT = "맑은 고딕"
BG = "#f8f9fa"


class App:
    def __init__(self, root):
        self.root = root
        root.title(f"R6S 서버 매니저 v{__version__}")
        root.geometry("420x700")
        root.minsize(380, 480)
        root.configure(bg=BG)

        # 상단 제목
        top = tk.Frame(root, bg=BG)
        top.pack(side="top", fill="x", pady=(12, 6))
        tk.Label(top, text="레인보우 식스 시즈 서버 선택", font=(FONT, 13, "bold"), bg=BG).pack()
        self.status = tk.Label(top, text="", font=(FONT, 9, "bold"), bg=BG)
        self.status.pack(pady=(2, 0))

        # 하단 저장 버튼을 먼저 고정 (창을 줄여도 안 잘림)
        bottom = tk.Frame(root, bg=BG)
        bottom.pack(side="bottom", fill="x", padx=18, pady=12)
        tk.Button(
            bottom, text="💾 선택한 서버로 저장", font=(FONT, 11, "bold"),
            bg="#0066cc", fg="#ffffff", activebackground="#0052a3", activeforeground="#ffffff",
            height=2, cursor="hand2", command=self.save,
        ).pack(fill="x")

        # 중앙 서버 목록 (스크롤)
        outer = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        outer.pack(side="top", padx=18, pady=4, fill="both", expand=True)
        self.canvas = tk.Canvas(outer, bg="#ffffff", highlightthickness=0)
        bar = tk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.list_frame = tk.Frame(self.canvas, bg="#ffffff")
        win = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(win, width=e.width))
        root.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

        self.selected = tk.StringVar()
        self.buttons = {}
        self.refresh()

    def _build_list(self, current):
        for rb in self.buttons.values():
            rb.destroy()
        self.buttons = {}
        for code, label in build_server_list(settings.parse_hint_codes(), current):
            rb = tk.Radiobutton(
                self.list_frame, text=f"  {label}", variable=self.selected, value=code,
                anchor="w", padx=10, pady=2, selectcolor="#e6f2ff", activebackground="#e9ecef",
            )
            rb.pack(fill="x")
            self.buttons[code] = rb

    def refresh(self):
        current = settings.current_code()
        self._build_list(current)
        self.selected.set(current or DEFAULT_CODE)
        for code, rb in self.buttons.items():
            if code == current:  # 현재 적용된 서버 강조
                rb.config(bg="#cce5ff", fg="#004085", font=(FONT, 10, "bold"))
            else:
                rb.config(bg="#ffffff", fg="#222222", font=(FONT, 10))
        if current is None:
            self.status.config(text="⚠️ 설정 파일 없음 (게임을 1회 이상 실행 필요)", fg="#d9534f")
        else:
            self.status.config(text=f"현재 저장된 서버: {current}", fg="#0052cc")

    def save(self):
        code = self.selected.get()
        if not settings.find_ini_files():
            messagebox.showerror("오류", f"설정 파일을 찾을 수 없습니다.\n경로: {settings.BASE_DIR}")
            return
        try:
            count = settings.apply_to_all(code)
        except OSError as e:
            messagebox.showerror("저장 오류", f"파일 저장 중 오류가 발생했습니다:\n{e}")
            return
        self.refresh()
        messagebox.showinfo(
            "저장 완료",
            f"서버가 [{code}]로 변경되었습니다.\n(적용된 계정: {count}개)\n\n"
            "※ 게임 실행 중이라면 재시작해야 적용됩니다.",
        )


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()
