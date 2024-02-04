import streamlit as st
import json
import time
from LoginApp import Page
import datetime
import warnings
import os
import datetime
import pytz
import AdminPanel as ap
import pandas as pd

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

hide_st_style = """
		<style>
		header {visibility: hidden;}
		footer {visibility: hidden;}
  		</style>
  		"""

st.markdown(hide_st_style, unsafe_allow_html = True)

warnings.filterwarnings("ignore")

Page.main()

if "user" in st.session_state:
	UserDetails = st.session_state["user"]
	#st.write(UserDetails)
	st.session_state["LoginVal"] = True
else:
	st.session_state["LoginVal"] = False

def main():
	if st.session_state["LoginVal"]:
		st.session_state['page'] = "MainRoom"
		UserName = UserDetails["Name"]
		Status = UserDetails["AccVerifStatus"]
		if UserName == "Admin":
			ap.main()
		else:
			if Status == "Verified":
				tab1, tab2, tab3 = st.tabs(["Course", "Questionnaire", "Results"])
				with tab1:
					VideoPanel(UserDetails["Set"])
				with tab2:
					QuestionsPanel(UserDetails["Set"])
				with tab3:
					if UserDetails["Result"] == "NO":
						st.error("Please take Test to display your Results")
					else:
						st.success("You have Scored " + UserDetails["Result"])
			else:
				path = "LoginApp/UnVerified.uv"
				k = FileReader(path)
				if UserName not in k["Names"]:
					st.error("Your Account Creation was Suspended")
				else:
					st.error("Still in Review, You are not Authorized Yet!!")

def VideoPanel(Set):
	Path = "YTCourse/" + Set
	Videos = FileReader(Path)
	Seen = int(UserDetails["SeenCount"])
	st.subheader(Videos["VideoLinks"][Seen]["LinkTitle"])
	st.video(Videos["VideoLinks"][Seen]["Link"])
	col1, col2 = st.columns(2)
	with col1:
		if st.button("Previous"):
			if int(Seen) > 0:
				UserDetails["SeenCount"] = str(Seen - 1)
				Path = "UserAcc/" + UserDetails["Name"] + ".ua"
				FileWriter(Path, UserDetails)
				st.rerun()
			else:
				st.error("You are at the first Video")
	with col2:
		if st.button("Next"):
			if int(Seen) == (len(Videos["VideoLinks"]) - 1):
				st.success("You completed the Course", icon = "✅")
			else:
				UserDetails["SeenCount"] = str(Seen + 1)
				Path = "UserAcc/" + UserDetails["Name"] + ".ua"
				FileWriter(Path, UserDetails)
				st.rerun()

def QuestionsPanel(Set):
	length = len(UserDetails["Answers"])
	Path = "YTCourse/" + Set
	SetFile = FileReader(Path)
	if length != len(SetFile["Questions"]):
		Ques = SetFile["Questions"][length]
		with st.form("Questions", clear_on_submit = True):
			st.code(Ques["Question"])
			Answer = st.text_area("Type your Response")
			if st.form_submit_button("Save your Answer"):
				UserDetails["Answers"].append({"Question": Ques["Question"], "Answer": Answer, "Score": 0, "AnswerStamp": str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")))})
				Path = "UserAcc/" + UserDetails["Name"] + ".ua"
				FileWriter(Path, UserDetails)
				st.success("Your Response Saved Successfully", icon = "✅")
				st.rerun()
	else:
		st.success("You Completed the Questionnaire", icon = "✅")
		Path = "UserAcc/" + UserDetails["Name"] + ".ua"
		EvalFile = FileReader(Path)
		Solutions = EvalFile["Answers"]
		FinalScore = 0
		for i in Solutions:
			Score = GeminiEvaluator(i["Question"], i["Answer"])
			i["Score"] = Score
			FinalScore += Score
		EvalFile["Result"] = FinalScore
		FileWriter(Path, EvalFile)

def FileReader(Path):
	with open(Path, "r") as File:
		PjDetails = json.load(File)
	return PjDetails

def FileWriter(Path, Details):
	with open(Path, "w") as File:
		json.dump(Details, File)

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '> ', predicate=lambda _: True)

def GeminiEvaluator(Question, Answer):
	genai.configure(api_key='AIzaSyBE1HLZuDQHbVz1C6MPD9FcvPbkeJqGrQU')
	
	model = genai.GenerativeModel('gemini-pro')
	prompt = "Hey Gemini this is Question: " + Question + " ; and this is the respective Answer: " + Answer + " ; Please evaluate the answer according to the question and just give the marks out of 10 and dont generate anything other than the marks..."
	response = model.generate_content(prompt)
	#Marks = to_markdown(response.text)
	st.write(response.text)
	return int(Marks)

		

if __name__ == "__main__":
	main()
