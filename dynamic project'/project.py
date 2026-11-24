import tkinter as tk
from tkinter import messagebox


class BeautifulLCSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("LCS Visualizer")
        self.root.geometry("900x670")
        self.root.minsize(800, 600)

        self.FONT_MAIN = "Century Gothic"

        self.BG_MAIN = "#1A1528"
        self.BG_CARD = "#262038"
        self.BG_BORDER = "#3E3557"
        self.TEXT_MAIN = "#F5EBF7"
        self.TEXT_MUTED = "#A89CB8"

        self.CLR_ACTIVE = "#FFD43B"
        self.CLR_MATCH = "#51CF66"
        self.CLR_MISMATCH = "#4DABF7"
        self.CLR_PATH = "#CC5DE8"
        self.CLR_LCS_CHAR = "#FF6B8B"
        self.CLR_S1 = "#FF7597"
        self.CLR_S2 = "#B197FC"

        self.root.configure(bg=self.BG_MAIN)

        self.s1 = "STONE"
        self.s2 = "SHOE"
        self.i = 1
        self.j = 1
        self.is_playing = False
        self.backtracking = False
        self.bt_i = 0
        self.bt_j = 0
        self.lcs_chars = []

        self._build_ui()
        self.reset()

    def _build_ui(self):
        top_bar = tk.Frame(self.root, bg=self.BG_CARD, padx=15, pady=10, bd=1, relief="solid")
        top_bar.pack(fill="x", padx=12, pady=(10, 5))

        tk.Label(
            top_bar, text=" LCS Visualizer",
            font=(self.FONT_MAIN, 13, "bold"), bg=self.BG_CARD, fg=self.CLR_S1
        ).pack(side="left", padx=(0, 20))

        tk.Label(top_bar, text="String 1:", bg=self.BG_CARD, fg=self.CLR_S1, font=(self.FONT_MAIN, 10, "bold")).pack(side="left", padx=(0, 4))
        self.entry_s1 = tk.Entry(top_bar, width=9, font=(self.FONT_MAIN, 11, "bold"), bg="#141021", fg=self.CLR_S1,
                                 insertbackground="white", bd=1, relief="solid")
        self.entry_s1.insert(0, self.s1)
        self.entry_s1.pack(side="left", padx=(0, 15))

        tk.Label(top_bar, text="String 2:", bg=self.BG_CARD, fg=self.CLR_S2, font=(self.FONT_MAIN, 10, "bold")).pack(side="left", padx=(0, 4))
        self.entry_s2 = tk.Entry(top_bar, width=9, font=(self.FONT_MAIN, 11, "bold"), bg="#141021", fg=self.CLR_S2,
                                 insertbackground="white", bd=1, relief="solid")
        self.entry_s2.insert(0, self.s2)
        self.entry_s2.pack(side="left", padx=(0, 15))

        tk.Button(top_bar, text="✔ Apply", bg="#D6336C", fg="white", font=(self.FONT_MAIN, 9, "bold"),
                  activebackground="#C2255C", activeforeground="white", relief="flat", padx=12, pady=3,
                  command=self.set_strings).pack(side="left", padx=4)

        tk.Button(top_bar, text="🔄 Reset", bg="#FA5252", fg="white", font=(self.FONT_MAIN, 9, "bold"),
                  activebackground="#E03131", activeforeground="white", relief="flat", padx=12, pady=3,
                  command=self.reset).pack(side="left", padx=4)

        ctrl_bar = tk.Frame(self.root, bg=self.BG_MAIN, pady=4)
        ctrl_bar.pack(fill="x", padx=12)

        self.btn_next = tk.Button(ctrl_bar, text="⏭ Next Step", bg="#51CF66", fg="#141021",
                                  font=(self.FONT_MAIN, 10, "bold"), relief="flat", padx=14, pady=4,
                                  command=self.next_step)
        self.btn_next.pack(side="left", padx=(0, 6))

        self.btn_play = tk.Button(ctrl_bar, text="▶ Auto Play", bg="#FFD43B", fg="#141021",
                                  font=(self.FONT_MAIN, 10, "bold"), relief="flat", padx=14, pady=4,
                                  command=self.toggle_play)
        self.btn_play.pack(side="left", padx=(0, 12))

        tk.Label(ctrl_bar, text="Speed:", bg=self.BG_MAIN, fg=self.TEXT_MUTED, font=(self.FONT_MAIN, 9, "bold")).pack(side="left", padx=(0, 4))
        self.speed_slider = tk.Scale(ctrl_bar, from_=100, to=1000, orient="horizontal", bg=self.BG_MAIN,
                                     fg=self.TEXT_MAIN, highlightthickness=0, length=100, showvalue=False)
        self.speed_slider.set(380)
        self.speed_slider.pack(side="left", padx=(0, 15))

        legend_frame = tk.Frame(ctrl_bar, bg=self.BG_MAIN)
        legend_frame.pack(side="right")
        self._add_legend(legend_frame, "Active", self.CLR_ACTIVE, "#141021")
        self._add_legend(legend_frame, "Match", self.CLR_MATCH, "#141021")
        self._add_legend(legend_frame, "Mismatch", self.CLR_MISMATCH, "#FFFFFF")
        self._add_legend(legend_frame, "LCS Path", self.CLR_PATH, "#FFFFFF")

        self.table_card = tk.Frame(self.root, bg=self.BG_CARD, bd=1, relief="solid")
        self.table_card.pack(expand=True, padx=12, pady=6)

        info_card = tk.Frame(self.root, bg=self.BG_CARD, padx=15, pady=8, bd=1, relief="solid")
        info_card.pack(fill="x", padx=12, pady=5)

        self.info_lbl = tk.Label(
            info_card, text="Click 'Next Step' or 'Auto Play' to begin calculation.",
            font=(self.FONT_MAIN, 10, "bold"), bg=self.BG_CARD, fg=self.TEXT_MAIN, anchor="w"
        )
        self.info_lbl.pack(fill="x")

        self.formula_lbl = tk.Label(
            info_card, text="dp[i][j] = 1 + dp[i-1][j-1] (Match)  OR  max(top, left) (Mismatch)",
            font=(self.FONT_MAIN, 11, "bold"), bg="#141021", fg="#FFD43B", pady=5, relief="solid", bd=1
        )
        self.formula_lbl.pack(fill="x", pady=(4, 0))

        status_bar = tk.Frame(self.root, bg="#141021", padx=15, pady=8, bd=1, relief="solid")
        status_bar.pack(fill="x", side="bottom")

        self.status_lbl = tk.Label(status_bar, text="Status: Ready", bg="#141021", fg=self.TEXT_MUTED, font=(self.FONT_MAIN, 9, "bold"))
        self.status_lbl.pack(side="left")

        self.result_lbl = tk.Label(status_bar, text="✨ LCS: --  |  Length: 0", font=(self.FONT_MAIN, 11, "bold"),
                                   bg="#141021", fg=self.CLR_S1)
        self.result_lbl.pack(side="right")

    def _add_legend(self, parent, text, bg, fg):
        lbl = tk.Label(parent, text=f" {text} ", bg=bg, fg=fg, font=(self.FONT_MAIN, 8, "bold"), relief="solid", bd=1)
        lbl.pack(side="left", padx=3)

    def set_strings(self):
        s1 = self.entry_s1.get().strip().upper()
        s2 = self.entry_s2.get().strip().upper()
        if not s1 or not s2:
            messagebox.showwarning("Warning", "Both strings must contain at least 1 character.")
            return
        if len(s1) > 10 or len(s2) > 10:
            messagebox.showwarning("Warning", "For optimal display, keep strings <= 10 letters.")
            return
        self.s1, self.s2 = s1, s2
        self.reset()

    def reset(self):
        self.is_playing = False
        self.btn_play.config(text="▶ Auto Play", bg="#FFD43B", fg="#141021")
        self.i, self.j = 1, 1
        self.backtracking = False
        self.bt_i, self.bt_j = len(self.s1), len(self.s2)
        self.lcs_chars = []

        m, n = len(self.s1), len(self.s2)
        self.dp = [[0] * (n + 1) for _ in range(m + 1)]

        for w in self.table_card.winfo_children():
            w.destroy()

        self.cells = {}

        tk.Label(self.table_card, text="", width=5, bg="#141021").grid(row=0, column=0, padx=2, pady=2)
        tk.Label(self.table_card, text="∅", width=5, bg="#2F2746", fg=self.CLR_S2, font=(self.FONT_MAIN, 11, "bold")).grid(row=0, column=1, padx=2, pady=2)

        for col, ch in enumerate(self.s2):
            lbl = tk.Label(self.table_card, text=ch, width=5, bg="#2F2746", fg=self.CLR_S2, font=(self.FONT_MAIN, 12, "bold"))
            lbl.grid(row=0, column=col + 2, padx=2, pady=2)
            self.cells[("col_head", col + 1)] = lbl

        for r in range(m + 1):
            row_txt = "∅" if r == 0 else self.s1[r - 1]
            lbl = tk.Label(self.table_card, text=row_txt, width=5, bg="#2F2746", fg=self.CLR_S1, font=(self.FONT_MAIN, 12, "bold"))
            lbl.grid(row=r + 1, column=0, padx=2, pady=2)
            if r > 0:
                self.cells[("row_head", r)] = lbl

            for c in range(n + 1):
                val = "0" if (r == 0 or c == 0) else ""
                bg = "#191424" if (r == 0 or c == 0) else self.BG_CARD
                fg = self.TEXT_MUTED if (r == 0 or c == 0) else self.TEXT_MAIN
                cell = tk.Label(self.table_card, text=val, width=5, height=2, bg=bg, fg=fg,
                                relief="solid", bd=1, font=(self.FONT_MAIN, 12, "bold"))
                cell.grid(row=r + 1, column=c + 1, padx=2, pady=2)
                self.cells[(r, c)] = cell

        self.info_lbl.config(text="Ready to start. Press 'Next Step' or 'Auto Play'.")
        self.formula_lbl.config(text="dp[i][j] = 1 + dp[i-1][j-1] (Match)  OR  max(top, left) (Mismatch)")
        self.status_lbl.config(text="Status: Ready")
        self.result_lbl.config(text="✨ LCS: --  |  Length: 0")

    def next_step(self):
        m, n = len(self.s1), len(self.s2)

        if not self.backtracking:
            self._restore_colors()

            i, j = self.i, self.j
            c1 = self.s1[i - 1]
            c2 = self.s2[j - 1]

            self.cells[("row_head", i)].config(bg=self.CLR_ACTIVE, fg="#141021")
            self.cells[("col_head", j)].config(bg=self.CLR_ACTIVE, fg="#141021")

            if c1 == c2:
                self.dp[i][j] = 1 + self.dp[i - 1][j - 1]
                self.cells[(i - 1, j - 1)].config(bg=self.CLR_MATCH, fg="#141021")
                self.cells[(i, j)].config(text=str(self.dp[i][j]), bg=self.CLR_ACTIVE, fg="#141021")
                self.info_lbl.config(text=f"Match! '{c1}' == '{c2}' ➔ Add 1 to diagonal cell dp[{i-1}][{j-1}] ({self.dp[i-1][j-1]})")
                self.formula_lbl.config(text=f"dp[{i}][{j}] = 1 + dp[{i-1}][{j-1}] = 1 + {self.dp[i-1][j-1]} = {self.dp[i][j]}")
            else:
                top = self.dp[i - 1][j]
                left = self.dp[i][j - 1]
                self.dp[i][j] = max(top, left)
                self.cells[(i - 1, j)].config(bg=self.CLR_MISMATCH, fg="#FFFFFF")
                self.cells[(i, j - 1)].config(bg=self.CLR_MISMATCH, fg="#FFFFFF")
                self.cells[(i, j)].config(text=str(self.dp[i][j]), bg=self.CLR_ACTIVE, fg="#141021")
                self.info_lbl.config(text=f"Mismatch ('{c1}' != '{c2}') ➔ Take max(top={top}, left={left})")
                self.formula_lbl.config(text=f"dp[{i}][{j}] = max(top={top}, left={left}) = {self.dp[i][j]}")

            self.status_lbl.config(text=f"Status: Computing cell dp[{i}][{j}]")

            self.j += 1
            if self.j > n:
                self.j = 1
                self.i += 1

            if self.i > m:
                self.backtracking = True
                self.bt_i, self.bt_j = m, n
                self.status_lbl.config(text="Status: DP Table Complete! Beginning Backtracking...")

        else:
            if self.bt_i > 0 and self.bt_j > 0:
                i, j = self.bt_i, self.bt_j
                c1 = self.s1[i - 1]
                c2 = self.s2[j - 1]

                if c1 == c2:
                    self.cells[(i, j)].config(bg=self.CLR_LCS_CHAR, fg="#FFFFFF")
                    self.lcs_chars.append(c1)
                    curr = "".join(reversed(self.lcs_chars))
                    self.info_lbl.config(text=f"Backtracking: Match ('{c1}'). Included in LCS! Move diagonally up-left.")
                    self.formula_lbl.config(text=f"LCS so far: \"{curr}\" (adding '{c1}')")
                    self.result_lbl.config(text=f"✨ LCS: \"{curr}\"  |  Length: {len(self.lcs_chars)}")
                    self.bt_i -= 1
                    self.bt_j -= 1
                elif self.dp[i - 1][j] >= self.dp[i][j - 1]:
                    self.cells[(i, j)].config(bg=self.CLR_PATH, fg="#FFFFFF")
                    self.info_lbl.config(text="Backtracking: Top >= Left ➔ Move UP to cell.")
                    self.formula_lbl.config(text=f"Moving Up: top value ({self.dp[i-1][j]}) >= left value ({self.dp[i][j-1]})")
                    self.bt_i -= 1
                else:
                    self.cells[(i, j)].config(bg=self.CLR_PATH, fg="#FFFFFF")
                    self.info_lbl.config(text="Backtracking: Left > Top ➔ Move LEFT to cell.")
                    self.formula_lbl.config(text=f"Moving Left: left value ({self.dp[i][j-1]}) > top value ({self.dp[i-1][j]})")
                    self.bt_j -= 1
            else:
                self.cells[(0, 0)].config(bg=self.CLR_PATH, fg="#FFFFFF")
                final_lcs = "".join(reversed(self.lcs_chars))
                self.info_lbl.config(text=f"Backtracking finished! Optimal LCS: \"{final_lcs}\"")
                self.formula_lbl.config(text=f"Final Result: Length = {len(final_lcs)}  |  LCS = \"{final_lcs}\"")
                self.result_lbl.config(text=f"🎉 Final LCS: \"{final_lcs}\"  |  Length: {len(final_lcs)}")
                self.status_lbl.config(text="Status: Completed successfully! ✨")
                self.is_playing = False
                self.btn_play.config(text="▶ Auto Play", bg="#FFD43B", fg="#141021")
                return False

        return True

    def _restore_colors(self):
        for (r, c), cell in self.cells.items():
            if r == "row_head" or r == "col_head":
                cell.config(bg="#2F2746", fg=self.CLR_S1 if r == "row_head" else self.CLR_S2)
            elif isinstance(r, int) and isinstance(c, int):
                if (r == 0 or c == 0):
                    cell.config(bg="#191424", fg=self.TEXT_MUTED)
                elif cell.cget("text") != "":
                    cell.config(bg=self.BG_CARD, fg=self.TEXT_MAIN)

    def toggle_play(self):
        if self.is_playing:
            self.is_playing = False
            self.btn_play.config(text="▶ Auto Play", bg="#FFD43B", fg="#141021")
        else:
            self.is_playing = True
            self.btn_play.config(text="⏸ Pause", bg="#FA5252", fg="white")
            self._loop()

    def _loop(self):
        if self.is_playing:
            if self.next_step():
                self.root.after(self.speed_slider.get(), self._loop)
            else:
                self.is_playing = False
                self.btn_play.config(text="▶ Auto Play", bg="#FFD43B", fg="#141021")


if __name__ == "__main__":
    root = tk.Tk()
    app = BeautifulLCSVisualizer(root)
    root.mainloop()
