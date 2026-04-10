import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


# ══════════════════════════════════════════════
#  DATA LAYER
# ══════════════════════════════════════════════

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age


class Student(Person):
    def __init__(self, name, age, student_id, courses: dict):
        super().__init__(name, age)
        self.student_id = student_id
        self.courses    = courses
        self.GPA        = self._calc_gpa()

    def add_course(self, course_name, grade):
        self.courses[course_name] = grade
        self.GPA = self._calc_gpa()

    def edit_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name] = grade
            self.GPA = self._calc_gpa()
            return True
        return False

    def delete_course(self, course_name):
        if course_name in self.courses:
            del self.courses[course_name]
            self.GPA = self._calc_gpa()
            return True
        return False

    def _calc_gpa(self):
        if not self.courses:
            return 0.0
        return sum(self.courses.values()) / len(self.courses)


class SystemManagement:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def delete_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                return True
        return False

    def find_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def top_students(self, n=3):
        return sorted(self.students, key=lambda s: s.GPA, reverse=True)[:n]


# ══════════════════════════════════════════════
#  UNIVERSITY PORTAL THEME
# ══════════════════════════════════════════════

NAVY        = "#1B3A6B"
NAVY_DARK   = "#122952"
NAVY_LIGHT  = "#2B5299"
WHITE       = "#FFFFFF"
OFF_WHITE   = "#F4F6FA"
BORDER      = "#D0D8E8"
BORDER_DARK = "#B0BDD4"
GOLD        = "#C8963E"
GOLD_LIGHT  = "#F5E6C8"
SUCCESS     = "#2E7D4F"
SUCCESS_BG  = "#E8F5EE"
DANGER      = "#B02A2A"
DANGER_BG   = "#FDEAEA"
WARNING     = "#8A6200"
WARNING_BG  = "#FFF8E1"
TEXT        = "#1A1F36"
SUBTEXT     = "#5A6580"
MUTED       = "#9AA3B8"

FONT_TITLE  = ("Georgia",   16, "bold")
FONT_H2     = ("Segoe UI",  11, "bold")
FONT_BODY   = ("Segoe UI",  10)
FONT_SMALL  = ("Segoe UI",   9)
FONT_LABEL  = ("Segoe UI",  10, "bold")
FONT_NAV    = ("Segoe UI",  10)


# ══════════════════════════════════════════════
#  REUSABLE WIDGETS
# ══════════════════════════════════════════════

def primary_button(parent, text, command, width=18):
    return tk.Button(parent, text=text, command=command,
        bg=NAVY, fg=WHITE, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground=NAVY_DARK, activeforeground=WHITE,
        padx=14, pady=7, width=width, bd=0)


def secondary_button(parent, text, command, width=16):
    return tk.Button(parent, text=text, command=command,
        bg=WHITE, fg=NAVY, font=("Segoe UI", 10),
        relief="flat", cursor="hand2",
        activebackground=OFF_WHITE, activeforeground=NAVY_DARK,
        padx=12, pady=6, width=width, bd=1,
        highlightthickness=1, highlightbackground=NAVY)


def danger_button(parent, text, command, width=16):
    return tk.Button(parent, text=text, command=command,
        bg=DANGER, fg=WHITE, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground="#8B1A1A", activeforeground=WHITE,
        padx=12, pady=7, width=width, bd=0)


def success_button(parent, text, command, width=18):
    return tk.Button(parent, text=text, command=command,
        bg=SUCCESS, fg=WHITE, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground="#1F5C38", activeforeground=WHITE,
        padx=14, pady=7, width=width, bd=0)


def portal_entry(parent, placeholder="", width=28):
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var,
        bg=WHITE, fg=TEXT, insertbackground=NAVY,
        font=FONT_BODY, relief="flat", bd=0, width=width,
        highlightthickness=1, highlightbackground=BORDER_DARK,
        highlightcolor=NAVY)
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg=MUTED)
        def on_in(ev):
            if e.get() == placeholder:
                e.delete(0, tk.END); e.config(fg=TEXT)
        def on_out(ev):
            if e.get() == "":
                e.insert(0, placeholder); e.config(fg=MUTED)
        e.bind("<FocusIn>", on_in)
        e.bind("<FocusOut>", on_out)
    return e, var


def page_title(parent, text, bg=OFF_WHITE):
    return tk.Label(parent, text=text, bg=bg, fg=NAVY, font=FONT_TITLE, anchor="w")


def section_header(parent, text, bg=OFF_WHITE):
    return tk.Label(parent, text=text, bg=bg, fg=TEXT, font=FONT_H2, anchor="w")


def field_label(parent, text, bg=OFF_WHITE):
    return tk.Label(parent, text=text, bg=bg, fg=SUBTEXT, font=FONT_LABEL, anchor="w")


def h_rule(parent, bg=BORDER):
    return tk.Frame(parent, bg=bg, height=1)


def gpa_colors(gpa):
    if gpa >= 90: return SUCCESS, SUCCESS_BG
    if gpa >= 75: return NAVY_LIGHT, "#E8EEFA"
    if gpa >= 60: return WARNING, WARNING_BG
    return DANGER, DANGER_BG


def standing(gpa):
    if gpa >= 90: return "Distinction"
    if gpa >= 80: return "Merit"
    if gpa >= 70: return "Good Standing"
    if gpa >= 60: return "Pass"
    return "At Risk"


def letter_grade(g):
    if g >= 90: return "A"
    if g >= 80: return "B"
    if g >= 70: return "C"
    if g >= 60: return "D"
    return "F"


# ══════════════════════════════════════════════
#  ADD COURSE DIALOG
# ══════════════════════════════════════════════

class AddCourseDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Course")
        self.configure(bg=OFF_WHITE)
        self.resizable(False, False)
        self.result = None
        self._build()
        self.grab_set()
        self.wait_window()

    def _build(self):
        hdr = tk.Frame(self, bg=NAVY, height=38)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  Add New Course", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=12, pady=8)

        body = tk.Frame(self, bg=OFF_WHITE)
        body.pack(padx=24, pady=20)

        field_label(body, "Course Name").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.e_c, _ = portal_entry(body, "e.g. Calculus I", width=24)
        self.e_c.grid(row=1, column=0, ipady=5, pady=(0, 12))

        field_label(body, "Grade (0–100)").grid(row=2, column=0, sticky="w", pady=(0, 4))
        self.e_g, _ = portal_entry(body, "e.g. 87", width=24)
        self.e_g.grid(row=3, column=0, ipady=5, pady=(0, 16))

        row = tk.Frame(body, bg=OFF_WHITE)
        row.grid(row=4, column=0, sticky="ew")
        success_button(row, "Add Course", self._submit, width=14).pack(side="left", padx=(0, 8))
        secondary_button(row, "Cancel", self.destroy, width=10).pack(side="left")

    def _submit(self):
        name  = self.e_c.get().strip()
        grade = self.e_g.get().strip()
        placeholders = {"e.g. Calculus I", "e.g. 87", ""}
        if name in placeholders or grade in placeholders:
            messagebox.showerror("Error", "Please fill in all fields.", parent=self)
            return
        try:
            grade = float(grade)
        except ValueError:
            messagebox.showerror("Error", "Grade must be a number.", parent=self)
            return
        self.result = (name, grade)
        self.destroy()


# ══════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Student Portal")
        self.geometry("1160x720")
        self.minsize(980, 640)
        self.configure(bg=OFF_WHITE)
        self.system = SystemManagement()
        self._seed()
        self._build_ui()

    def _seed(self):
        s1 = Student("Alice Johnson",  20, "S001", {"Calculus I": 88, "Physics":    82, "Programming": 95})
        s2 = Student("Bob Martinez",   22, "S002", {"Chemistry":  90, "Biology":    87, "Statistics":  79})
        s3 = Student("Carol Chen",     21, "S003", {"Circuits":   94, "Signals":    88, "Control Sys": 91})
        for s in (s1, s2, s3): self.system.add_student(s)

    # ─── top-level layout ─────────────────────
    def _build_ui(self):
        self._build_topbar()
        body = tk.Frame(self, bg=OFF_WHITE)
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)
        self._build_main_area(body)

    # ─── topbar ───────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self, bg=NAVY, height=54)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # gold accent strip
        tk.Frame(bar, bg=GOLD, width=5).pack(side="left", fill="y")

        tk.Label(bar, text="  🎓 UniPortal",
                 bg=NAVY, fg=WHITE, font=("Georgia", 13, "bold")).pack(side="left")
        tk.Label(bar, text="  Student Information System",
                 bg=NAVY, fg="#A8BDD8", font=("Segoe UI", 9)).pack(side="left", pady=17)

        # enrolled count box
        count_box = tk.Frame(bar, bg=NAVY_DARK)
        count_box.pack(side="right", fill="y")
        tk.Label(count_box, text="ENROLLED", bg=NAVY_DARK, fg=GOLD,
                 font=("Segoe UI", 7, "bold")).pack(padx=18, pady=(8, 0))
        self.count_var = tk.StringVar()
        self._refresh_count()
        tk.Label(count_box, textvariable=self.count_var, bg=NAVY_DARK, fg=WHITE,
                 font=("Georgia", 14, "bold")).pack(padx=18, pady=(0, 8))

        tk.Label(bar, text="Spring 2025  ", bg=NAVY, fg="#A8BDD8",
                 font=("Segoe UI", 9)).pack(side="right")

    def _refresh_count(self):
        self.count_var.set(str(len(self.system.students)))

    # ─── sidebar ──────────────────────────────
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=NAVY_DARK, width=215)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="MAIN MENU", bg=NAVY_DARK, fg=GOLD,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(18, 6))

        nav = [
            ("🏠   Dashboard",        self._show_all),
            ("➕   Enroll Student",   self._show_add),
            ("🔍   Search Records",   self._show_search),
            ("✏️    Edit Student",     self._show_edit),
            ("🗑️    Remove Student",   self._show_delete),
            ("🏆   Honours Board",    self._show_top),
        ]
        self._nav_btns = []
        for lbl, fn in nav:
            b = tk.Button(sb, text=lbl, bg=NAVY_DARK, fg="#C8D8F0",
                          font=FONT_NAV, relief="flat", anchor="w",
                          cursor="hand2", padx=18, pady=10, bd=0,
                          activebackground=NAVY, activeforeground=WHITE)
            b.pack(fill="x")
            self._nav_btns.append((b, fn))

        def make(b, fn):
            def cmd():
                self._highlight_nav(b); fn()
            return cmd

        for b, fn in self._nav_btns:
            b.config(command=make(b, fn))

        self._highlight_nav(self._nav_btns[0][0])

        # help box at bottom
        tk.Frame(sb, bg=NAVY_DARK).pack(fill="both", expand=True)
        hb = tk.Frame(sb, bg="#162444", padx=12, pady=10)
        hb.pack(fill="x", padx=10, pady=14)
        tk.Label(hb, text="ℹ  Tip", bg="#162444", fg=GOLD,
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(anchor="w")
        tk.Label(hb, text="Double-click any row\nto manage that student's\ncourse records.",
                 bg="#162444", fg="#8BA0C4", font=("Segoe UI", 8),
                 justify="left").pack(anchor="w", pady=(4, 0))

    def _highlight_nav(self, active):
        for b, _ in self._nav_btns:
            b.config(bg=NAVY_DARK, fg="#C8D8F0")
        active.config(bg=NAVY, fg=WHITE)

    # ─── main content area ────────────────────
    def _build_main_area(self, parent):
        # breadcrumb strip
        bc = tk.Frame(parent, bg=WHITE,
                      highlightthickness=1, highlightbackground=BORDER)
        bc.pack(fill="x")
        self.bc_var = tk.StringVar(value="Home  ›  Dashboard")
        tk.Label(bc, textvariable=self.bc_var, bg=WHITE, fg=SUBTEXT,
                 font=("Segoe UI", 9), padx=20, pady=6).pack(side="left")

        self.main = tk.Frame(parent, bg=OFF_WHITE)
        self.main.pack(fill="both", expand=True)
        self._show_all()

    def _clear(self):
        for w in self.main.winfo_children(): w.destroy()

    def _bc(self, path):
        self.bc_var.set(f"Home  ›  {path}")

    # ══════════════════════════════════════════
    #  TREEVIEW STYLE (shared)
    # ══════════════════════════════════════════
    def _apply_tree_style(self, name="Portal.Treeview", heading_bg=NAVY):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(name,
            background=WHITE, foreground=TEXT,
            fieldbackground=WHITE, rowheight=32,
            font=("Segoe UI", 10), borderwidth=0)
        s.configure(f"{name}.Heading",
            background=heading_bg, foreground=WHITE,
            font=("Segoe UI", 10, "bold"), relief="flat", padding=(8, 6))
        s.map(name,
            background=[("selected", NAVY_LIGHT)],
            foreground=[("selected", WHITE)])
        s.map(f"{name}.Heading",
            background=[("active", NAVY_DARK)])

    # ══════════════════════════════════════════
    #  VIEW 1 — DASHBOARD
    # ══════════════════════════════════════════
    def _show_all(self):
        self._clear()
        self._bc("Dashboard")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)

        row = tk.Frame(outer, bg=OFF_WHITE)
        row.pack(fill="x", pady=(0, 4))
        page_title(row, "Student Records").pack(side="left")
        badge = tk.Label(row, text=f"  {len(self.system.students)} Enrolled  ",
                         bg=GOLD_LIGHT, fg=NAVY, font=("Segoe UI", 9, "bold"),
                         padx=8, pady=3)
        badge.pack(side="right", pady=6)

        h_rule(outer).pack(fill="x", pady=8)
        self._render_table(outer, self.system.students)

    def _render_table(self, parent, students):
        self._apply_tree_style()
        cols = ("ID", "Full Name", "Age", "Courses", "GPA", "Standing")

        wrap = tk.Frame(parent, bg=BORDER, bd=1)
        wrap.pack(fill="both", expand=True)

        tree = ttk.Treeview(wrap, columns=cols, show="headings",
                            style="Portal.Treeview", selectmode="browse")
        widths  = [80, 190, 55, 70, 80, 120]
        anchors = ["center", "w", "center", "center", "center", "center"]
        for col, w, anc in zip(cols, widths, anchors):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor=anc, minwidth=w)

        tree.tag_configure("even", background="#EEF2FA")
        tree.tag_configure("odd",  background=WHITE)

        for i, s in enumerate(students):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", tags=(tag,),
                        values=(s.student_id, s.name, s.age,
                                len(s.courses), f"{s.GPA:.1f}", standing(s.GPA)))

        sb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        tree.bind("<Double-1>", lambda e: self._open_courses(
            str(tree.item(tree.focus())["values"][0]) if tree.focus() else None))

        tk.Label(parent, text="  ↑ Double-click a row to manage that student's courses",
                 bg=OFF_WHITE, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(6, 0))
        return tree

    # ─── course management popup ──────────────
    def _open_courses(self, sid):
        if not sid: return
        s = self.system.find_student(sid)
        if not s: return

        win = tk.Toplevel(self)
        win.title(f"Courses — {s.name}")
        win.configure(bg=OFF_WHITE)
        win.geometry("600x520")
        win.resizable(False, False)
        win.grab_set()

        # header
        hdr = tk.Frame(win, bg=NAVY, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"  📋  {s.name}", bg=NAVY, fg=WHITE,
                 font=("Georgia", 12, "bold")).pack(side="left", padx=16, pady=10)
        tk.Label(hdr, text=f"   ID: {s.student_id}", bg=NAVY, fg="#A8BDD8",
                 font=("Segoe UI", 9)).pack(side="left")

        # GPA strip
        fg_g, bg_g = gpa_colors(s.GPA)
        self._gpas = tk.Frame(win, bg=bg_g, pady=10)
        self._gpas.pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(self._gpas, text="Current GPA", bg=bg_g, fg=SUBTEXT,
                 font=("Segoe UI", 9)).pack(side="left", padx=16)
        self._gpa_num = tk.Label(self._gpas, text=f"{s.GPA:.2f}",
                                  bg=bg_g, fg=fg_g, font=("Georgia", 20, "bold"))
        self._gpa_num.pack(side="left", padx=6)
        self._gpa_txt = tk.Label(self._gpas, text=f"— {standing(s.GPA)}",
                                  bg=bg_g, fg=fg_g, font=("Segoe UI", 9, "bold"))
        self._gpa_txt.pack(side="left")

        h_rule(win).pack(fill="x", padx=20, pady=8)

        # course tree
        self._apply_tree_style("Course.Treeview", heading_bg=NAVY_DARK)
        tf = tk.Frame(win, bg=BORDER, bd=1)
        tf.pack(fill="both", expand=True, padx=20)
        self._ct = ttk.Treeview(tf, columns=("Course", "Grade", "Letter"),
                                 show="headings", style="Course.Treeview",
                                 selectmode="browse", height=9)
        for col, w, anc in zip(("Course", "Grade", "Letter"), (270, 100, 120),
                                ("w", "center", "center")):
            self._ct.heading(col, text=col)
            self._ct.column(col, width=w, anchor=anc)
        self._ct.pack(fill="both", expand=True)

        def refresh():
            self._ct.delete(*self._ct.get_children())
            for cn, gr in s.courses.items():
                self._ct.insert("", "end", values=(cn, f"{gr:.0f}", letter_grade(gr)))
            fg2, bg2 = gpa_colors(s.GPA)
            self._gpa_num.config(text=f"{s.GPA:.2f}", fg=fg2, bg=bg2)
            self._gpa_txt.config(text=f"— {standing(s.GPA)}", fg=fg2, bg=bg2)
            self._gpas.config(bg=bg2)
            for ch in self._gpas.winfo_children(): ch.config(bg=bg2)
            self._show_all()

        refresh()

        br = tk.Frame(win, bg=OFF_WHITE)
        br.pack(fill="x", padx=20, pady=14)

        def add_c():
            d = AddCourseDialog(win)
            if d.result: s.add_course(*d.result); refresh()

        def edit_c():
            sel = self._ct.focus()
            if not sel:
                messagebox.showwarning("Select", "Select a course first.", parent=win); return
            cn = self._ct.item(sel)["values"][0]
            ng = simpledialog.askfloat("Edit Grade",
                f"New grade for '{cn}':", parent=win, minvalue=0, maxvalue=100)
            if ng is not None: s.edit_grade(cn, ng); refresh()

        def del_c():
            sel = self._ct.focus()
            if not sel:
                messagebox.showwarning("Select", "Select a course first.", parent=win); return
            cn = self._ct.item(sel)["values"][0]
            if messagebox.askyesno("Confirm", f"Remove course '{cn}'?", parent=win):
                s.delete_course(cn); refresh()

        success_button(br, "＋  Add Course", add_c,  width=14).pack(side="left", padx=(0, 8))
        primary_button(br, "✎   Edit Grade", edit_c, width=13).pack(side="left", padx=(0, 8))
        danger_button( br, "✕   Remove",     del_c,  width=12).pack(side="left")

    # ══════════════════════════════════════════
    #  VIEW 2 — ENROLL
    # ══════════════════════════════════════════
    def _show_add(self):
        self._clear()
        self._bc("Enroll Student")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)
        page_title(outer, "Enroll New Student").pack(anchor="w")
        h_rule(outer).pack(fill="x", pady=10)

        card = tk.Frame(outer, bg=WHITE, bd=1,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(anchor="w", fill="x", ipadx=20, ipady=16)

        form = tk.Frame(card, bg=WHITE)
        form.pack(padx=24, pady=16, anchor="w")

        section_header(form, "Personal Information", bg=WHITE).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        info_fields = [("Full Name", "e.g. John Smith", 0, 1),
                       ("Age",       "e.g. 20",         2, 3),
                       ("Student ID","e.g. S004",       4, 5)]
        entries = {}
        for lbl, ph, c_lbl, c_ent in info_fields:
            field_label(form, lbl, bg=WHITE).grid(row=1, column=c_lbl, sticky="w",
                                                   padx=(0, 8), pady=(0, 4))
            e, _ = portal_entry(form, ph, width=20)
            e.grid(row=2, column=c_ent, ipady=5, padx=(0, 20), sticky="w")
            entries[lbl] = e

        tk.Frame(form, bg=WHITE, height=8).grid(row=3, column=0, columnspan=6)
        section_header(form, "Initial Courses", bg=WHITE).grid(
            row=4, column=0, columnspan=6, sticky="w", pady=(0, 8))

        cbox = tk.Frame(form, bg=OFF_WHITE, bd=1,
                        highlightthickness=1, highlightbackground=BORDER)
        cbox.grid(row=5, column=0, columnspan=6, sticky="ew", pady=(0, 10))
        crows = []

        def add_row():
            rf = tk.Frame(cbox, bg=OFF_WHITE)
            rf.pack(fill="x", padx=10, pady=4)
            en, _ = portal_entry(rf, "Course name", width=18)
            en.pack(side="left", ipady=4, padx=(0, 8))
            eg, _ = portal_entry(rf, "Grade", width=8)
            eg.pack(side="left", ipady=4, padx=(0, 8))
            def rem():
                rf.destroy(); crows.remove((en, eg))
            tk.Button(rf, text="✕ Remove", command=rem, bg=OFF_WHITE, fg=DANGER,
                      font=("Segoe UI", 8), relief="flat", cursor="hand2",
                      activebackground=DANGER_BG).pack(side="left")
            crows.append((en, eg))

        secondary_button(cbox, "+ Add Course", add_row, width=16).pack(anchor="w", padx=10, pady=8)
        add_row()

        tk.Frame(form, bg=WHITE, height=6).grid(row=6, column=0)

        def submit():
            name  = entries["Full Name"].get().strip()
            age_s = entries["Age"].get().strip()
            sid   = entries["Student ID"].get().strip()
            ph    = {"e.g. John Smith", "e.g. 20", "e.g. S004", ""}
            if name in ph or age_s in ph or sid in ph:
                messagebox.showerror("Validation", "Complete all personal info fields."); return
            try: age = int(age_s)
            except ValueError:
                messagebox.showerror("Validation", "Age must be a whole number."); return
            if self.system.find_student(sid):
                messagebox.showerror("Duplicate", f"ID '{sid}' already exists."); return
            courses = {}
            for en, eg in crows:
                cn = en.get().strip(); cg = eg.get().strip()
                if cn and cg and cn != "Course name" and cg != "Grade":
                    try: courses[cn] = float(cg)
                    except ValueError:
                        messagebox.showerror("Validation", f"Invalid grade for '{cn}'."); return
            self.system.add_student(Student(name, age, sid, courses))
            self._refresh_count()
            messagebox.showinfo("Enrolled", f"'{name}' has been enrolled.")
            self._show_all()

        br = tk.Frame(form, bg=WHITE)
        br.grid(row=7, column=0, columnspan=6, sticky="w", pady=4)
        success_button(br, "✔  Enroll Student", submit, width=20).pack(side="left", padx=(0, 10))
        secondary_button(br, "Cancel", self._show_all, width=10).pack(side="left")

    # ══════════════════════════════════════════
    #  VIEW 3 — SEARCH
    # ══════════════════════════════════════════
    def _show_search(self):
        self._clear()
        self._bc("Search Records")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)
        page_title(outer, "Search Student Records").pack(anchor="w")
        h_rule(outer).pack(fill="x", pady=10)

        card = tk.Frame(outer, bg=WHITE, bd=1,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", ipadx=16, ipady=4)
        bar = tk.Frame(card, bg=WHITE)
        bar.pack(padx=20, pady=14, anchor="w")
        field_label(bar, "Student ID", bg=WHITE).pack(anchor="w", pady=(0, 4))
        row = tk.Frame(bar, bg=WHITE)
        row.pack(anchor="w")
        e, _ = portal_entry(row, "Enter Student ID (e.g. S002)", width=30)
        e.pack(side="left", ipady=6, padx=(0, 10))

        res = tk.Frame(outer, bg=OFF_WHITE)
        res.pack(fill="both", expand=True, pady=14)

        def search():
            for w in res.winfo_children(): w.destroy()
            sid = e.get().strip()
            if not sid or sid == "Enter Student ID (e.g. S002)": return
            s = self.system.find_student(sid)
            if not s:
                msg = tk.Frame(res, bg=DANGER_BG, bd=1,
                               highlightthickness=1, highlightbackground=DANGER)
                msg.pack(fill="x", pady=4, ipady=10)
                tk.Label(msg, text=f"  ✕  No student found with ID '{sid}'",
                         bg=DANGER_BG, fg=DANGER, font=FONT_BODY).pack(anchor="w", padx=16)
                return
            section_header(res, "Search Result").pack(anchor="w", pady=(0, 8))
            self._render_table(res, [s])

        primary_button(row, "🔍  Search", search, width=12).pack(side="left")
        e.bind("<Return>", lambda ev: search())

    # ══════════════════════════════════════════
    #  VIEW 4 — EDIT
    # ══════════════════════════════════════════
    def _show_edit(self):
        self._clear()
        self._bc("Edit Student")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)
        page_title(outer, "Edit Student Record").pack(anchor="w")
        h_rule(outer).pack(fill="x", pady=10)

        card = tk.Frame(outer, bg=WHITE, bd=1,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", ipadx=16, ipady=4)
        bar = tk.Frame(card, bg=WHITE)
        bar.pack(padx=20, pady=14, anchor="w")
        field_label(bar, "Student ID", bg=WHITE).pack(anchor="w", pady=(0, 4))
        row = tk.Frame(bar, bg=WHITE)
        row.pack(anchor="w")
        e_id, _ = portal_entry(row, "Enter Student ID", width=26)
        e_id.pack(side="left", ipady=6, padx=(0, 10))

        ea = tk.Frame(outer, bg=OFF_WHITE)
        ea.pack(fill="both", expand=True, pady=12)

        def load():
            for w in ea.winfo_children(): w.destroy()
            sid = e_id.get().strip()
            s = self.system.find_student(sid)
            if not s:
                msg = tk.Frame(ea, bg=DANGER_BG, bd=1,
                               highlightthickness=1, highlightbackground=DANGER)
                msg.pack(fill="x", pady=4, ipady=8)
                tk.Label(msg, text=f"  ✕  Student '{sid}' not found.",
                         bg=DANGER_BG, fg=DANGER, font=FONT_BODY).pack(anchor="w", padx=16)
                return

            ec = tk.Frame(ea, bg=WHITE, bd=1,
                          highlightthickness=1, highlightbackground=BORDER)
            ec.pack(fill="x", pady=8, ipadx=16, ipady=8)
            fm = tk.Frame(ec, bg=WHITE)
            fm.pack(padx=20, pady=12, anchor="w")

            section_header(fm, f"Editing: {s.name}  [{s.student_id}]",
                           bg=WHITE).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

            field_label(fm, "Full Name", bg=WHITE).grid(row=1, column=0, sticky="w", pady=(0, 4), padx=(0, 16))
            en, _ = portal_entry(fm, s.name, width=26)
            en.config(fg=TEXT); en.grid(row=2, column=0, ipady=5, padx=(0, 20))

            field_label(fm, "Age", bg=WHITE).grid(row=1, column=1, sticky="w", pady=(0, 4))
            ea2, _ = portal_entry(fm, str(s.age), width=10)
            ea2.config(fg=TEXT); ea2.grid(row=2, column=1, ipady=5)

            def save():
                nm = en.get().strip(); ag = ea2.get().strip()
                if not nm or not ag:
                    messagebox.showerror("Validation", "Name and Age cannot be empty."); return
                try: ag = int(ag)
                except ValueError:
                    messagebox.showerror("Validation", "Age must be a whole number."); return
                s.name = nm; s.age = ag
                messagebox.showinfo("Updated", "Student record updated.")
                self._show_all()

            br = tk.Frame(fm, bg=WHITE)
            br.grid(row=3, column=0, columnspan=4, sticky="w", pady=10)
            success_button(br, "✔  Save Changes", save, width=18).pack(side="left", padx=(0, 10))
            secondary_button(br, "Cancel", self._show_all, width=10).pack(side="left")

        primary_button(row, "Load Record", load, width=14).pack(side="left")
        e_id.bind("<Return>", lambda ev: load())

    # ══════════════════════════════════════════
    #  VIEW 5 — DELETE
    # ══════════════════════════════════════════
    def _show_delete(self):
        self._clear()
        self._bc("Remove Student")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)
        page_title(outer, "Remove Student Record").pack(anchor="w")

        warn = tk.Frame(outer, bg=WARNING_BG, bd=1,
                        highlightthickness=1, highlightbackground="#C8A000")
        warn.pack(fill="x", pady=10, ipady=8)
        tk.Label(warn, text="  ⚠  This action is permanent and cannot be undone.",
                 bg=WARNING_BG, fg=WARNING, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16)

        card = tk.Frame(outer, bg=WHITE, bd=1,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", ipadx=16, ipady=4)
        bar = tk.Frame(card, bg=WHITE)
        bar.pack(padx=20, pady=14, anchor="w")
        field_label(bar, "Student ID to Remove", bg=WHITE).pack(anchor="w", pady=(0, 4))
        row = tk.Frame(bar, bg=WHITE)
        row.pack(anchor="w")
        e, _ = portal_entry(row, "Enter Student ID", width=28)
        e.pack(side="left", ipady=6, padx=(0, 10))

        def delete():
            sid = e.get().strip()
            if not sid or sid == "Enter Student ID": return
            s = self.system.find_student(sid)
            if not s:
                messagebox.showerror("Not Found", f"No student with ID '{sid}'."); return
            if messagebox.askyesno("Confirm Removal",
                f"Permanently remove '{s.name}' ({sid})?", icon="warning"):
                self.system.delete_student(sid)
                self._refresh_count()
                messagebox.showinfo("Removed", f"'{s.name}' has been removed.")
                self._show_all()

        danger_button(row, "🗑️  Remove Student", delete, width=18).pack(side="left")
        e.bind("<Return>", lambda ev: delete())

    # ══════════════════════════════════════════
    #  VIEW 6 — HONOURS BOARD
    # ══════════════════════════════════════════
    def _show_top(self):
        self._clear()
        self._bc("Academic Honours Board")

        outer = tk.Frame(self.main, bg=OFF_WHITE)
        outer.pack(fill="both", expand=True, padx=24, pady=18)
        page_title(outer, "Academic Honours Board").pack(anchor="w")
        tk.Label(outer, text="Top students ranked by cumulative GPA",
                 bg=OFF_WHITE, fg=SUBTEXT, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
        h_rule(outer).pack(fill="x", pady=10)

        top = self.system.top_students(3)
        if not top:
            tk.Label(outer, text="No students enrolled.", bg=OFF_WHITE, fg=MUTED,
                     font=FONT_BODY).pack(anchor="w"); return

        medals     = ["🥇", "🥈", "🥉"]
        ranks      = ["1st Place — Distinction", "2nd Place — Merit", "3rd Place"]
        stripes    = [GOLD, "#8C9BAA", "#A0724A"]

        for i, s in enumerate(top):
            card = tk.Frame(outer, bg=WHITE, bd=1,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(fill="x", pady=7)

            tk.Frame(card, bg=stripes[i], width=7).pack(side="left", fill="y")
            tk.Label(card, text=medals[i], bg=WHITE,
                     font=("Segoe UI Emoji", 26)).pack(side="left", padx=16, pady=14)

            info = tk.Frame(card, bg=WHITE)
            info.pack(side="left", pady=14)
            tk.Label(info, text=s.name, bg=WHITE, fg=TEXT,
                     font=("Georgia", 12, "bold")).pack(anchor="w")
            tk.Label(info,
                     text=f"ID: {s.student_id}   •   Age: {s.age}   •   {len(s.courses)} courses",
                     bg=WHITE, fg=SUBTEXT, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
            tk.Label(info, text=ranks[i], bg=WHITE, fg=stripes[i],
                     font=("Segoe UI", 8, "bold")).pack(anchor="w")

            fg_g, bg_g = gpa_colors(s.GPA)
            gbox = tk.Frame(card, bg=bg_g, padx=18, pady=10)
            gbox.pack(side="right", padx=20, pady=14)
            tk.Label(gbox, text=f"{s.GPA:.2f}", bg=bg_g, fg=fg_g,
                     font=("Georgia", 24, "bold")).pack()
            tk.Label(gbox, text="GPA", bg=bg_g, fg=fg_g,
                     font=("Segoe UI", 8, "bold")).pack()


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
