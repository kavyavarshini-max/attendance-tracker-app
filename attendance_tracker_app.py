# ===============================================================
# SOC SKILL HUB HACKATHON 2K25
# Theme: Information Technology
# Project ID: SHIT09
# Title: Simple Attendance Tracker (100 Students Version)
# ---------------------------------------------------------------
# Developer: Pavithran B (EEE - PSNACET)
# Background:
# A Streamlit-based attendance tracker that can record attendance
# for up to 100 students, visualize results, and save history.
#
# Features:
# ✅ Dynamic student count (1–100)
# ✅ Save attendance to CSV
# ✅ Attendance % and absent list
# ✅ Pie chart visualization
# ✅ View past records
# ✅ AI feedback based on attendance %
# ===============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ------------------- Configuration -------------------
st.set_page_config(page_title="Simple Attendance Tracker", page_icon="✅", layout="centered")

st.title("📋 Simple Attendance Tracker")


FILENAME = "attendance_records.csv"

# ------------------- Step 1: Choose number of students -------------------
st.sidebar.header("⚙️ Configuration")
num_students = st.sidebar.number_input("Number of Students", min_value=1, max_value=100, value=10, step=1)
st.sidebar.info("You can set between 1 and 100 students.")

st.subheader(f"🧑‍🎓 Enter Details for {num_students} Students")

# ------------------- Step 2: Input Section -------------------
students = []
for i in range(num_students):
    cols = st.columns([2, 1])
    with cols[0]:
        name = st.text_input(f"Student {i+1} Name", key=f"name_{i}")
    with cols[1]:
        status = st.selectbox("Status", ["Select", "Present", "Absent"], key=f"status_{i}")
    students.append((name, status))

# ------------------- Step 3: Generate Report -------------------
if st.button("✅ Generate Attendance Report"):
    missing_names = [i+1 for i, (name, _) in enumerate(students) if not name.strip()]
    if missing_names:
        st.warning(f"⚠️ Please enter names for students: {', '.join(map(str, missing_names))}")
    else:
        present_count = sum(1 for _, s in students if s.lower() == "present")
        absent_students = [n for n, s in students if s.lower() == "absent"]
        attendance_percent = int(round((present_count / num_students) * 100))
        absent_str = ", ".join(absent_students) if absent_students else "None"

        # Display results
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

        # Summary table
        df = pd.DataFrame(students, columns=["Student Name", "Status"])
        st.subheader("📊 Attendance Summary")
        st.dataframe(df)

        # ------------------- Save Data to CSV -------------------
        today = date.today().strftime("%d-%m-%Y")
        df["Date"] = today

        try:
            existing_df = pd.read_csv(FILENAME)
            final_df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            final_df = df
        final_df.to_csv(FILENAME, index=False)

        st.success(f"💾 Attendance saved for {today}!")

        # ------------------- Pie Chart -------------------
        st.subheader("📈 Attendance Visualization")
        fig, ax = plt.subplots()
        ax.pie(
            [present_count, num_students - present_count],
            labels=["Present", "Absent"],
            autopct="%1.1f%%",
            colors=["#6fdc6f", "#ff6961"]
        )
        st.pyplot(fig)

        # ------------------- CSV Download Button -------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Today's Attendance as CSV",
            data=csv,
            file_name=f"attendance_{today}.csv",
            mime="text/csv",
        )

# ------------------- Step 4: View Attendance History -------------------
st.markdown("---")
st.subheader("📅 View Attendance History")

if st.button("📂 Load Previous Records"):
    try:
        records = pd.read_csv(FILENAME)
        st.dataframe(records)
        days = records["Date"].nunique()
        st.info(f"📘 Total records available: {days} day(s)")
    except FileNotFoundError:
        st.warning("⚠️ No previous attendance records found yet.")

# ------------------- Footer -------------------
st.markdown("---")
st.caption("Developed by **KAVYAVARSHINI | B.Tech AI&DS | SSMIET**")
