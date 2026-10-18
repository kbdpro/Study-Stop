# -*- coding: utf-8 -*-
"""
Study Stop - Dil ve Çeviri Modülü (Localization Module)
Türkçe ve İngilizce dil desteği sağlar.
"""

TRANSLATIONS = {
    "tr": {
        "app_title": "Study Stop - Eksik Konu & Yeni Nesil Çalışma Uygulaması",
        "app_subtitle": "Eksiklerini Belirle, Yeni Nesil Sorularla Pekiştir!",
        "tab_topics": "📌 Eksik Konular",
        "tab_quiz": "📝 Yeni Nesil Mini Test",
        "tab_history": "📊 Test Geçmişi",
        "language": "Dil / Language",
        "grade_level": "Sınıf Düzeyi:",
        "grade_placeholder": "Örn: 8. Sınıf, 11. Sınıf, LGS, YKS",
        "subject": "Ders:",
        "subject_placeholder": "Örn: Matematik, Fen Bilimleri, Türkçe, Fizik",
        "topic": "Eksik Konu Adı:",
        "topic_placeholder": "Örn: Çarpanlar ve Katlar, Paragrafta Anlam, Basınç",
        "question_note": "Yapamadığın Soru / Zorlandığın Kısım (İsteğe Bağlı):",
        "note_placeholder": "Örn: Deneyli sorularda ve grafik yorumlamada zorlanıyorum.",
        "btn_add_topic": "➕ Eksik Konu Ekle",
        "btn_delete_topic": "🗑️ Seçileni Sil",
        "btn_start_quiz_from_topic": "🎯 Bu Konudan 5 Soruluk Mini Test Başlat",
        "topic_list_title": "Eksik Olduğun Konular Listesi",
        "col_grade": "Sınıf",
        "col_subject": "Ders",
        "col_topic": "Konu",
        "col_note": "Soru Notu",
        "col_date": "Tarih",
        "no_topics_yet": "Henüz eklenmiş bir eksik konu yok. Yukarıdaki formdan ekleyebilirsiniz.",
        "select_topic_prompt": "Lütfen önce test çözmek istediğiniz eksik konuyu seçin!",
        "quiz_title": "Yeni Nesil 5 Soruluk Mini Test",
        "quiz_info": "Konu: {topic} | Ders: {subject} | Sınıf: {grade}",
        "question_header": "Soru {current} / {total}",
        "btn_submit_answer": "Cevabı Onayla",
        "btn_next_question": "Sonraki Soru ➡️",
        "btn_finish_quiz": "Testi Tamamla 🏁",
        "btn_new_quiz": "🔄 Yeni Test Çöz",
        "score_title": "🎉 Mini Test Tamamlandı!",
        "score_result": "Sonucunuz: {correct} / {total} Doğru ({percentage}%)",
        "score_feedback_high": "Tebrikler! Bu konuda gayet başarılısın. Pratiğe devam et!",
        "score_feedback_med": "İyi başlangıç! Yanlış yaptığın soruların çözümlerini dikkatle incele.",
        "score_feedback_low": "Bu konuyu biraz daha tekrar etmelisin. Çözüm adımlarını mutlaka oku!",
        "solution_label": "💡 Soru Çözümü & Açıklama:",
        "correct_answer": "Doğru Cevap: {ans}",
        "your_answer": "Senin Cevabın: {ans}",
        "status_correct": "✅ Doğru!",
        "status_incorrect": "❌ Yanlış!",
        "select_answer_warning": "Lütfen bir şık (A, B, C, D) seçiniz!",
        "confirm_delete": "Bu konuyu silmek istediğinize emin misiniz?",
        "topic_added_success": "Eksik konu başarıyla eklendi!",
        "fill_required": "Lütfen Sınıf, Ders ve Konu alanlarını doldurunuz.",
        "history_title": "Çözülen Mini Testlerin Geçmişi",
        "col_score": "Skor",
        "col_percent": "Başarı %",
        "btn_clear_history": "Geçmişi Temizle",
        "switch_lang_btn": "English'e Geç",
    },
    "en": {
        "app_title": "Study Stop - Weak Topics & New Generation Study App",
        "app_subtitle": "Identify Weak Topics, Master Them with New Generation Questions!",
        "tab_topics": "📌 Weak Topics",
        "tab_quiz": "📝 New Gen Mini Test",
        "tab_history": "📊 Test History",
        "language": "Language / Dil",
        "grade_level": "Grade Level:",
        "grade_placeholder": "e.g., 8th Grade, 11th Grade, High School",
        "subject": "Subject:",
        "subject_placeholder": "e.g., Mathematics, Science, English, Physics",
        "topic": "Weak Topic Name:",
        "topic_placeholder": "e.g., Fractions, Electric Circuits, Reading Comprehension",
        "question_note": "Struggled Question / Note (Optional):",
        "note_placeholder": "e.g., I have trouble with graph interpretation questions.",
        "btn_add_topic": "➕ Add Weak Topic",
        "btn_delete_topic": "🗑️ Delete Selected",
        "btn_start_quiz_from_topic": "🎯 Start 5-Question Mini Test on This Topic",
        "topic_list_title": "Your Weak Topics List",
        "col_grade": "Grade",
        "col_subject": "Subject",
        "col_topic": "Topic",
        "col_note": "Question Note",
        "col_date": "Date",
        "no_topics_yet": "No weak topics added yet. Add one using the form above.",
        "select_topic_prompt": "Please select a topic from the list to start a test!",
        "quiz_title": "New Generation 5-Question Mini Test",
        "quiz_info": "Topic: {topic} | Subject: {subject} | Grade: {grade}",
        "question_header": "Question {current} / {total}",
        "btn_submit_answer": "Confirm Answer",
        "btn_next_question": "Next Question ➡️",
        "btn_finish_quiz": "Finish Test 🏁",
        "btn_new_quiz": "🔄 New Test",
        "score_title": "🎉 Mini Test Completed!",
        "score_result": "Your Result: {correct} / {total} Correct ({percentage}%)",
        "score_feedback_high": "Congratulations! You have strong understanding. Keep practicing!",
        "score_feedback_med": "Good effort! Carefully review the solutions of the questions you missed.",
        "score_feedback_low": "You should review this topic again. Be sure to check the solution steps!",
        "solution_label": "💡 Solution & Explanation:",
        "correct_answer": "Correct Answer: {ans}",
        "your_answer": "Your Answer: {ans}",
        "status_correct": "✅ Correct!",
        "status_incorrect": "❌ Incorrect!",
        "select_answer_warning": "Please select an option (A, B, C, D)!",
        "confirm_delete": "Are you sure you want to delete this topic?",
        "topic_added_success": "Weak topic successfully added!",
        "fill_required": "Please fill in Grade, Subject, and Topic fields.",
        "history_title": "Mini Test History",
        "col_score": "Score",
        "col_percent": "Success %",
        "btn_clear_history": "Clear History",
        "switch_lang_btn": "Türkçe'ye Geç",
    }
}

class Localization:
    def __init__(self, default_lang="tr"):
        self.current_lang = default_lang if default_lang in TRANSLATIONS else "tr"

    def set_language(self, lang):
        if lang in TRANSLATIONS:
            self.current_lang = lang

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "tr" else "tr"
        return self.current_lang

    def get(self, key, **kwargs):
        text = TRANSLATIONS.get(self.current_lang, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def t(self, key, **kwargs):
        return self.get(key, **kwargs)
