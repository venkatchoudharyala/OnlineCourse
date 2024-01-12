import streamlit as st
import json
import time
from LoginApp import Page
import datetime
import warnings
import os
import datetime
import pytz
from CryptTech import Recipes
import AdminPanel as ap
import pandas as pd
import Emailer

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
		Role = UserDetails["Role"]
		Status = UserDetails["AccVerifStatus"]
		if UserName == "Admin":
			ap.main()
		else:
			if Role == "Lead" and Status == "Verified":
				tab1, tab2, tab3, tab4 = st.tabs(["Projects", "New Project", "Meetings", "New Meeting"])
				with tab1:
					LeadPanel()
				with tab2:
					CreateProject()
				with tab3:
					MeetingPanel()
				with tab4:
					Projects = UserDetails["Projects"]
					project = st.selectbox("Select a Project", Projects, index = None, key = "p")
					if project != None:
						k = os.listdir("MeetingNotes/" + project)
						CreateMeetSession(project, len(k))
					
			elif Role == "Member" and Status == "Verified":
				tab1, tab2 = st.tabs(["Projects", "Meetings"])
				with tab1:
					MemberPanel()
				with tab2:
					MeetingPanel()
			else:
				path = "LoginApp/UnVerified.uv"
				with open(path, "r") as File:
					k = json.load(File)
				if UserName not in k["Names"]:
					st.error("Your Account Creation was Suspended")
				else:
					st.error("Still in Review, You are not Authorized Yet!!")

def FileReader(Path):
	with open(Path, "r") as File:
		PjDetails = json.load(File)
	return PjDetails

def FileWriter(Path, Details):
	with open(Path, "w") as File:
		json.dump(Details, File)
		

if __name__ == "__main__":
	main()
