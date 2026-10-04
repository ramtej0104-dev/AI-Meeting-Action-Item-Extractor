import streamlit as st
from extractor import extract_action_items

st.title("AI Meeting Action-Item Extractor")
st.write("Upload a transcript .txt file, or paste one below, and the tool will pull out action items: who owns each task and when it's due.")

uploaded_file = st.file_uploader("Upload a transcript file (.txt)", type=["txt"])

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")
    st.text_area("Meeting transcript", value=transcript, height=300)
else:
    transcript = st.text_area("Meeting transcript", height=300, placeholder="Sarah: Can you send the report by Friday?\nMark: Sure, I'll have it ready by Friday.")

if st.button("Extract action items"):
    if transcript.strip() == "":
        st.warning("Please paste a transcript first.")
    else:
        items = extract_action_items(transcript)

        if not items:
            st.info("No action items were detected in this transcript.")
        else:
            st.subheader(f"Found {len(items)} action item(s)")
            for item in items:
                with st.container(border=True):
                    st.write(f"**Task:** {item['task']}")
                    st.write(f"**Owner:** {item['owner']}  |  **Deadline:** {item['deadline']}  |  **Confidence:** {item['confidence']}%")
                    if item["status"] == "CONFIDENT":
                        st.success("Confident")
                    else:
                        st.warning("Needs review")