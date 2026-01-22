import streamlit as st
import random
from questions_v2 import questions_list

# ----------------------------
# LOGIQUE STREAMLIT
# ----------------------------
st.set_page_config(page_title="Quiz Citoyenneté Canadienne", layout="centered")

st.title("🇨🇦 Quiz de citoyenneté canadienne")
st.write(
    "Réponds à 20 questions à choix multiples. Tu gagnes si tu obtiens au moins 15 bonnes réponses."
)

# ----------------------------
# INITIALISATION SESSION
# ----------------------------
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(questions_list, 20)
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = []

# ----------------------------
# INTERFACE
# ----------------------------
st.title("🎓 Jeu de citoyenneté — Quiz QCM")

# ----------------------------
# AFFICHAGE DES QUESTIONS
# ----------------------------
if st.session_state.current_index < len(st.session_state.selected_questions):
    q = st.session_state.selected_questions[st.session_state.current_index]

    st.subheader(f"Question {st.session_state.current_index + 1}/20")
    st.write(q["question"])

    user_choice = st.radio(
        "Choisis une réponse :",
        q["choices"],
        key=f"question_{st.session_state.current_index}",
    )

    if st.button("Valider la réponse"):
        selected_letter = user_choice[0]  # "A", "B", "C" ou "D"
        st.session_state.user_answers.append(selected_letter)

        if selected_letter == q["answer"]:
            st.session_state.score += 1
            st.success("✅ Bonne réponse !")
        else:
            st.error(f"❌ Mauvaise réponse. La bonne réponse était {q['answer']}.")

        st.session_state.current_index += 1
        st.rerun()

# ----------------------------
# FIN DU JEU
# ----------------------------
else:
    st.subheader("📊 Résultat final")
    st.write(f"Score : **{st.session_state.score}/20**")

    if st.session_state.score >= 15:
        st.markdown("""
<style>
@keyframes fly {
    0% { transform: translateY(0) rotate(0deg); opacity: 0; }
    50% { transform: translateY(-50vh) rotate(180deg); opacity: 1; }
    100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
}
.flag {
    position: fixed;
    bottom: 0;
    font-size: 4em;
    animation: fly 8s ease-out;
    pointer-events: none;
    z-index: 1000;
}
.delay1 { animation-delay: 0s; left: 20%; }
.delay2 { animation-delay: 1s; left: 40%; }
.delay3 { animation-delay: 2s; left: 60%; }
.delay4 { animation-delay: 3s; left: 80%; }
</style>
<div class="flag delay1">🇨🇦</div>
<div class="flag delay2">🇨🇦</div>
<div class="flag delay3">🇨🇦</div>
<div class="flag delay4">🇨🇦</div>
""", unsafe_allow_html=True)
        st.success("🏆 Bravo ! Tu as gagné le jeu !")
    else:
        st.warning("😕 Tu as perdu. Réessaie pour t'améliorer !")

    st.markdown("---")
    st.subheader("📝 Récapitulatif des questions et réponses")

    for i, q in enumerate(st.session_state.selected_questions):
        user_letter = st.session_state.user_answers[i]
        correct_letter = q["answer"]

        user_choice_text = next(c for c in q["choices"] if c.startswith(user_letter))
        correct_choice_text = next(
            c for c in q["choices"] if c.startswith(correct_letter)
        )

        is_correct = user_letter == correct_letter
        status = "✅ Correct" if is_correct else "❌ Incorrect"

        st.markdown(f"**Q{i + 1} : {q['question']}**")
        st.write(f"👉 Ta réponse : {user_choice_text}")
        st.write(f"✔️ Bonne réponse : {correct_choice_text}")
        st.write(f"📌 Résultat : {status}")
        st.markdown("---")

    if st.button("🔁 Rejouer"):
        del st.session_state.selected_questions
        del st.session_state.current_index
        del st.session_state.score
        del st.session_state.user_answers
        st.rerun()
