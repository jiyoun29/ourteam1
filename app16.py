import streamlit as st

# 전체 레이아웃을 넓게 설정
st.set_page_config(layout="wide")

# 제목 설정
st.title("비디오 사물 검출 앱")

# 파일 업로드 버튼을 상단으로 이동
uploaded_file = st.file_uploader("비디오 파일을 업로드하세요", type=["mp4", "mov", "avi"])

# 전체 레이아웃을 컨테이너로 감싸기
with st.container(): # 이 with절이란? 하나의 기능을 하는 코드를 묶어주는 것(가독성 높이기)
    col1, col2 = st.columns(2)  # 열을 균등하게 분배하여 넓게 표시

    with col1:
        st.header("원본 영상") # 영상 제목
        if uploaded_file is not None:  # 못봤음,,
            st.video(uploaded_file) # 영상을 플레이 해라.
        else:
            st.write("원본 영상을 표시하려면 비디오 파일을 업로드하세요.")

    with col2:
        st.header("사물 검출 결과 영상") # 영상 제목
        # 사물 검출 결과가 나타날 자리 확보 및 고정 높이 회색 박스 스타일 추가
        result_placeholder = st.empty()
#       if "processed_video" in st.session_state: # 사물검출 완료된 비디오가 있으면
        if "processed_video" in st.session_state and st.session_state["processed_video"] is not None:
            st.video(st.session_state["processed_video"]) # 그 비디오를 출력해라.
        else:
            result_placeholder.markdown(
                """
                <div style='width:100%; height:620px; background-color:#d3d3d3; display:flex; align-items:center; justify-content:center; border-radius:5px;'>
                    <p style='color:#888;'>여기에 사물 검출 결과가 표시됩니다.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# 사물 검출 버튼 추가
if st.button("사물 검출 실행"): # 사물검출 실행이라는 버튼을 누르면
    if uploaded_file is not None: # upload된 파일이 none이 아니라면, 영상이라면
        # st.session_state["processed_video"] = uploaded_file # 검출된 영상을 사용
        # st.success("사물 검출이 완료되어 오른쪽에 표시됩니다.") # 이메세지 출력
        # 여기에 사물 검출을 수행하는 코드를 추가하고, 결과를 st.session_state["processed_video"]에 저장
        st.session_state["processed_video"] = None  # 실제 결과 영상으로 바꿔야 함
        result_placeholder.markdown(
            "<div style='width:100%; height:500px; background-color:#d3d3d3; display:flex; align-items:center; justify-content:center; border-radius:5px;'>"
            "<p style='color:#888;'>사물 검출 결과 영상이 여기에 표시됩니다.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.success("사물 검출이 완료되어 오른쪽에 표시됩니다.")
    else:
        st.warning("사물 검출을 실행하려면 비디오 파일을 업로드하세요.")
