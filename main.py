import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class BrotatoArchiveModifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Brotato Archive Modifier")
        self.root.geometry("640x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f9")

        # 多语言字典
        self.lang = "en"
        self.text = {
            "en": {
                "title": "Brotato Archive Modifier",
                "author": "Powered by Kingrzkx",
                "select": "Select run_v3_0.json",
                "save": "SAVE CHANGES",
                "success_load": "Archive loaded successfully.",
                "success_save": "All values saved correctly.\n1:1 matched in-game.",
                "error_no_file": "Please load an archive first.",
                "error_load": "Failed to load archive.",
                "error_save": "Save failed:",
                "gold": "Gold",
                "level": "Level",
                "max_hp": "Max Health",
                "area": "Area",
                "engineer": "Engineering",
                "dmg": "Damage %",
                "speed": "Move Speed %",
                "cost": "Item Cost",
                "heal": "Consumable Heal",
                "switch": "中文"
            },
            "cn": {
                "title": "Brotato 存档修改器",
                "author": "作者：Kingrzkx",
                "select": "选择 run_v3_0.json",
                "save": "保存修改",
                "success_load": "存档加载成功！",
                "success_save": "修改已保存！\n所有属性 1:1 游戏内生效！",
                "error_no_file": "请先选择存档！",
                "error_load": "存档加载失败！",
                "error_save": "保存失败：",
                "gold": "金币",
                "level": "等级",
                "max_hp": "最大生命值",
                "area": "范围",
                "engineer": "工程学",
                "dmg": "伤害百分比",
                "speed": "移动速度百分比",
                "cost": "道具价格",
                "heal": "消耗品治疗",
                "switch": "English"
            }
        }

        self.data = None
        self.path = ""
        self.entries = {}
        self.widgets = {}

        # 界面样式
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background="#f0f4f9")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 10), background="#f0f4f9")
        self.style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), background="#3498db", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#2980b9")])

        # ---------- 界面开始 ----------
        # 顶部语言切换按钮
        self.lang_btn = ttk.Button(root, text=self.text[self.lang]["switch"], command=self.switch_lang)
        self.lang_btn.pack(pady=5, anchor="ne", padx=20)

        # 标题
        self.title_label = ttk.Label(root, text=self.text[self.lang]["title"], style="Title.TLabel")
        self.title_label.pack(pady=2)

        self.author_label = ttk.Label(root, text=self.text[self.lang]["author"], style="Sub.TLabel")
        self.author_label.pack(pady=0)

        # 选择文件按钮
        self.file_btn = ttk.Button(root, text=self.text[self.lang]["select"], style="Accent.TButton", command=self.load_file)
        self.file_btn.pack(pady=10)

        # 输入面板
        self.panel = tk.Frame(root, bg="white", bd=1, relief="solid")
        self.panel.pack(pady=5, padx=30, fill="both", expand=True)

        # 属性列表
        self.fields = [
            (self.text[self.lang]["gold"], "gold"),
            (self.text[self.lang]["level"], "current_level"),
            (self.text[self.lang]["max_hp"], "1880215261"),
            (self.text[self.lang]["area"], "453346765"),
            (self.text[self.lang]["engineer"], "4033990219"),
            (self.text[self.lang]["dmg"], "475911951"),
            (self.text[self.lang]["speed"], "455061873"),
            (self.text[self.lang]["cost"], "2055766425"),
            (self.text[self.lang]["heal"], "857480423"),
        ]

        self.key_order = ["gold", "current_level", "1880215261", "453346765", "4033990219",
                          "475911951", "455061873", "2055766425", "857480423"]

        self.create_fields()

        # 保存按钮
        self.save_btn = ttk.Button(root, text=self.text[self.lang]["save"], style="Accent.TButton", command=self.save)
        self.save_btn.pack(pady=15)

    def create_fields(self):
        # 清空旧组件
        for widget in self.panel.winfo_children():
            widget.destroy()

        self.label_refs = []
        self.entries = {}

        # 重新生成
        keys = self.key_order
        labels = [
            self.text[self.lang]["gold"],
            self.text[self.lang]["level"],
            self.text[self.lang]["max_hp"],
            self.text[self.lang]["area"],
            self.text[self.lang]["engineer"],
            self.text[self.lang]["dmg"],
            self.text[self.lang]["speed"],
            self.text[self.lang]["cost"],
            self.text[self.lang]["heal"],
        ]

        for label_text, key in zip(labels, keys):
            row = tk.Frame(self.panel, bg="white")
            row.pack(fill="x", padx=20, pady=8)

            lbl = tk.Label(row, text=label_text, width=18, anchor="w", font=("Segoe UI", 11), bg="white")
            lbl.pack(side="left")
            self.label_refs.append(lbl)

            entry = ttk.Entry(row, font=("Segoe UI", 10), justify="center")
            entry.insert(0, "100")
            entry.pack(side="right", fill="x", expand=True)
            self.entries[key] = entry

    def switch_lang(self):
        # 切换语言
        self.lang = "cn" if self.lang == "en" else "en"
        tx = self.text[self.lang]

        self.title_label.config(text=tx["title"])
        self.author_label.config(text=tx["author"])
        self.file_btn.config(text=tx["select"])
        self.save_btn.config(text=tx["save"])
        self.lang_btn.config(text=tx["switch"])

        self.create_fields()

    def load_file(self):
        self.path = filedialog.askopenfilename(filetypes=[("JSON Archive", "*.json")])
        if not self.path:
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            messagebox.showinfo(self.text[self.lang]["success_load"].split()[0], self.text[self.lang]["success_load"])
        except:
            messagebox.showerror("Error", self.text[self.lang]["error_load"])

    def save(self):
        if not self.data:
            messagebox.showerror("Error", self.text[self.lang]["error_no_file"])
            return

        try:
            run = self.data["current_run_state"]
            p = run["players_data"][0]
            fx = p["effects"]

            p["gold"] = int(self.entries["gold"].get())
            p["current_level"] = int(self.entries["current_level"].get())

            for k in self.key_order[2:]:
                fx[k] = int(self.entries[k].get())

            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)

            messagebox.showinfo("Success", self.text[self.lang]["success_save"])
        except Exception as e:
            messagebox.showerror("Error", f"{self.text[self.lang]['error_save']}\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BrotatoArchiveModifier(root)
    root.mainloop()