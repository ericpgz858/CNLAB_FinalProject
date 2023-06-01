import streamlit as st
from streamlit_webrtc import webrtc_streamer
from streamlit_extras.switch_page_button import switch_page
import cv2
import av
import queue
import os
from time import sleep
from PIL import Image
import requests
result_queue = queue.Queue()
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)
st.set_page_config(
    page_title="detect",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
pred=0
par=st.experimental_get_query_params()
if par.get("class"):
    #st.write(par)
    #st.write(par.get("name")[0])
    #st.write(par.get("class")[0])
    have_class=1
    personclass=par.get("class")[0]
    personclassname=par.get("classname")[0]
    st.write("class is: ",personclassname)
    st.text_input("Your name", key="name")
    if 'name' in st.session_state and st.session_state["name"]!="":
        have_name=1
        personname=st.session_state["name"]
        face_cascade=cv2.CascadeClassifier("/home/ubuntu/face_r/data/haarcascade_frontalface_default.xml")
        filepath=f"/home/ubuntu/face_r/data/classifiers/{personname}_classifier.xml"
        if os.path.isfile(filepath):
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(f"/home/ubuntu/face_r/data/classifiers/{personname}_classifier.xml")
            st.write("your name is: ",personname)
        else:
            st.write("you did not have a classifier")
            #if st.button("create a classifier"):
                #nav_to("https://18.181.158.90:8502")

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        frm=frame.to_ndarray(format="bgr24")
        global pred
        if have_name and have_class:
            #print(personname)
            #default_img = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h,x:x+w]
                id,confidence = recognizer.predict(roi_gray)
                confidence = 100 - int(confidence)
                if confidence > 50:
                    pred += +1
                    text = personname.upper()
                    font = cv2.FONT_HERSHEY_PLAIN
                    frm = cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frm = cv2.putText(frm, text, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                else:   
                    pred += -1
                    text = "UnknownFace"
                    font = cv2.FONT_HERSHEY_PLAIN
                    frm = cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    frm = cv2.putText(frm, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)
                result_queue.put(pred)
        return av.VideoFrame.from_ndarray(frm,format='bgr24')
#webrtc_streamer(key="sample",video_processor_factory=VideoProcessor,media_stream_constraints={"video": True, "audio": False},)
ctx=webrtc_streamer(key="sample",video_frame_callback=video_frame_callback, media_stream_constraints={"video": True, "audio": False},async_processing=True,)
if ctx.state.playing:
    while True:
        if not result_queue.empty():
            result=result_queue.get()
            if result > 10:
                st.write("success")
                url="http://18.181.158.90:8000/main/test/"
                myobj={'name':personname,'class':personclass}
                x=requests.post(url,data=myobj)
                #switch_page("success")
                nav_to("http://18.181.158.90:8000/main/home")
                break
#if st.button("recreate classifier"):
    #switch_page("testapp")
#也能當成功後直接redirect
st.write(f'''
    <a target="_self" href="http://18.181.158.90:8000/main/home">
        <button>
            go to main page
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)