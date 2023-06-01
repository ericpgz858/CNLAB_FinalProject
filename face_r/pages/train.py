import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import numpy as np
from PIL import Image
import os, cv2

st.set_page_config(
    page_title="training",
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

if 'name' in st.session_state and st.session_state["name"]!="":
        personname=st.session_state["name"]
        #st.write("your name is: ",personname)
        progress_text = "training "+personname+"'s classifier"
        my_bar = st.progress(0, text=progress_text)
        #st.write("training ",personname,"'s classifier")
        path = os.path.join("/home/ubuntu/face_r/data/"+personname+"/")
        #st.write("path is: ",path)
        faces = []
        ids = []
        labels = []
        pictures = {}


        # Store images in a numpy format and ids of the user on the same index in imageNp and id lists

        for root,dirs,files in os.walk(path):
                pictures = files

        for pic in pictures :

                imgpath = path+pic
                img = Image.open(imgpath).convert('L')
                imageNp = np.array(img, 'uint8')
                id = int(pic.split(personname)[0])
                #names[name].append(id)
                faces.append(imageNp)
                ids.append(id)

        ids = np.array(ids)

        #Train and save classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        for i in range (1,11):
            my_bar.progress(i, text=progress_text)
        clf.train(faces, ids)
        for i in range (11,101):
            my_bar.progress(i, text=progress_text)
        clf.write("/home/ubuntu/face_r/data/classifiers/"+personname+"_classifier.xml")
        st.session_state["name"]=personname
        switch_page("test")
else:
    switch_page("app")