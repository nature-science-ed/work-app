import streamlit as st
import random

st.set_page_config(page_title="仕事の計算トレーニング", page_icon="⚙️")

st.title("仕事の計算トレーニング（W = F × d）")
st.write("力の大きさ F（N） と 動いた距離 d（m） から仕事 W（J）を計算する練習アプリです。")

NUM_QUESTIONS = 5  # 出題数


# --- 問題を作る関数 ---
def generate_questions(n):
    questions = []
    for i in range(n):
        # 力Fと距離dの値（必要に応じて変更OK）
        F = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])  # N
        d = random.choice([0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10])  # m

        W = F * d  # 仕事J
        questions.append(
            {
                "F": F,
                "d": d,
                "W": W,
            }
        )
    return questions


# --- セッション状態の初期化 ---
if "questions" not in st.session_state:
    st.session_state.questions = generate_questions(NUM_QUESTIONS)

if "checked" not in st.session_state:
    st.session_state.checked = False


# --- ボタン：新しい問題を作る ---
if st.button("🔄 新しい問題を作る"):
    st.session_state.questions = generate_questions(NUM_QUESTIONS)
    st.session_state.checked = False
    # 入力値リセット
    for i in range(NUM_QUESTIONS):
        key = f"ans_{i}"
        if key in st.session_state:
            del st.session_state[key]


st.subheader("問題（5問）")
st.write("単位にも注意して答えましょう。（答えは J で入力）")

# 採点後に解説を表示するか
show_explanation = st.checkbox("採点後に解説も表示する", value=True)

# --- 問題を表示 ---
for i, q in enumerate(st.session_state.questions):
    st.markdown(f"### 第 {i+1} 問")
    st.write(
        f"大きさ **{q['F']} N** の力で物体を **{q['d']} m** 動かしたときの **仕事** は何 J か。"
    )

    st.number_input(
        "答え（J）を入力",
        key=f"ans_{i}",
        step=1.0,
        format="%.2f",
    )
    st.divider()


# --- 採点ボタン ---
if st.button("✅ 採点する"):
    st.session_state.checked = True

    correct_count = 0
    results = []

    for i, q in enumerate(st.session_state.questions):
        user_key = f"ans_{i}"
        user_answer = st.session_state.get(user_key, None)

        if user_answer is None:
            is_correct = False
        else:
            # 小数誤差 ±0.01 までは正解扱い
            is_correct = abs(user_answer - q["W"]) < 0.01

        if is_correct:
            correct_count += 1

        results.append(
            {
                "index": i + 1,
                "F": q["F"],
                "d": q["d"],
                "W": q["W"],
                "user": user_answer,
                "is_correct": is_correct,
            }
        )

    st.subheader("採点結果")
    st.write(f"👉 5問中 **{correct_count} 問正解** です。")

    # --- 各問題の結果と解説 ---
    for r in results:
        if r["is_correct"]:
            st.markdown(f"#### 第 {r['index']} 問：✅ 正解！")
        else:
            st.markdown(f"#### 第 {r['index']} 問：❌ 不正解")

        st.write(f"- あなたの答え： {r['user']} J")

        if show_explanation:
            st.write(
                f"- 正解： {r['W']} J  \n"
                f"- 計算： W = F × d = {r['F']} N × {r['d']} m = {r['W']} J"
            )

        st.divider()

else:
    if st.session_state.checked:
        st.info("「🔄 新しい問題を作る」を押すと、別の5問が出題されます。")
