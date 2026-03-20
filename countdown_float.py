"""
悬浮倒计时器 - 细长条透明版
从15分02秒开始，无声音，最后10秒变红
"""

import tkinter as tk
import time
import threading

TOTAL_SECONDS = 15 * 60 + 2  # 15分02秒

class FloatingTimer:
    def __init__(self):
        self.remaining = TOTAL_SECONDS
        self.running = True
        self.paused = False

        self.root = tk.Tk()
        self.root.title("")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.55)
        self.root.configure(bg="#000000")
        self.root.attributes("-transparentcolor", "#000000")

        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"168x32+{sw - 184}+14")

        self._drag_x = 0
        self._drag_y = 0
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        self.frame = tk.Frame(
            self.root, bg="#0d0d14", bd=0,
            highlightthickness=1,
            highlightbackground="#252535"
        )
        self.frame.pack(fill="both", expand=True)

        # 时间数字 —— 可拖动、双击关闭
        self.var_time = tk.StringVar(value="15:02")
        self.label_time = tk.Label(
            self.frame, textvariable=self.var_time,
            bg="#0d0d14", fg="#e8c060",
            font=("Consolas", 16, "bold"),
            padx=8, pady=0
        )
        self.label_time.pack(side="left")
        self.label_time.bind("<ButtonPress-1>",   self._on_drag_start)
        self.label_time.bind("<B1-Motion>",       self._on_drag_move)
        self.label_time.bind("<Double-Button-1>", lambda e: self._quit())

        self.frame.bind("<ButtonPress-1>",   self._on_drag_start)
        self.frame.bind("<B1-Motion>",       self._on_drag_move)
        self.frame.bind("<Double-Button-1>", lambda e: self._quit())

        # 暂停按钮
        self.btn_pause = tk.Label(
            self.frame, text="⏸",
            bg="#0d0d14", fg="#555570",
            font=("Arial", 12), padx=5,
            cursor="hand2"
        )
        self.btn_pause.pack(side="left")
        self.btn_pause.bind("<ButtonRelease-1>", lambda e: self._toggle_pause())

        # 重置按钮
        self.btn_reset = tk.Label(
            self.frame, text="↺",
            bg="#0d0d14", fg="#555570",
            font=("Arial", 12), padx=5,
            cursor="hand2"
        )
        self.btn_reset.pack(side="left")
        self.btn_reset.bind("<ButtonRelease-1>", lambda e: self._reset())

        # 启动倒计时
        self.thread = threading.Thread(target=self._tick_loop, daemon=True)
        self.thread.start()

    def _tick_loop(self):
        while self.running:
            time.sleep(1)
            if self.paused or not self.running:
                continue
            if self.remaining > 0:
                self.remaining -= 1
                self.root.after(0, self._update_display)
            else:
                self.root.after(0, self._on_finish)
                break

    def _update_display(self):
        m = self.remaining // 60
        s = self.remaining % 60
        self.var_time.set(f"{m:02d}:{s:02d}")
        # 最后10秒变红，其余金色
        self.label_time.config(
            fg="#e05050" if self.remaining <= 10 else "#e8c060"
        )

    def _on_finish(self):
        self.var_time.set("00:00")
        self.label_time.config(fg="#e05050")

    def _toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.config(text="▶" if self.paused else "⏸")

    def _reset(self):
        self.paused = False
        self.remaining = TOTAL_SECONDS
        self.var_time.set("15:02")
        self.label_time.config(fg="#e8c060")
        self.btn_pause.config(text="⏸")

    def _on_drag_start(self, event):
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _on_drag_move(self, event):
        self.root.geometry(
            f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}"
        )

    def _quit(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    FloatingTimer()
