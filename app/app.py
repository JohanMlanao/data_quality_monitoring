import streamlit as st

pg = st.navigation(
    {
        "Pages": [
            st.Page("homepage.py", title="Home page", icon=":material/home:"),
            st.Page(
                "visualisation.py",
                title="Data Visualisation",
                icon=":material/dashboard:",
            ),
        ]
    }
)
pg.run()
