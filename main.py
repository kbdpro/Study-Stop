# -*- coding: utf-8 -*-
"""
Study Stop - Ana Grafik Arayüz (Tkinter GUI)
Kullanıcının eksik konularını yönettiği ve 5 soruluk yeni nesil mini testler çözdüğü ana uygulama.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox

from localization import Localization
from storage import DataManager
from question_engine import DynamicQuestionGenerator


class StudyStopGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Veri yöneticisi ve dil modülü
        self.db = DataManager()
        saved_lang = self.db.get_language()
        self.loc = Localization(default_lang=saved_lang)

        # Pencere ayarları
        self.title("Study Stop")
        self.geometry("960x720")
        self.minsize(860, 640)

        # Renk Paleti (Modern Slate & Indigo)
        self.colors = {
            "bg": "#f1f5f9",
            "card_bg": "#ffffff",
            "primary": "#2563eb",
            "primary_hover": "#1d4ed8",
            "secondary": "#64748b",
            "text": "#0f172a",
            "text_muted": "#64748b",
            "border": "#cbd5e1",
            "success": "#16a34a",
            "danger": "#dc2626",
            "warning": "#d97706",
            "accent": "#4f46e5"
        }

        self.configure(bg=self.colors["bg"])

        # Test durumu değişkenleri
        self.current_quiz_questions = []
        self.current_question_index = 0
        self.current_quiz_topic = None
        self.user_answers = []
        self.selected_option_var = tk.StringVar(value="")
        self.answer_confirmed = False

        # Stil yapılandırması
        self._setup_styles()

        # Arayüz bileşenlerini oluştur
        self._build_ui()

        # İlk veri yüklemeleri
        self.refresh_topics_list()
        self.refresh_history_list()
        self.update_ui_texts()

    def _setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(".", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        
        # Notebook Tab stili
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(16, 8),
                        background="#e2e8f0", foreground=self.colors["text"])
        style.map("TNotebook.Tab",
                  background=[("selected", self.colors["primary"])],
                  foreground=[("selected", "#ffffff")])

        # Treeview stili
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28,
                        background="#ffffff", fieldbackground="#ffffff",
                        bordercolor=self.colors["border"])
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#e2e8f0", foreground=self.colors["text"])
        style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])

        # Combobox stili
        style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff")

    def _build_ui(self):
        # 1. ÜST BİLGİ & DİL ÇUBUĞU (Header)
        self.header_frame = tk.Frame(self, bg="#1e293b", height=75)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.header_inner = tk.Frame(self.header_frame, bg="#1e293b")
        self.header_inner.pack(fill=tk.BOTH, padx=20, pady=12)

        # Başlık ve Alt Başlık
        self.title_box = tk.Frame(self.header_inner, bg="#1e293b")
        self.title_box.pack(side=tk.LEFT, fill=tk.Y)

        self.lbl_app_title = tk.Label(
            self.title_box,
            text=self.loc.t("app_title"),
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1e293b"
        )
        self.lbl_app_title.pack(anchor="w")

        self.lbl_app_subtitle = tk.Label(
            self.title_box,
            text=self.loc.t("app_subtitle"),
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        self.lbl_app_subtitle.pack(anchor="w")

        # Dil Değiştirme Butonu
        lang_text = "🇬🇧 English" if self.loc.current_lang == "tr" else "🇹🇷 Türkçe"
        self.btn_lang = tk.Button(
            self.header_inner,
            text=lang_text,
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#ffffff",
            activebackground="#475569",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.toggle_language
        )
        self.btn_lang.pack(side=tk.RIGHT, pady=4)

        # 2. ANA SEKMELER (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # Sekme 1: Eksik Konular
        self.tab_topics_frame = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_topics_frame, text=self.loc.t("tab_topics"))
        self._build_topics_tab()

        # Sekme 2: Yeni Nesil Mini Test
        self.tab_quiz_frame = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_quiz_frame, text=self.loc.t("tab_quiz"))
        self._build_quiz_tab()

        # Sekme 3: Test Geçmişi
        self.tab_history_frame = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_history_frame, text=self.loc.t("tab_history"))
        self._build_history_tab()

    # =========================================================================
    # SEKME 1: EKSİK KONULAR ARAYÜZÜ
    # =========================================================================
    def _build_topics_tab(self):
        # Üst Kısım: Yeni Konu Ekleme Kartı
        form_card = tk.LabelFrame(
            self.tab_topics_frame,
            text=" ➕ " + self.loc.t("btn_add_topic"),
            bg=self.colors["card_bg"],
            fg=self.colors["primary"],
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=12,
            relief=tk.GROOVE
        )
        form_card.pack(fill=tk.X, padx=8, pady=(8, 12))
        self.form_card = form_card

        # Form Grid
        # Satır 0: Sınıf ve Ders
        lbl_grade = tk.Label(form_card, text=self.loc.t("grade_level"), font=("Segoe UI", 10, "bold"),
                             bg=self.colors["card_bg"], fg=self.colors["text"])
        lbl_grade.grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.lbl_form_grade = lbl_grade

        self.grade_combo = ttk.Combobox(
            form_card,
            values=[
                "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)",
                "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)",
                "Mezun / KPSS", "Üniversite"
            ],
            width=22,
            font=("Segoe UI", 10)
        )
        self.grade_combo.grid(row=0, column=1, sticky="w", padx=6, pady=4)
        self.grade_combo.set("8. Sınıf (LGS)")

        lbl_subject = tk.Label(form_card, text=self.loc.t("subject"), font=("Segoe UI", 10, "bold"),
                               bg=self.colors["card_bg"], fg=self.colors["text"])
        lbl_subject.grid(row=0, column=2, sticky="w", padx=16, pady=4)
        self.lbl_form_subject = lbl_subject

        self.subject_combo = ttk.Combobox(
            form_card,
            values=[
                "Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi",
                "İngilizce", "Din Kültürü", "Fizik", "Kimya", "Biyoloji", "Geometri", "Coğrafya"
            ],
            width=22,
            font=("Segoe UI", 10)
        )
        self.subject_combo.grid(row=0, column=3, sticky="w", padx=6, pady=4)
        self.subject_combo.set("Matematik")

        # Satır 1: Eksik Konu Adı
        lbl_topic = tk.Label(form_card, text=self.loc.t("topic"), font=("Segoe UI", 10, "bold"),
                             bg=self.colors["card_bg"], fg=self.colors["text"])
        lbl_topic.grid(row=1, column=0, sticky="w", padx=6, pady=6)
        self.lbl_form_topic = lbl_topic

        self.ent_topic = tk.Entry(form_card, font=("Segoe UI", 10), width=65)
        self.ent_topic.grid(row=1, column=1, columnspan=3, sticky="we", padx=6, pady=6)

        # Satır 2: Soru Notu / Yapılamayan Kısım
        lbl_note = tk.Label(form_card, text=self.loc.t("question_note"), font=("Segoe UI", 10),
                            bg=self.colors["card_bg"], fg=self.colors["text"])
        lbl_note.grid(row=2, column=0, sticky="w", padx=6, pady=4)
        self.lbl_form_note = lbl_note

        self.ent_note = tk.Entry(form_card, font=("Segoe UI", 10), width=65)
        self.ent_note.grid(row=2, column=1, columnspan=3, sticky="we", padx=6, pady=4)

        # Satır 3: Buton
        self.btn_save_topic = tk.Button(
            form_card,
            text=self.loc.t("btn_add_topic"),
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="#ffffff",
            activebackground=self.colors["primary_hover"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.on_add_topic
        )
        self.btn_save_topic.grid(row=3, column=1, sticky="w", padx=6, pady=(8, 4))

        # Alt Kısım: Eksik Konular Listesi ve Aksiyonlar
        list_card = tk.Frame(self.tab_topics_frame, bg=self.colors["card_bg"], relief=tk.GROOVE, bd=1)
        list_card.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Liste Başlığı ve Butonlar
        toolbar = tk.Frame(list_card, bg=self.colors["card_bg"])
        toolbar.pack(fill=tk.X, padx=12, pady=10)

        self.lbl_list_title = tk.Label(
            toolbar,
            text=self.loc.t("topic_list_title"),
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        )
        self.lbl_list_title.pack(side=tk.LEFT)

        self.btn_delete_topic = tk.Button(
            toolbar,
            text=self.loc.t("btn_delete_topic"),
            font=("Segoe UI", 9),
            bg="#fecaca",
            fg="#991b1b",
            activebackground="#fca5a5",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.on_delete_topic
        )
        self.btn_delete_topic.pack(side=tk.RIGHT, padx=4)

        self.btn_start_quiz = tk.Button(
            toolbar,
            text=self.loc.t("btn_start_quiz_from_topic"),
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            activebackground="#15803d",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.on_start_quiz_from_selected
        )
        self.btn_start_quiz.pack(side=tk.RIGHT, padx=6)

        # Tablo (Treeview)
        tree_container = tk.Frame(list_card, bg=self.colors["card_bg"])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        columns = ("id", "grade", "subject", "topic", "note", "tests", "date")
        self.topics_tree = ttk.Treeview(tree_container, columns=columns, show="headings", selectmode="browse")

        self.topics_tree.heading("id", text="ID")
        self.topics_tree.heading("grade", text=self.loc.t("col_grade"))
        self.topics_tree.heading("subject", text=self.loc.t("col_subject"))
        self.topics_tree.heading("topic", text=self.loc.t("col_topic"))
        self.topics_tree.heading("note", text=self.loc.t("col_note"))
        self.topics_tree.heading("tests", text="Çözülen Test")
        self.topics_tree.heading("date", text=self.loc.t("col_date"))

        self.topics_tree.column("id", width=0, stretch=tk.NO)
        self.topics_tree.column("grade", width=110, anchor="center")
        self.topics_tree.column("subject", width=120, anchor="w")
        self.topics_tree.column("topic", width=220, anchor="w")
        self.topics_tree.column("note", width=240, anchor="w")
        self.topics_tree.column("tests", width=90, anchor="center")
        self.topics_tree.column("date", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.topics_tree.yview)
        self.topics_tree.configure(yscroll=scrollbar.set)

        self.topics_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # =========================================================================
    # SEKME 2: YENİ NESİL MİNİ TEST ARAYÜZÜ
    # =========================================================================
    def _build_quiz_tab(self):
        # Üst Test Bilgi Kartı
        self.quiz_info_frame = tk.Frame(self.tab_quiz_frame, bg="#3b82f6", height=45)
        self.quiz_info_frame.pack(fill=tk.X, padx=8, pady=(8, 6))

        self.lbl_quiz_info = tk.Label(
            self.quiz_info_frame,
            text=self.loc.t("select_topic_prompt"),
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#3b82f6",
            pady=8
        )
        self.lbl_quiz_info.pack()

        # Soru İçerik Kartı (Scrollable)
        self.quiz_card = tk.Frame(self.tab_quiz_frame, bg=self.colors["card_bg"], relief=tk.GROOVE, bd=1)
        self.quiz_card.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Soru Numarası
        self.lbl_question_num = tk.Label(
            self.quiz_card,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["card_bg"],
            anchor="w"
        )
        self.lbl_question_num.pack(fill=tk.X, padx=16, pady=(12, 4))

        # Soru Metni
        self.txt_question_text = tk.Text(
            self.quiz_card,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            bg="#f8fafc",
            fg="#0f172a",
            relief=tk.FLAT,
            height=7,
            padx=12,
            pady=8
        )
        self.txt_question_text.pack(fill=tk.X, padx=16, pady=4)
        self.txt_question_text.config(state=tk.DISABLED)

        # Şıklar (A, B, C, D)
        self.options_frame = tk.Frame(self.quiz_card, bg=self.colors["card_bg"])
        self.options_frame.pack(fill=tk.X, padx=16, pady=8)

        self.option_radios = {}
        for opt_key in ["A", "B", "C", "D"]:
            opt_container = tk.Frame(self.options_frame, bg=self.colors["card_bg"])
            opt_container.pack(fill=tk.X, pady=3)

            rbtn = tk.Radiobutton(
                opt_container,
                text="",
                value=opt_key,
                variable=self.selected_option_var,
                font=("Segoe UI", 10),
                bg=self.colors["card_bg"],
                fg=self.colors["text"],
                activebackground=self.colors["card_bg"],
                selectcolor="#ffffff",
                anchor="w",
                justify=tk.LEFT,
                wraplength=760,
                cursor="hand2"
            )
            rbtn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.option_radios[opt_key] = rbtn

        # Çözüm ve Geri Bildirim Alanı
        self.solution_frame = tk.Frame(self.quiz_card, bg="#f0fdf4", relief=tk.SOLID, bd=1)
        
        self.lbl_feedback_status = tk.Label(
            self.solution_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg="#f0fdf4",
            fg=self.colors["success"]
        )
        self.lbl_feedback_status.pack(anchor="w", padx=12, pady=(6, 2))

        self.txt_solution = tk.Text(
            self.solution_frame,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            bg="#f0fdf4",
            fg="#166534",
            relief=tk.FLAT,
            height=4,
            padx=12,
            pady=4
        )
        self.txt_solution.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))
        self.txt_solution.config(state=tk.DISABLED)

        # Alt Butonlar Çubuğu
        self.quiz_btn_bar = tk.Frame(self.quiz_card, bg=self.colors["card_bg"])
        self.quiz_btn_bar.pack(fill=tk.X, padx=16, pady=12)

        self.btn_submit_ans = tk.Button(
            self.quiz_btn_bar,
            text=self.loc.t("btn_submit_answer"),
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["primary"],
            fg="#ffffff",
            activebackground=self.colors["primary_hover"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.on_submit_answer
        )
        self.btn_submit_ans.pack(side=tk.LEFT)

        self.btn_next_q = tk.Button(
            self.quiz_btn_bar,
            text=self.loc.t("btn_next_question"),
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["accent"],
            fg="#ffffff",
            activebackground="#4338ca",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.on_next_question
        )

        # Başlangıçta test aktif değilse boş ekran mesajı
        self._show_empty_quiz_state()

    def _show_empty_quiz_state(self):
        self.lbl_question_num.config(text="")
        self.txt_question_text.config(state=tk.NORMAL)
        self.txt_question_text.delete("1.0", tk.END)
        self.txt_question_text.insert(
            tk.END,
            self.loc.t("select_topic_prompt")
        )
        self.txt_question_text.config(state=tk.DISABLED)
        for rbtn in self.option_radios.values():
            rbtn.config(text="", state=tk.DISABLED)
        self.solution_frame.pack_forget()
        self.btn_submit_ans.pack_forget()
        self.btn_next_q.pack_forget()

    # =========================================================================
    # SEKME 3: TEST GEÇMİŞİ ARAYÜZÜ
    # =========================================================================
    def _build_history_tab(self):
        container = tk.Frame(self.tab_history_frame, bg=self.colors["card_bg"], relief=tk.GROOVE, bd=1)
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Araç çubuğu
        toolbar = tk.Frame(container, bg=self.colors["card_bg"])
        toolbar.pack(fill=tk.X, padx=12, pady=10)

        self.lbl_hist_title = tk.Label(
            toolbar,
            text=self.loc.t("history_title"),
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        )
        self.lbl_hist_title.pack(side=tk.LEFT)

        self.btn_clear_hist = tk.Button(
            toolbar,
            text=self.loc.t("btn_clear_history"),
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg=self.colors["text"],
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.on_clear_history
        )
        self.btn_clear_hist.pack(side=tk.RIGHT)

        # Geçmiş Tablosu
        tree_frame = tk.Frame(container, bg=self.colors["card_bg"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        columns = ("date", "grade", "subject", "topic", "score", "percent")
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.history_tree.heading("date", text=self.loc.t("col_date"))
        self.history_tree.heading("grade", text=self.loc.t("col_grade"))
        self.history_tree.heading("subject", text=self.loc.t("col_subject"))
        self.history_tree.heading("topic", text=self.loc.t("col_topic"))
        self.history_tree.heading("score", text=self.loc.t("col_score"))
        self.history_tree.heading("percent", text=self.loc.t("col_percent"))

        self.history_tree.column("date", width=130, anchor="center")
        self.history_tree.column("grade", width=100, anchor="center")
        self.history_tree.column("subject", width=120, anchor="w")
        self.history_tree.column("topic", width=240, anchor="w")
        self.history_tree.column("score", width=80, anchor="center")
        self.history_tree.column("percent", width=80, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scroll.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # =========================================================================
    # VERİ YÖNETİMİ & EVENT HANDLERLARI
    # =========================================================================
    def on_add_topic(self):
        grade = self.grade_combo.get().strip()
        subject = self.subject_combo.get().strip()
        topic = self.ent_topic.get().strip()
        note = self.ent_note.get().strip()

        if not grade or not subject or not topic:
            messagebox.showwarning("Study Stop", self.loc.t("fill_required"), parent=self)
            return

        self.db.add_topic(grade, subject, topic, note)
        self.ent_topic.delete(0, tk.END)
        self.ent_note.delete(0, tk.END)
        self.refresh_topics_list()
        messagebox.showinfo("Study Stop", self.loc.t("topic_added_success"), parent=self)

    def on_delete_topic(self):
        selected_item = self.topics_tree.selection()
        if not selected_item:
            return
        
        confirm = messagebox.askyesno("Study Stop", self.loc.t("confirm_delete"), parent=self)
        if confirm:
            item_values = self.topics_tree.item(selected_item[0], "values")
            topic_id = item_values[0]
            self.db.delete_topic(topic_id)
            self.refresh_topics_list()

    def on_start_quiz_from_selected(self):
        selected_item = self.topics_tree.selection()
        if not selected_item:
            messagebox.showwarning("Study Stop", self.loc.t("select_topic_prompt"), parent=self)
            return

        item_values = self.topics_tree.item(selected_item[0], "values")
        topic_id = item_values[0]
        topic_data = self.db.get_topic_by_id(topic_id)
        if topic_data:
            self.start_quiz(topic_data)

    def start_quiz(self, topic_data):
        self.current_quiz_topic = topic_data
        self.current_question_index = 0
        self.user_answers = []

        # 5 soruluk yeni nesil soru üretimi
        self.current_quiz_questions = DynamicQuestionGenerator.generate_5_questions(
            grade=topic_data["grade"],
            subject=topic_data["subject"],
            topic=topic_data["topic"],
            note=topic_data.get("note", ""),
            lang=self.loc.current_lang
        )

        # Bilgi başlığını güncelle
        info_str = self.loc.t(
            "quiz_info",
            topic=topic_data["topic"],
            subject=topic_data["subject"],
            grade=topic_data["grade"]
        )
        self.lbl_quiz_info.config(text=info_str)

        # Mini test sekmesine geç
        self.notebook.select(self.tab_quiz_frame)

        # İlk soruyu yükle
        self.load_question(0)

    def load_question(self, index):
        if index >= len(self.current_quiz_questions):
            self.finish_quiz()
            return

        self.current_question_index = index
        self.answer_confirmed = False
        self.selected_option_var.set("")
        self.solution_frame.pack_forget()
        self.btn_next_q.pack_forget()
        self.btn_submit_ans.pack(side=tk.LEFT)

        q = self.current_quiz_questions[index]

        # Soru başlığı
        header_text = self.loc.t("question_header", current=index + 1, total=len(self.current_quiz_questions))
        self.lbl_question_num.config(text=header_text)

        # Soru metni
        self.txt_question_text.config(state=tk.NORMAL)
        self.txt_question_text.delete("1.0", tk.END)
        self.txt_question_text.insert(tk.END, q["question"])
        self.txt_question_text.config(state=tk.DISABLED)

        # Şıklar
        options = q["options"]
        for key, rbtn in self.option_radios.items():
            opt_text = f"{key}) {options.get(key, '')}"
            rbtn.config(text=opt_text, state=tk.NORMAL, fg=self.colors["text"])

    def on_submit_answer(self):
        user_choice = self.selected_option_var.get()
        if not user_choice:
            messagebox.showwarning("Study Stop", self.loc.t("select_answer_warning"), parent=self)
            return

        self.answer_confirmed = True
        q = self.current_quiz_questions[self.current_question_index]
        correct_choice = q["correct"]
        is_correct = (user_choice == correct_choice)

        self.user_answers.append({
            "question_index": self.current_question_index,
            "user_choice": user_choice,
            "correct_choice": correct_choice,
            "is_correct": is_correct
        })

        # Şıkları kilitle ve renklendir
        for key, rbtn in self.option_radios.items():
            if key == correct_choice:
                rbtn.config(fg="#16a34a", font=("Segoe UI", 10, "bold"))
            elif key == user_choice and not is_correct:
                rbtn.config(fg="#dc2626", font=("Segoe UI", 10, "bold"))
            rbtn.config(state=tk.DISABLED)

        # Çözüm ve Geri Bildirim kutusu
        status_text = self.loc.t("status_correct") if is_correct else self.loc.t("status_incorrect")
        status_color = self.colors["success"] if is_correct else self.colors["danger"]
        bg_box = "#f0fdf4" if is_correct else "#fef2f2"

        self.solution_frame.config(bg=bg_box)
        self.lbl_feedback_status.config(
            text=f"{status_text} | " + self.loc.t("correct_answer", ans=correct_choice) + " | " + self.loc.t("your_answer", ans=user_choice),
            fg=status_color,
            bg=bg_box
        )

        self.txt_solution.config(state=tk.NORMAL, bg=bg_box, fg="#1e293b")
        self.txt_solution.delete("1.0", tk.END)
        self.txt_solution.insert(tk.END, self.loc.t("solution_label") + "\n" + q.get("explanation", ""))
        self.txt_solution.config(state=tk.DISABLED)

        self.solution_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # Butonları güncelle
        self.btn_submit_ans.pack_forget()
        next_label = self.loc.t("btn_next_question") if (self.current_question_index < len(self.current_quiz_questions) - 1) else self.loc.t("btn_finish_quiz")
        self.btn_next_q.config(text=next_label)
        self.btn_next_q.pack(side=tk.LEFT)

    def on_next_question(self):
        next_idx = self.current_question_index + 1
        if next_idx < len(self.current_quiz_questions):
            self.load_question(next_idx)
        else:
            self.finish_quiz()

    def finish_quiz(self):
        total = len(self.current_quiz_questions)
        correct_count = sum(1 for ans in self.user_answers if ans["is_correct"])
        percentage = round((correct_count / total) * 100) if total > 0 else 0

        # Veritabanına geçmişi kaydet
        if self.current_quiz_topic:
            self.db.add_history_entry(
                topic=self.current_quiz_topic["topic"],
                subject=self.current_quiz_topic["subject"],
                grade=self.current_quiz_topic["grade"],
                score=correct_count,
                total=total
            )
            self.db.increment_topic_test_count(self.current_quiz_topic["id"])

        self.refresh_topics_list()
        self.refresh_history_list()

        # Geri bildirim mesajı seçimi
        if percentage >= 80:
            fb_text = self.loc.t("score_feedback_high")
        elif percentage >= 50:
            fb_text = self.loc.t("score_feedback_med")
        else:
            fb_text = self.loc.t("score_feedback_low")

        result_msg = (
            f"{self.loc.t('score_title')}\n\n"
            f"{self.loc.t('score_result', correct=correct_count, total=total, percentage=percentage)}\n\n"
            f"{fb_text}"
        )

        messagebox.showinfo(self.loc.t("score_title"), result_msg, parent=self)
        self._show_empty_quiz_state()
        self.notebook.select(self.tab_history_frame)

    def refresh_topics_list(self):
        for item in self.topics_tree.get_children():
            self.topics_tree.delete(item)

        topics = self.db.get_topics()
        for t in topics:
            self.topics_tree.insert(
                "",
                tk.END,
                values=(
                    t["id"],
                    t["grade"],
                    t["subject"],
                    t["topic"],
                    t.get("note", "-"),
                    t.get("tests_completed", 0),
                    t.get("created_at", "-")
                )
            )

    def refresh_history_list(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        history = self.db.get_history()
        for h in history:
            self.history_tree.insert(
                "",
                tk.END,
                values=(
                    h["date"],
                    h["grade"],
                    h["subject"],
                    h["topic"],
                    f"{h['score']} / {h['total']}",
                    f"%{h['percentage']}"
                )
            )

    def on_clear_history(self):
        if messagebox.askyesno("Study Stop", self.loc.t("confirm_delete"), parent=self):
            self.db.clear_history()
            self.refresh_history_list()

    def toggle_language(self):
        new_lang = self.loc.toggle_language()
        self.db.set_language(new_lang)
        self.update_ui_texts()

    def update_ui_texts(self):
        # Üst Header
        self.lbl_app_title.config(text=self.loc.t("app_title"))
        self.lbl_app_subtitle.config(text=self.loc.t("app_subtitle"))
        lang_btn_text = "🇬🇧 English" if self.loc.current_lang == "tr" else "🇹🇷 Türkçe"
        self.btn_lang.config(text=lang_btn_text)

        # Sekme başlıkları
        self.notebook.tab(0, text=self.loc.t("tab_topics"))
        self.notebook.tab(1, text=self.loc.t("tab_quiz"))
        self.notebook.tab(2, text=self.loc.t("tab_history"))

        # Form etiketleri
        self.form_card.config(text=" ➕ " + self.loc.t("btn_add_topic"))
        self.lbl_form_grade.config(text=self.loc.t("grade_level"))
        self.lbl_form_subject.config(text=self.loc.t("subject"))
        self.lbl_form_topic.config(text=self.loc.t("topic"))
        self.lbl_form_note.config(text=self.loc.t("question_note"))
        self.btn_save_topic.config(text=self.loc.t("btn_add_topic"))

        # Liste Butonları ve Başlığı
        self.lbl_list_title.config(text=self.loc.t("topic_list_title"))
        self.btn_delete_topic.config(text=self.loc.t("btn_delete_topic"))
        self.btn_start_quiz.config(text=self.loc.t("btn_start_quiz_from_topic"))

        # Tablo sütun başlıkları
        self.topics_tree.heading("grade", text=self.loc.t("col_grade"))
        self.topics_tree.heading("subject", text=self.loc.t("col_subject"))
        self.topics_tree.heading("topic", text=self.loc.t("col_topic"))
        self.topics_tree.heading("note", text=self.loc.t("col_note"))
        self.topics_tree.heading("date", text=self.loc.t("col_date"))

        # Test Geçmişi
        self.lbl_hist_title.config(text=self.loc.t("history_title"))
        self.btn_clear_hist.config(text=self.loc.t("btn_clear_history"))
        self.history_tree.heading("date", text=self.loc.t("col_date"))
        self.history_tree.heading("grade", text=self.loc.t("col_grade"))
        self.history_tree.heading("subject", text=self.loc.t("col_subject"))
        self.history_tree.heading("topic", text=self.loc.t("col_topic"))
        self.history_tree.heading("score", text=self.loc.t("col_score"))
        self.history_tree.heading("percent", text=self.loc.t("col_percent"))

        # Mini test boş ekranı
        if not self.current_quiz_questions:
            self._show_empty_quiz_state()


def main():
    app = StudyStopGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
