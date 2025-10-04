import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# PDF Display Options
st.header("📄 How to Display PDFs")

st.subheader("Option 1: Link to an External PDF")
st.markdown("""
You can paste a link to a PDF like this:
```python
st.markdown("[View PDF Document](https://example.com/document.pdf)")
```
Example: [Sample PDF](https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf)
""")

st.subheader("Option 2: Display PDF from URL")
st.markdown("""
To display a PDF inline using an iframe:
```python
pdf_url = "https://example.com/document.pdf"
st.markdown(f'<iframe src="{pdf_url}" width="700" height="1000" type="application/pdf"></iframe>', unsafe_allow_html=True)
```
""")

st.subheader("Option 3: Upload and Display Local PDF")
st.markdown("""
To allow users to upload a PDF file:
```python
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Display the PDF
    st.download_button(
        label="Download PDF",
        data=uploaded_file,
        file_name=uploaded_file.name,
        mime="application/pdf"
    )
```
""")

# Live Example - PDF File Uploader
st.divider()
st.subheader("Try it yourself!")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    st.download_button(
        label="Download PDF",
        data=uploaded_file,
        file_name=uploaded_file.name,
        mime="application/pdf"
    )
