import re
import altair as alt
import pandas as pd
import streamlit as st
from podcast_utils import fetch_matching_episodes

def get_topic_counts(episodes, keyword):
    title_count = 0
    description_count = 0
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    for ep in episodes:
        if pattern.search(ep.get("title", "")):
            title_count += 1
        if pattern.search(ep.get("description", "")):
            description_count += 1

    return title_count, description_count

st.set_page_config(page_title="PodPulse", page_icon="🎧")
st.title("🎧 PodPulse - Real-Time Podcast Alerts")
st.write("Enter a topic and get the latest podcast episodes about it.")

keyword = st.text_input("🔍 Keyword", "")

if st.button("Find Episodes"):
    if not keyword.strip():
        st.warning("Please enter a keyword.")
    else:
        with st.spinner("Searching..."):
            results = fetch_matching_episodes(keyword)
            if results:
                title_count, description_count = get_topic_counts(results, keyword)

                # One-time keyword appearance chart
                st.subheader("📊 Keyword Appearance Analysis")
                chart_data = pd.DataFrame({
                    'Section': ['Title', 'Description'],
                    'Count': [title_count, description_count]
                })

                chart = alt.Chart(chart_data).mark_bar().encode(
                    x=alt.X("Section", title="Podcast Section"),
                    y=alt.Y("Count", title="Occurrences"),
                    color="Section"
                ).properties(width=400, height=300)

                st.altair_chart(chart, use_container_width=True)

                st.success(f"Found {len(results)} matching episodes!")

                # Show all matching episodes
                for ep in results:
                    st.markdown(f"### {ep['title']}")
                    st.markdown(ep['description'])
                    st.markdown(f"🔗 [Listen Here]({ep['link']})")
                    st.markdown("---")
            else:
                st.info("No matches found.")


