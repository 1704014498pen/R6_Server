"""tkinter GUI."""

import tkinter as tk
from tkinter import filedialog, messagebox

from r6_server import __version__, paths, settings
from r6_server.servers import DEFAULT_CODE, build_server_list

FONT = "맑은 고딕"
BG = "#f8f9fa"
DISCLAIMER = (
    "비공식 도구 · Ubisoft 와 무관 · 무보증\n"
    "밴·계정 제재를 포함한 모든 결과의 책임은 사용자에게 있습니다"
)


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
        self.status = tk.Label(top, text="", font=(FONT, 9, "bold"), bg=BG, justify="center")
        self.status.pack(pady=(2, 0))

        # 설정 폴더 경로 + 폴더 선택
        path_row = tk.Frame(top, bg=BG)
        path_row.pack(fill="x", padx=18, pady=(4, 0))
        tk.Button(
            path_row, text="📁 폴더 선택", font=(FONT, 9), cursor="hand2", command=self.choose_folder,
        ).pack(side="right")
        self.path_label = tk.Label(path_row, text="", font=(FONT, 8), fg="#666666", bg=BG, anchor="w", justify="left")
        self.path_label.pack(side="left", fill="x", expand=True)
        path_row.bind("<Configure>", lambda e: self.path_label.config(wraplength=max(e.width - 110, 100)))

        # 하단 저장 버튼을 먼저 고정 (창을 줄여도 안 잘림)
        bottom = tk.Frame(root, bg=BG)
        bottom.pack(side="bottom", fill="x", padx=18, pady=12)
        tk.Button(
            bottom, text="💾 선택한 서버로 저장", font=(FONT, 11, "bold"),
            bg="#0066cc", fg="#ffffff", activebackground="#0052a3", activeforeground="#ffffff",
            height=2, cursor="hand2", command=self.save,
        ).pack(fill="x")
        tk.Label(
            bottom, text=DISCLAIMER, font=(FONT, 8), fg="#888888", bg=BG, justify="center",
        ).pack(pady=(6, 0))

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
        base = paths.get_base_dir()
        if current is None:
            self.status.config(
                text="⚠️ 설정 파일을 못 찾았습니다\n게임을 1회 실행하거나, 문서 폴더가 다른 곳이면 [📁 폴더 선택]",
                fg="#d9534f",
            )
            self.path_label.config(text=f"찾아본 위치: {base}")
        else:
            self.status.config(text=f"현재 저장된 서버: {current}", fg="#0052cc")
            self.path_label.config(text=f"설정 폴더: {base}")

    def choose_folder(self):
        picked = filedialog.askdirectory(
            parent=self.root, title="'Rainbow Six - Siege' 폴더(또는 문서 / My Games 폴더)를 고르세요"
        )
        if not picked:
            return
        base = paths.normalize(picked)
        if base is None:
            messagebox.showerror(
                "폴더 오류",
                f"이 폴더에서 GameSettings.ini 를 찾지 못했습니다.\n{picked}\n\n"
                "문서\\My Games\\Rainbow Six - Siege 폴더를 골라 주세요.",
            )
            return
        try:
            paths.save(base)
        except OSError as e:
            messagebox.showwarning("경로 저장 실패", f"다음 실행 때는 다시 골라야 합니다.\n{e}")
        self.refresh()

    def save(self):
        code = self.selected.get()
        if not settings.find_ini_files():
            messagebox.showerror(
                "오류",
                f"설정 파일을 찾을 수 없습니다.\n찾아본 위치: {paths.get_base_dir()}\n\n"
                "게임을 1회 실행했는데도 이 메시지가 나오면 [📁 폴더 선택] 으로 위치를 지정하세요.",
            )
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
