import streamlit as st
import pandas as pd
import nltk
import time 
from pathlib import Path
from pdf_tools.extract_text import load_text_auto
from pdf_tools.parse_result import analyze_text
from graph_utils import create_prerequisite_graph

st.set_page_config(layout="wide")
st.title("AUTOMATIC METADATA TAGGING IN TEXTUAL LEARNING OBJECTS")

CSV = "major-project-data-word (1).csv"

tab1, tab2 = st.tabs(["Analyze", "History"])


# ==============================
# TAB 1 — ANALYZE
# ==============================
with tab1:

    file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"])

    if file:
        path = Path("uploads") / file.name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(file.getbuffer())

        if st.button("Analyze"):

            # START TIME
            start_time = time.time()

            text = load_text_auto(str(path))
            result = analyze_text(text, CSV)

            # END TIME
            end_time = time.time()
            total_time = round(end_time - start_time, 4)

            # TERMINAL OUTPUT
            print("\n====================================")
            print(" FILE ANALYSIS COMPLETED")
            print(f" File: {file.name}")
            print(f" TOTAL PROCESSING TIME: {total_time} seconds")
            print("====================================\n")

            result["file_name"] = file.name

            st.session_state["last"] = result

            if "history" not in st.session_state:
                st.session_state["history"] = {}

            st.session_state["history"][file.name] = result

            # ---------------- MERGED PREREQUISITES + ORDER ----------------
            # ---------------- MERGED PREREQUISITES + ORDER (UPGRADED UI) ----------------
            st.subheader("Step-by-Step Learning Order")

            if not result["learning_order"]:
                st.warning("No prerequisites detected.")
            else:
                # Format as a visual breadcrumb trail: A ➔ B ➔ C
                path_steps = [f"**{topic.title()}**" for topic in result["learning_order"]]
                visual_path = " ➔ ".join(path_steps)
                
                # Display inside a highlighted info box
                st.info(visual_path)

            # ---------------- LEARNING PATH (UPGRADED UI) ----------------
            st.subheader("Concept Relationships")

            if result.get("relations"):
                # Create a clean layout for the relationships
                for i, (c1, c2) in enumerate(result["relations"]):
                    st.markdown(f"🔹 **{c1.title()}** is required to understand **{c2.title()}**")
            else:
                st.write("No structured learning path generated.")
            
            # ---------------- GRAPH VISUALIZATION (STATIC MATPLOTLIB) ----------------
            st.subheader("Prerequisite Relationship Graph")

            prereq_dict = {}

            if result.get("relations"):
                for c1, c2 in result["relations"]:
                    if c2 not in prereq_dict:
                        prereq_dict[c2] = []
                    prereq_dict[c2].append(c1)

            if prereq_dict:
                fig = create_prerequisite_graph(prereq_dict)
                st.pyplot(fig)
            else:
                st.warning("No graph could be generated.")

            # ---------------- ROADMAP (WITH WIKI LINKS) ----------------
            st.subheader("Study Roadmap")

            if not result["study_roadmap"]:
                st.warning("No roadmap generated.")
            else:
                for item in result["study_roadmap"]:
                    topic_name = item.get("topic", "Concept")

                    with st.expander(topic_name):
                        st.markdown("**Definition:**")
                        st.write(item.get("definition", ""))
                        
                        # Show the Wikipedia link if it exists
                        if item.get("url"):
                            st.markdown(f"[🔗 Read more on Wikipedia]({item['url']})")


# ==============================
# TAB 2 — HISTORY
# ==============================
with tab2:

    st.subheader("Previously Analyzed Files")

    if "history" not in st.session_state or not st.session_state["history"]:
        st.info("No files analyzed yet.")
    else:
        for fname in st.session_state["history"]:

            if st.button(fname):

                selected = st.session_state["history"][fname]

                st.success(f"Opened: {fname}")

                # ---------------- MERGED PREREQUISITES + ORDER ----------------
                # ---------------- MERGED PREREQUISITES + ORDER (UPGRADED UI) ----------------
            st.subheader("Step-by-Step Learning Order")

            if not result["learning_order"]:
                st.warning("No prerequisites detected.")
            else:
                # Format as a visual breadcrumb trail: A ➔ B ➔ C
                path_steps = [f"**{topic.title()}**" for topic in result["learning_order"]]
                visual_path = " ➔ ".join(path_steps)
                
                # Display inside a highlighted info box
                st.info(visual_path)

            # ---------------- LEARNING PATH (UPGRADED UI) ----------------
            st.subheader(" Concept Relationships")

            if result.get("relations"):
                # Create a clean layout for the relationships
                for i, (c1, c2) in enumerate(result["relations"]):
                    st.markdown(f"🔹 **{c1.title()}** is required to understand 🔓 **{c2.title()}**")
            else:
                st.write("No structured learning path generated.")

                # ---------------- GRAPH VISUALIZATION (STATIC MATPLOTLIB) ----------------
                st.subheader("Prerequisite Relationship Graph")

                prereq_dict = {}

                if selected.get("relations"):
                    for c1, c2 in selected["relations"]:
                        if c2 not in prereq_dict:
                            prereq_dict[c2] = []
                        prereq_dict[c2].append(c1)

                if prereq_dict:
                    fig = create_prerequisite_graph(prereq_dict)
                    st.pyplot(fig)
                else:
                    st.warning("No graph could be generated.")

                # ---------------- ROADMAP (WITH WIKI LINKS) ----------------
                st.subheader("Study Roadmap")

                for item in selected["study_roadmap"]:
                    topic_name = item.get("topic", "Concept")

                    with st.expander(topic_name):
                        st.markdown("**Definition:**")
                        st.write(item.get("definition", ""))
                        
                        # Show the Wikipedia link if it exists
                        if item.get("url"):
                            st.markdown(f"[🔗 Read more on Wikipedia]({item['url']})")