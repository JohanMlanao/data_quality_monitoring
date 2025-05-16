import streamlit as st


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"<h1 style='color:#4CAF50;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<h4 style='color:gray;'>{subtitle}</h4>", unsafe_allow_html=True)
    st.markdown("---")


def show_footer():
    st.markdown(
        """<hr style="margin-top: 3em;">
    <div style="text-align: center; color: gray;">
        Built with ❤️ using Streamlit • <a href="https://github.com/JohanMlanao/data_quality_monitoring" target="_blank">GitHub Repo</a>
    </div>
    """,
        unsafe_allow_html=True,
    )
