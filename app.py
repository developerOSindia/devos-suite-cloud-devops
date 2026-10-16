"""
DeveloperOS Cloud & DevOps Suite - Interactive Application
"""

import streamlit as st
from core.cron import explain_cron_expression
from ui.components import render_suite_header, render_suite_footer, render_main_promotional_banner

st.set_page_config(
    page_title="DeveloperOS - Cloud & DevOps Suite",
    page_icon="☁️",
    layout="wide",
)


def main():
    render_suite_header(
        title="Cron Expression Explainer & Parser",
        description="Decode standard 5-part crontab expressions into human-readable plain English schedules instantly.",
    )

    cron_expr = st.text_input("Enter Cron Expression (5 parts):", value="*/15 0,12 * * 1-5")

    if cron_expr:
        res = explain_cron_expression(cron_expr)

        if res["is_valid"]:
            st.success("Valid Cron Expression")
            st.markdown(f"### Schedule: `{res['human_readable']}`")

            col1, col2, col3, col4, col5 = st.columns(5)
            p = res["parts"]
            col1.metric("Minute", p["minute"])
            col2.metric("Hour", p["hour"])
            col3.metric("Day (Month)", p["day_of_month"])
            col4.metric("Month", p["month"])
            col5.metric("Day (Week)", p["day_of_week"])
        else:
            st.error(res["error"])

    render_main_promotional_banner()
    render_suite_footer()


if __name__ == "__main__":
    main()
