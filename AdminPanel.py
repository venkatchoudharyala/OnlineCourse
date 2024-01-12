import streamlit as st
import os
import json
import datetime
import pytz

def main():
        tab1, tab2 = st.tabs(["Students", "Sets"])
        with tab1:
                Scrapper()
        with tab2:
                SetsPanel()
def Scrapper():
        dir = os.listdir("UserAcc")
        dir.remove("Admin.ua")
        dir.remove("test.ua")
        with st.expander("Students"):
                MPath = st.selectbox("Users", dir, key = "AdminP", label_visibility = "collapsed")
                if MPath:
                        Path = "UserAcc/" + MPath
                        st.write(FileReader(MPath))
        with st.expander("Authorizations"):
                UnvPath = "LoginApp/UnVerified.uv"
                NewUsers = FileReader(UnvPath)
                if len(NewUsers["Names"]) != 0:
                        st.error("User Name: " + NewUsers["Names"][0])
                        StudFilePath = "UserAcc/" + NewUsers["Names"][0] + ".ua"
                        k = FileReader(StudFilePath)
                        st.error("Email: " + k["Email"])
                        SetDirs = os.listdir("YTCourse")
                        Role = st.selectbox("Select Role", SetDirs, index = None, key = NewUsers["Names"][0])
                        col1, col2 = st.columns(2)
                        with col1:
                                if st.button("Verify") and Role != None:
                                        Name = NewUsers["Names"][0]
                                        del NewUsers["Names"][0]
                                        FileWriter(UnvPath, NewUsers)

                                        Path = "UserAcc/" + Name + ".ua"
                                        UDetails = FileReader(Path)

                                        UDetails["Set"] = Role
                                        UDetails["AccVerifStatus"] = "Verified"
                                        FileWriter(Path, UDetails)
                                        st.experimental_rerun()
                        with col2:
                                if st.button("Suspend"):
                                        with open("LoginApp/UnVerified.uv", "r") as File:
                                                UDetails = json.load(File)
                                        with open("LoginApp/UnVerified.uv", "w") as File:
                                                del NewUsers["Names"][0]
                                                json.dump(NewUsers, File)
                                        st.experimental_rerun()
                else:
                        st.success("No pending Authorizations left")


def SetsPanel():
        Sets = os.listdir("YTCourse/")
        with st.expander("YTCourse Sets"):
                if len(Sets) == 0:
                        st.error("No Sets uploaded yet")
                else:
                        SelSet = st.selectbox("Select a Set", Sets)
                        SelSetFile = FileReader("YTCourse/" + SelSet)
                        for i in SelSetFile["VideoLinks"]:
                                st.write(i)
                        UpdateSet(SelSet)

        with st.expander("Create New Set"):
                with st.form("NewSet", clear_on_submit = True, border = False):
                        SetName = st.text_input("Enter the Name of the Set")
                        Links = []
                        if st.form_submit_button("Create Set"):
                                Path = "YTCourse/" + SetName + ".sf"
                                with open(Path, "w") as File:
                                        json.dump({"VideoLinks": Links, "CreationTime": str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")))}, File)
                                st.success("New Set: " + SetName + ", Created Successfully", icon = "✅")


def FileReader(Path):
        with open(Path, "r") as File:
                Data = json.load(File)
        return Data

def FileWriter(Path, Data):
        with open(Path, "w") as File:
                json.dump(Data, File)

def UpdateSet(SetName):
        with st.form("New", clear_on_submit = True, border = False):
                LinkName = st.text_input("Enter the Title of the Link")
                LinkID = st.text_input("Enter the Embed Link")
                if st.form_submit_button("SAVE"):
                        Data = FileReader("YTCourse/" + SetName)
                        Data["VideoLinks"].append({"LinkTitle": LinkName, "Link": LinkID, "LinkStamp": str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")))})
                        FileWriter("YTCourse/" + SetName, Data)

if __name__ == "__main__":
        main()
