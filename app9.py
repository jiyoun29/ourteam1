import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 임베딩 모델 로드
encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 식당 관련 질문과 답변 데이터
questions = [
    "포트폴리오 주제는 뭔가요?",
    "어떤 모델을 사용했나요?",
    "프로젝트 참여 인원은 몇 명인가요?",
    "프로젝트 작업 기간은 어느 정도 인가요?",
    "조장이 누구인가요?",
    "데이터는 무얼 이용 했나요?",
    "프로젝트 하는 데 어려움은 없었나요?"
]

answers = [
    "포트폴리오 주제는 사용자 로그 학습 기반 추천 알고리즘 입니다.",
    "모델로는 NCF를 사용했습니다",
    "참여 인원은 총 3명 입니다.",
    "작업 기간은 3주 입니다.",
    "박찬혁 입니다.",
    "케글에서 영화 데이터를 다운 받아 이용했습니다.",
    "사용자 데이터를 구하기 어려웠습니다. 그래서 직접 생성하여 사용하였습니다."
]

# 질문 임베딩과 답변 데이터프레임 생성
question_embeddings = encoder.encode(questions)
df = pd.DataFrame({'question': questions, '챗봇': answers, 'embedding': list(question_embeddings)})

# 대화 이력을 저장하기 위한 Streamlit 상태 설정
if 'history' not in st.session_state:
    st.session_state.history = []

# 챗봇 함수 정의
def get_response(user_input):
    # 사용자 입력 임베딩
    embedding = encoder.encode(user_input)
    
    # 유사도 계산하여 가장 유사한 응답 찾기
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    # 대화 이력에 추가
    st.session_state.history.append({"user": user_input, "bot": answer['챗봇']})

# Streamlit 인터페이스
st.title("사용자 로그 학습 기반 추천 알고리즘 포트폴리오 챗봇")


# 이미지 표시
st.image("algo.png", caption="Welcome to the Restaurant Chatbot", use_column_width=True)


st.write("포트폴리오에 관한 질문을 입력해보세요. 예: 주제가 무엇인가요?")

user_input = st.text_input("user", "")

if st.button("Submit"):
    if user_input:
        get_response(user_input)
        user_input = ""  # 입력 초기화

# 대화 이력 표시
for message in st.session_state.history:
    st.write(f"**사용자**: {message['user']}")
    st.write(f"**챗봇**: {message['bot']}")
