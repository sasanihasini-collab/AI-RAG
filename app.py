import streamlit as st
from pypdf import PdfReader
import re

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI PDF Study Assistant",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📚 AI PDF Study Assistant")
st.write("Upload your PDF and ask questions about it using AI.")

# -----------------------------
# PDF UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📄 Upload your study PDF",
    type=["pdf"]
)

# -----------------------------
# PROCESS PDF
# -----------------------------
if uploaded_file is not None:

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Read PDF
    reader = PdfReader(uploaded_file)

    # Extract text
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # Number of pages
    st.info(f"📄 PDF contains {len(reader.pages)} pages.")

    # -----------------------------
    # VIEW PDF TEXT
    # -----------------------------
    with st.expander("📖 View PDF Text"):
        if text.strip():
            st.write(text)
        else:
            st.warning("No readable text was found in this PDF.")

    # -----------------------------
    # QUESTION INPUT
    # -----------------------------
    question = st.text_input(
        "💬 Ask a question about your PDF"
    )

    # -----------------------------
    # SEARCH BUTTON
    # -----------------------------
    if st.button("🔍 Search PDF"):

        if not question.strip():
            st.warning("⚠️ Please enter a question.")

        elif not text.strip():
            st.error("❌ No readable text was found in the PDF.")

        else:

            # Convert PDF text and question to lowercase
            pdf_text = text.lower()
            user_question = question.lower().strip()

            # Remove common question words
            stop_words = [
                "what",
                "is",
                "are",
                "the",
                "a",
                "an",
                "this",
                "that",
                "about",
                "of",
                "in",
                "on",
                "for",
                "tell",
                "me",
                "give",
                "explain",
                "describe",
                "list",
                "show"
            ]

            # Extract useful keywords
            words = re.findall(r"\b[a-zA-Z0-9]+\b", user_question)

            keywords = [
                word for word in words
                if word not in stop_words and len(word) > 2
            ]

            # -----------------------------
            # FIND RELEVANT INFORMATION
            # -----------------------------
            lines = text.splitlines()

            matched_lines = []

            for line in lines:

                clean_line = line.strip()

                if not clean_line:
                    continue

                line_lower = clean_line.lower()

                # Count matching keywords
                score = 0

                for keyword in keywords:
                    if keyword in line_lower:
                        score += 1

                if score > 0:
                    matched_lines.append((score, clean_line))

            # Sort by relevance
            matched_lines.sort(
                key=lambda x: x[0],
                reverse=True
            )

            # -----------------------------
            # DISPLAY ANSWER
            # -----------------------------
            if matched_lines:

                st.success("✅ Relevant information found in the PDF:")

                # Display best results
                shown = set()

                answer_count = 0

                for score, line in matched_lines:

                    if line not in shown:

                        st.write("• " + line)

                        shown.add(line)

                        answer_count += 1

                    if answer_count >= 8:
                        break

            else:

                # Try searching the complete question
                if user_question in pdf_text:

                    st.success("✅ Your question was found in the PDF.")

                else:

                    st.warning(
                        "⚠️ No exact relevant information was found."
                    )

                    # Show some PDF information
                    st.write("### 📄 Some information from your PDF:")

                    preview = text[:2000]

                    st.write(preview)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption(
    "📚 AI PDF Study Assistant | Upload a PDF and ask questions"
)