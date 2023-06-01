from streamlit_webrtc import webrtc_streamer
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import av
import cv2
import os
import queue
st.set_page_config(page_title="main",initial_sidebar_state="collapsed")
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
num_of_images=0
have_name=0
personname=""
path=""
cascade=cv2.CascadeClassifier("/home/ubuntu/face_r/data/haarcascade_frontalface_default.xml")
result_queue = queue.Queue()
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        global num_of_images
        global personname
        global have_name
        global path
        frm=frame.to_ndarray(format="bgr24")
        faces=cascade.detectMultiScale(cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
        for x,y,w,h in faces:
            cv2.rectangle(frm,(x,y),(x+w,y+h),(0,255,0),2)
            new_img=frm[y:y+h, x:x+w]
            if have_name:
                cv2.putText(frm, "Face Detected", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                cv2.putText(frm, str(str(num_of_images)+" images captured"), (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
        #cv2.imshow("FaceDetection", frm)
        if have_name:
            try :
                cv2.imwrite(str(path+"/"+str(num_of_images)+personname+".jpg"), new_img)
                num_of_images += 1
            except :
                pass
        result_queue.put(num_of_images)
        return av.VideoFrame.from_ndarray(frm,format='bgr24')
st.text_input("Your name", key="name")
if 'name' in st.session_state and st.session_state["name"]!="":
        st.write("your name is: ",st.session_state["name"])
        have_name=1
        personname=st.session_state["name"]
        path = "/home/ubuntu/face_r/data/" + st.session_state["name"]
        #print(os.path.realpath('.'))

if 'name' in st.session_state and st.session_state["name"]!="":
    try:
        os.makedirs(path)
    except:
        st.write("Directory Already Created",st.session_state["name"])

#ctx=webrtc_streamer(key="sample",video_processor_factory=VideoProcessor, media_stream_constraints={"video": True, "audio": False},async_processing=True,)
ctx=webrtc_streamer(key="sample",video_frame_callback=video_frame_callback, media_stream_constraints={"video": True, "audio": False},async_processing=True,)
if ctx.state.playing:
    while True:
        if not result_queue.empty():
            result=result_queue.get()
            if result > 50:
                switch_page("train")
#webrtc_streamer(key="sample")
#if st.button("train the model"):
    #switch_page("train")
st.write(f'''
    <a target="_self" href="http://18.181.158.90:8000/main/home">
        <button>
            go to main page
        </button>
    </a>
    ''',
    unsafe_allow_html=True
)
