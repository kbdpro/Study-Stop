# -*- coding: utf-8 -*-
"""
Study Stop - Komut Satırı Arayüzü (CLI Version)
Terminal üzerinden eksik konuları yönetmek ve yeni nesil mini test çözmek için alternatif arayüz.
"""

import sys
from localization import Localization
from storage import DataManager
from question_engine import DynamicQuestionGenerator

def clear_screen():
    print("\n" + "=" * 65 + "\n")

def run_cli():
    db = DataManager()
    loc = Localization(default_lang=db.get_language())

    while True:
        clear_screen()
        print("🛑  STUDY STOP - " + loc.t("app_title"))
        print("    " + loc.t("app_subtitle"))
        print("-" * 65)
        print("1. " + loc.t("tab_topics") + " (Ekle / Listele / Sil)")
        print("2. " + loc.t("tab_quiz") + " (5 Soru)")
        print("3. " + loc.t("tab_history"))
        print("4. " + loc.t("language") + f" [Şu an: {loc.current_lang.upper()}]")
        print("5. Çıkış / Exit")
        print("-" * 65)

        choice = input("👉 Seçiminiz / Your Choice (1-5): ").strip()

        if choice == "1":
            handle_topics_menu(db, loc)
        elif choice == "2":
            handle_quiz_menu(db, loc)
        elif choice == "3":
            handle_history_menu(db, loc)
        elif choice == "4":
            new_lang = loc.toggle_language()
            db.set_language(new_lang)
            print(f"Dil değiştirildi: {new_lang.upper()}")
            input("Devam etmek için Enter'a basın...")
        elif choice == "5":
            print("Study Stop'tan çıkılıyor. İyi çalışmalar!")
            break
        else:
            print("Geçersiz seçim!")

def handle_topics_menu(db, loc):
    while True:
        clear_screen()
        print("📌  " + loc.t("topic_list_title").upper())
        print("-" * 65)
        topics = db.get_topics()

        if not topics:
            print(loc.t("no_topics_yet"))
        else:
            for idx, t in enumerate(topics, 1):
                note_str = f" | Not: {t['note']}" if t.get('note') else ""
                print(f"[{idx}] {t['grade']} - {t['subject']}: {t['topic']}{note_str} (Çözülen: {t.get('tests_completed', 0)})")

        print("-" * 65)
        print("A. " + loc.t("btn_add_topic"))
        print("D. " + loc.t("btn_delete_topic"))
        print("Q. Ana Menüye Dön")
        sub_choice = input("👉 Seçiminiz (A/D/Q): ").strip().upper()

        if sub_choice == "A":
            grade = input(f"{loc.t('grade_level')} (Örn: 8. Sınıf, 11. Sınıf): ").strip()
            subject = input(f"{loc.t('subject')} (Örn: Matematik, Fizik): ").strip()
            topic = input(f"{loc.t('topic')} (Örn: Çarpanlar ve Katlar): ").strip()
            note = input(f"{loc.t('question_note')}: ").strip()

            if grade and subject and topic:
                db.add_topic(grade, subject, topic, note)
                print(loc.t("topic_added_success"))
            else:
                print(loc.t("fill_required"))
            input("Devam etmek için Enter'a basın...")

        elif sub_choice == "D":
            if not topics:
                input("Silinecek konu yok. Enter'a basın...")
                continue
            idx_str = input("Silmek istediğiniz konunun numarasını girin: ").strip()
            if idx_str.isdigit() and 1 <= int(idx_str) <= len(topics):
                selected = topics[int(idx_str) - 1]
                db.delete_topic(selected["id"])
                print("Konu silindi.")
            else:
                print("Geçersiz numara!")
            input("Devam etmek için Enter'a basın...")

        elif sub_choice == "Q":
            break

def handle_quiz_menu(db, loc):
    clear_screen()
    print("📝  " + loc.t("quiz_title").upper())
    print("-" * 65)
    topics = db.get_topics()

    if not topics:
        print(loc.t("no_topics_yet"))
        print("Önce bir eksik konu eklemelisiniz!")
        input("Devam etmek için Enter'a basın...")
        return

    print("Test çözmek istediğiniz eksik konuyu seçin:\n")
    for idx, t in enumerate(topics, 1):
        print(f"[{idx}] {t['grade']} | {t['subject']} -> {t['topic']}")

    sel = input(f"\n👉 Konu Numarası (1-{len(topics)}): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(topics)):
        print("Geçersiz seçim!")
        input("Devam etmek için Enter'a basın...")
        return

    selected_topic = topics[int(sel) - 1]
    questions = DynamicQuestionGenerator.generate_5_questions(
        grade=selected_topic["grade"],
        subject=selected_topic["subject"],
        topic=selected_topic["topic"],
        note=selected_topic.get("note", ""),
        lang=loc.current_lang
    )

    correct_count = 0
    total = len(questions)

    for idx, q in enumerate(questions, 1):
        clear_screen()
        print(loc.t("quiz_info", topic=selected_topic["topic"], subject=selected_topic["subject"], grade=selected_topic["grade"]))
        print("=" * 65)
        print(f"📢  {loc.t('question_header', current=idx, total=total)}\n")
        print(q["question"])
        print("\nŞıklar:")
        for opt_key in ["A", "B", "C", "D"]:
            print(f"  [{opt_key}] {q['options'].get(opt_key, '')}")
        print("-" * 65)

        user_ans = ""
        while user_ans not in ["A", "B", "C", "D"]:
            user_ans = input("👉 Cevabınız (A, B, C, D): ").strip().upper()

        is_correct = (user_ans == q["correct"])
        if is_correct:
            correct_count += 1
            print(f"\n{loc.t('status_correct')} 🌟")
        else:
            print(f"\n{loc.t('status_incorrect')} ❗")
            print(loc.t("correct_answer", ans=q["correct"]))

        print("\n" + loc.t("solution_label"))
        print(q.get("explanation", ""))
        input("\nSonraki soru için Enter'a basın...")

    # Test bitti
    clear_screen()
    percentage = round((correct_count / total) * 100) if total > 0 else 0
    db.add_history_entry(
        topic=selected_topic["topic"],
        subject=selected_topic["subject"],
        grade=selected_topic["grade"],
        score=correct_count,
        total=total
    )
    db.increment_topic_test_count(selected_topic["id"])

    print("🎉 " + loc.t("score_title"))
    print("-" * 65)
    print(loc.t("score_result", correct=correct_count, total=total, percentage=percentage))
    if percentage >= 80:
        print(loc.t("score_feedback_high"))
    elif percentage >= 50:
        print(loc.t("score_feedback_med"))
    else:
        print(loc.t("score_feedback_low"))

    input("\nAna Menüye dönmek için Enter'a basın...")

def handle_history_menu(db, loc):
    clear_screen()
    print("📊  " + loc.t("history_title").upper())
    print("-" * 65)
    history = db.get_history()

    if not history:
        print("Henüz çözülmüş bir test bulunmuyor.")
    else:
        for idx, h in enumerate(history, 1):
            print(f"[{idx}] {h['date']} | {h['grade']} | {h['subject']} - {h['topic']} -> Skor: {h['score']}/{h['total']} (%{h['percentage']})")

    print("-" * 65)
    action = input("Geçmişi temizlemek için 'C', geri dönmek için Enter'a basın: ").strip().upper()
    if action == "C":
        db.clear_history()
        print("Geçmiş temizlendi.")
        input("Enter'a basın...")

if __name__ == "__main__":
    run_cli()
