# ===============================================================
# SOC SKILL HUB HACKATHON 2K25
# Theme: Information Technology
# Project ID: SHIT09
# Title: Simple Attendance Tracker (Enhanced Student Details)
# ---------------------------------------------------------------
# Developer: KAVYAVARSHINI | B.Tech AI&DS | SSMIET
# ===============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ------------------- CONFIGURATION -------------------
st.set_page_config(page_title="Simple Attendance Tracker", page_icon="✅", layout="centered")
st.title("📋 Simple Attendance Tracker ")
#st.caption("SOC Skill Hub Hackathon 2K25 — Theme: Information Technology")

FILENAME = "attendance_records.csv"

# ------------------- SIDEBAR SETTINGS -------------------
st.sidebar.header("⚙️ Configuration")
num_students = st.sidebar.number_input("Number of Students", min_value=1, max_value=100, value=10, step=1)
st.sidebar.info("You can set between 1 and 100 students.")

st.subheader(f"🧑‍🎓 Enter Details for {num_students} Students")

# ------------------- INPUT SECTION -------------------
students = []
for i in range(num_students):
    cols = st.columns([2, 1])
    with cols[0]:
        name = st.text_input(f"Student {i+1} Name", key=f"name_{i}")
    with cols[1]:
        status = st.selectbox("Status", ["Select", "Present", "Absent"], key=f"status_{i}")
    students.append((name, status))

# ------------------- SAVE & GENERATE REPORT -------------------
if st.button("✅ Generate Attendance Report"):
    missing_names = [i + 1 for i, (name, _) in enumerate(students) if not name.strip()]
    if missing_names:
        st.warning(f"⚠️ Please enter names for students: {', '.join(map(str, missing_names))}")
    else:
        present_count = sum(1 for _, s in students if s.lower() == "present")
        absent_students = [n for n, s in students if s.lower() == "absent"]
        attendance_percent = int(round((present_count / num_students) * 100))
        absent_str = ", ".join(absent_students) if absent_students else "None"

        st.success("✅ Attendance Report Generated Successfully!")
        st.markdown("---")
        st.markdown(f"**Absent:** {absent_str}")
        st.markdown(f"**Attendance:** {attendance_percent}%")

        # AI Feedback
        if attendance_percent < 75:
            st.error("⚠️ Attendance below 75%! Students need improvement.")
        elif attendance_percent < 90:
            st.warning("🙂 Good, but can be improved!")
        else:
            st.success("🎉 Excellent class attendance!")

        st.markdown("---")

        # Save to CSV
        df = pd.DataFrame(students, columns=["Student Name", "Status"])
        today = date.today().strftime("%d-%m-%Y")
        df["Date"] = today
        try:
            existing_df = pd.read_csv(FILENAME)
            final_df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            final_df = df
        final_df.to_csv(FILENAME, index=False)
        st.success(f"💾 Attendance saved for {today}!")

        # Pie chart
        st.subheader("📈 Attendance Visualization")
        fig, ax = plt.subplots()
        ax.pie([present_count, num_students - present_count],
               labels=["Present", "Absent"],
               autopct="%1.1f%%",
               colors=["#6fdc6f", "#ff6961"])
        st.pyplot(fig)

# ------------------- STUDENT-SPECIFIC DETAILS -------------------
st.markdown("---")
st.subheader("🎯 Check Specific Student Attendance Record")

if st.button("📂 Load Attendance Data"):
    try:
        records = pd.read_csv(FILENAME)
        st.dataframe(records)

        # Student search
        search_name = st.text_input("🔍 Enter Student Name to Check:")
        if search_name:
            student_data = records[records["Student Name"].str.lower() == search_name.strip().lower()]
            if not student_data.empty:
                total_days = student_data["Date"].nunique()
                present_days = (student_data["Status"].str.lower() == "present").sum()
                absent_days = (student_data["Status"].str.lower() == "absent").sum()
                percent = int(round((present_days / total_days) * 100))

                st.success(f"✅ Attendance Record for **{search_name.title()}**")
                st.markdown(f"- Total Days Recorded: **{total_days}**")
                st.markdown(f"- Present: **{present_days}** days")
                st.markdown(f"- Absent: **{absent_days}** days")
                st.markdown(f"- Attendance Percentage: **{percent}%**")

                if percent < 75:
                    st.error("⚠️ Attendance below 75%! Needs improvement.")
                else:
                    st.success("👍 Good attendance record!")

            else:
                st.warning(f"No attendance data found for '{search_name}'. Please check spelling.")
        
        # ------------------- OVERALL ATTENDANCE -------------------
        st.markdown("---")
        st.subheader("📊 Overall Attendance Summary")

        grouped = records.groupby("Student Name")["Status"].apply(
            lambda x: (x.str.lower() == "present").sum() / len(x) * 100
        ).reset_index(name="Attendance %")

        st.dataframe(grouped)

        overall_avg = round(grouped["Attendance %"].mean(), 2)
        st.info(f"🌍 **Overall Class Attendance Average:** {overall_avg}%")

    except FileNotFoundError:
        st.warning("⚠️ No attendance records found yet.")

# ------------------- FOOTER -------------------
st.markdown("---")
st.caption("Developed by **KAVYAVARSHINI | B.Tech AI&DS | SSMIET**")

