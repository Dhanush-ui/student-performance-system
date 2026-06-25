import streamlit as st
import pandas as pd
import database
import data_processor

st.set_page_config(page_title="Student Performance System", layout="wide")
database.init_db()

st.sidebar.title("Student Performance System")
page = st.sidebar.radio("Navigate", ["Upload & Import", "Dashboard", "Manage Students", "Search"])


def rows_to_df(rows, columns):
    return pd.DataFrame(rows, columns=columns)


if page == "Upload & Import":
    st.title("Upload & Import CSV")
    st.write("Upload the student performance CSV to import it into the database.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = data_processor.load_csv(uploaded_file)
        st.write(f"Preview ({len(df)} valid rows after cleaning):")
        st.dataframe(df.head(10))

        if st.button("Import to Database"):
            count = data_processor.import_dataframe_to_db(df)
            st.success(f"Imported {count} student records into the database.")

elif page == "Dashboard":
    st.title("Dashboard")
    rows, columns = database.get_all_students()

    if not rows:
        st.warning("No data yet. Go to 'Upload & Import' first.")
    else:
        df = rows_to_df(rows, columns)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Students", len(df))
        col2.metric("Average Final Grade", round(df["final_grade"].mean(), 2))
        col3.metric("Pass Rate (%)", round(df["is_passing"].mean() * 100, 2))

        st.subheader("Grade Letter Distribution")
        st.bar_chart(df["grade_letter"].value_counts())

        st.subheader("Top 5 Students")
        st.dataframe(df.sort_values("final_grade", ascending=False).head(5))

        st.subheader("Bottom 5 Students (At Risk)")
        st.dataframe(df.sort_values("final_grade", ascending=True).head(5))

        st.subheader("Average Grade by Gender")
        st.bar_chart(df.groupby("gender")["final_grade"].mean())

elif page == "Manage Students":
    st.title("Manage Students")
    rows, columns = database.get_all_students()

    if not rows:
        st.warning("No data yet. Go to 'Upload & Import' first.")
    else:
        df = rows_to_df(rows, columns)
        st.dataframe(df)

        st.subheader("Edit a Student's Final Grade")
        student_ids = df["id"].tolist()
        selected_id = st.selectbox("Select record ID", student_ids)

        selected_row = df[df["id"] == selected_id].iloc[0]
        new_grade = st.number_input("New Final Grade", min_value=0.0, max_value=100.0,
                                     value=float(selected_row["final_grade"]))

        if st.button("Update Grade"):
            if new_grade >= 90:
                letter = "A"
            elif new_grade >= 80:
                letter = "B"
            elif new_grade >= 70:
                letter = "C"
            elif new_grade >= 60:
                letter = "D"
            else:
                letter = "F"
            is_passing = 1 if new_grade >= 60 else 0
            database.update_student(int(selected_id), new_grade, letter, is_passing)
            st.success("Record updated.")
            st.rerun()

        st.subheader("Delete a Student Record")
        delete_id = st.selectbox("Select record ID to delete", student_ids, key="delete_select")
        if st.button("Delete Record"):
            database.delete_student(int(delete_id))
            st.success("Record deleted.")
            st.rerun()

elif page == "Search":
    st.title("Search Student")
    name_query = st.text_input("Enter student name")

    if name_query:
        rows, columns = database.search_student_by_name(name_query)
        if not rows:
            st.info("No matching students found.")
        else:
            df = rows_to_df(rows, columns)
            st.dataframe(df)
