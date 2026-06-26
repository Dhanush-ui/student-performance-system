import streamlit as st
import pandas as pd
import plotly.express as px
import database
import data_processor

st.set_page_config(
    page_title="Student Performance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
database.init_db()

CUSTOM_CSS = """
<style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }

    div[data-testid="stMetric"] {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1rem 1.25rem;
    }

    div[data-testid="stMetricLabel"] { font-weight: 600; color: #4B5563; }

    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E5E7EB;
    }

    h1, h2, h3 { color: #1F2937; }

    .page-subtitle {
        color: #6B7280;
        font-size: 0.95rem;
        margin-top: -0.6rem;
        margin-bottom: 1.2rem;
    }

    .grade-badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.85rem;
        color: white;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

GRADE_COLORS = {
    "A": "#16A34A",
    "B": "#2563EB",
    "C": "#D97706",
    "D": "#EA580C",
    "F": "#DC2626",
}

NAV_ITEMS = {
    "Upload & Import": "📤",
    "Dashboard": "📊",
    "Manage Students": "🛠️",
    "Search": "🔍",
}

with st.sidebar:
    st.markdown("## 🎓 Student Performance")
    st.caption("Analytics & Management System")
    st.divider()
    page = st.radio(
        "Navigate",
        list(NAV_ITEMS.keys()),
        format_func=lambda label: f"{NAV_ITEMS[label]}  {label}",
        label_visibility="collapsed",
    )
    st.divider()
    rows, _ = database.get_all_students()
    st.caption(f"📦 {len(rows)} records in database")


def rows_to_df(rows, columns):
    return pd.DataFrame(rows, columns=columns)


def grade_badge_html(letter):
    color = GRADE_COLORS.get(letter, "#6B7280")
    return f'<span class="grade-badge" style="background-color:{color}">{letter}</span>'


def page_header(title, subtitle, icon):
    st.markdown(f"# {icon} {title}")
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)


if page == "Upload & Import":
    page_header(
        "Upload & Import CSV",
        "Bring in a student performance dataset and load it into the database.",
        "📤",
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = data_processor.load_csv(uploaded_file)
        st.success(f"✅ File loaded — {len(df)} valid rows after cleaning.")

        with st.expander("Preview cleaned data", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📥 Import to Database", type="primary", use_container_width=True):
                count = data_processor.import_dataframe_to_db(df)
                st.success(f"Imported {count} student records into the database.")
                st.balloons()
    else:
        st.info("👆 Upload a CSV file to get started.")

elif page == "Dashboard":
    page_header(
        "Dashboard",
        "Overview of student performance across the imported dataset.",
        "📊",
    )
    rows, columns = database.get_all_students()

    if not rows:
        st.warning("No data yet. Go to **Upload & Import** first.")
    else:
        df = rows_to_df(rows, columns)

        with st.expander("🔎 Filters", expanded=False):
            f1, f2, f3 = st.columns(3)
            with f1:
                gender_filter = st.multiselect(
                    "Gender", sorted(df["gender"].unique()), default=list(df["gender"].unique())
                )
            with f2:
                support_filter = st.multiselect(
                    "Parental Support", sorted(df["parental_support"].unique()),
                    default=list(df["parental_support"].unique()),
                )
            with f3:
                status_filter = st.radio("Status", ["All", "Passing", "Failing"], horizontal=True)

        df = df[df["gender"].isin(gender_filter) & df["parental_support"].isin(support_filter)]
        if status_filter == "Passing":
            df = df[df["is_passing"] == 1]
        elif status_filter == "Failing":
            df = df[df["is_passing"] == 0]

        if df.empty:
            st.info("No records match the selected filters.")
            st.stop()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total Students", len(df))
        col2.metric("📈 Average Final Grade", round(df["final_grade"].mean(), 2))
        col3.metric("✅ Pass Rate", f"{round(df['is_passing'].mean() * 100, 1)}%")
        col4.metric("📚 Avg Study Hrs/Week", round(df["study_hours_per_week"].mean(), 1))

        st.divider()

        chart_row1_left, chart_row1_right = st.columns(2)
        with chart_row1_left:
            st.subheader("Grade Letter Distribution")
            grade_counts = df["grade_letter"].value_counts().reset_index()
            grade_counts.columns = ["grade_letter", "count"]
            fig = px.bar(
                grade_counts, x="grade_letter", y="count", color="grade_letter",
                color_discrete_map=GRADE_COLORS, text="count",
            )
            fig.update_layout(showlegend=False, xaxis_title="Grade", yaxis_title="Students")
            st.plotly_chart(fig, use_container_width=True)

        with chart_row1_right:
            st.subheader("Pass vs Fail Breakdown")
            status_counts = df["is_passing"].map({1: "Passing", 0: "Failing"}).value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            fig = px.pie(
                status_counts, names="status", values="count", hole=0.45,
                color="status", color_discrete_map={"Passing": "#16A34A", "Failing": "#DC2626"},
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        chart_row2_left, chart_row2_right = st.columns(2)
        with chart_row2_left:
            st.subheader("Final Grade Distribution")
            fig = px.histogram(df, x="final_grade", nbins=20, color_discrete_sequence=["#4F46E5"])
            fig.update_layout(xaxis_title="Final Grade", yaxis_title="Number of Students")
            st.plotly_chart(fig, use_container_width=True)

        with chart_row2_right:
            st.subheader("Average Grade by Gender")
            gender_avg = df.groupby("gender")["final_grade"].mean().reset_index()
            fig = px.bar(
                gender_avg, x="gender", y="final_grade", color="gender", text_auto=".1f",
            )
            fig.update_layout(showlegend=False, xaxis_title="Gender", yaxis_title="Average Final Grade")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Study Hours vs Final Grade")
        fig = px.scatter(
            df, x="study_hours_per_week", y="final_grade", color="grade_letter",
            color_discrete_map=GRADE_COLORS, size="attendance_rate",
            hover_data=["name", "parental_support"],
            labels={"study_hours_per_week": "Study Hours / Week", "final_grade": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Final Grade by Parental Support")
        fig = px.box(
            df, x="parental_support", y="final_grade", color="parental_support",
            labels={"parental_support": "Parental Support", "final_grade": "Final Grade"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        col_top, col_bottom = st.columns(2)
        with col_top:
            st.subheader("🏆 Top 5 Students")
            st.dataframe(
                df.sort_values("final_grade", ascending=False).head(5)[
                    ["name", "final_grade", "grade_letter"]
                ],
                use_container_width=True,
                hide_index=True,
            )
        with col_bottom:
            st.subheader("⚠️ Bottom 5 Students (At Risk)")
            st.dataframe(
                df.sort_values("final_grade", ascending=True).head(5)[
                    ["name", "final_grade", "grade_letter"]
                ],
                use_container_width=True,
                hide_index=True,
            )

elif page == "Manage Students":
    page_header(
        "Manage Students",
        "View, edit, or remove individual student records.",
        "🛠️",
    )
    rows, columns = database.get_all_students()

    if not rows:
        st.warning("No data yet. Go to **Upload & Import** first.")
    else:
        df = rows_to_df(rows, columns)

        with st.expander(f"📋 All Records ({len(df)})", expanded=True):
            st.dataframe(df, use_container_width=True, hide_index=True)

        tab_edit, tab_delete = st.tabs(["✏️ Edit Grade", "🗑️ Delete Record"])

        with tab_edit:
            student_ids = df["id"].tolist()
            selected_id = st.selectbox(
                "Select record ID", student_ids, key="edit_select",
                format_func=lambda i: f"#{i} — {df[df['id'] == i].iloc[0]['name']}",
            )
            selected_row = df[df["id"] == selected_id].iloc[0]

            col1, col2 = st.columns([2, 1])
            with col1:
                new_grade = st.number_input(
                    "New Final Grade", min_value=0.0, max_value=100.0,
                    value=float(selected_row["final_grade"]),
                )
            with col2:
                st.markdown("Current grade")
                st.markdown(grade_badge_html(selected_row["grade_letter"]), unsafe_allow_html=True)

            if st.button("💾 Update Grade", type="primary"):
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

        with tab_delete:
            delete_id = st.selectbox(
                "Select record ID to delete", student_ids, key="delete_select",
                format_func=lambda i: f"#{i} — {df[df['id'] == i].iloc[0]['name']}",
            )
            st.warning("This action cannot be undone.")
            if st.button("🗑️ Delete Record", type="primary"):
                database.delete_student(int(delete_id))
                st.success("Record deleted.")
                st.rerun()

elif page == "Search":
    page_header(
        "Search Student",
        "Look up a student record by name.",
        "🔍",
    )
    name_query = st.text_input("Enter student name", placeholder="e.g. John")

    if name_query:
        rows, columns = database.search_student_by_name(name_query)
        if not rows:
            st.info("No matching students found.")
        else:
            df = rows_to_df(rows, columns)
            st.success(f"Found {len(df)} matching record(s).")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("👆 Start typing a name to search.")
