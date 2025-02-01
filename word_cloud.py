import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import base64
import io
import plotly.express as px

def download_plot(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="wordcloud.png">Download Word Cloud</a>'
    return href

def download_csv(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    return href

def read_file(file):
    if file is not None:
        if file.type == "application/pdf":
            # Read PDF file
            from PyPDF2 import PdfReader
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Read DOCX file
            import docx
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        elif file.type == "text/plain":
            # Read TXT file
            return file.read().decode("utf-8")
    return ""

def remove_stopwords(text):
    stopwords = set(STOPWORDS)
    return " ".join([word for word in text.split() if word.lower() not in stopwords])

# Streamlit code
st.title("Word Cloud Application")
st.write("This is a simple Word Cloud application to generate a word cloud from the text data.")
st.subheader("Created by Wazir Kifayat")

# Upload the PDF, DOCX, or TXT file
file = st.file_uploader("Upload a PDF, DOCX, or TXT file")

# Check the uploaded file type and read the file
text = read_file(file)

if text:
    # Remove the stopwords from the text
    text = remove_stopwords(text)

    # Create the word cloud
    wordcloud = WordCloud(width=800, height=400, stopwords=STOPWORDS, background_color="white").generate(text)

    # Plot the word cloud
    st.image(wordcloud.to_array())

    # Generate word cloud
    wordcloud = WordCloud().generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Display the word cloud
    st.markdown(download_plot(fig), unsafe_allow_html=True)
    # Create a download link for the text
    st.markdown(download_csv(pd.DataFrame(text.split(), columns=["Words"])), unsafe_allow_html=True)
    # Display the word cloud
    st.write("Word Cloud:")
    st.pyplot(fig)
    # Display the word frequency
    st.write("Word Frequency:")
    st.write(pd.Series(text.split()).value_counts())
    # Display the word frequency plot
    fig = px.bar(pd.Series(text.split()).value_counts(), x=pd.Series(text.split()).value_counts().index, y=pd.Series(text.split()).value_counts().values)
    st.plotly_chart(fig)

    # Add balloons
    st.balloons()
else:
    st.write("Please upload a file to generate a word cloud.")

# Add the footer
st.write("Thank you for using this application!")