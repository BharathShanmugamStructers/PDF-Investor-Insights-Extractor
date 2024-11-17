import pdfplumber
import re
import json
from langchain import PromptTemplate, LLMChain
from langchain_groq import ChatGroq
from transformers import pipeline
from google.colab import userdata
GROQ_API_KEY=userdata.get("GROQ_API_KEY")

# Set your Grok API key
grok_api_key = GROQ_API_KEY

# Initialize Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize Grok LLM with LangChain
llm = ChatGroq(api_key=grok_api_key)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from the provided PDF file.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"[INFO] No text found on page {page_num}.")
    return text.strip()

def preprocess_text(text):
    """
    Cleans and preprocesses the extracted text.
    """
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'\n+', '\n', text)  # Remove extra line breaks
    return text.strip()

def split_into_sections(text):
    """
    Splits text into sections based on headings or predefined rules.
    """
    # Example of splitting by common headings
    headings = re.split(
        r"(Future Prospects|Key Changes|Triggers|Material Impacts|Other Information)",
        text,
        flags=re.IGNORECASE
    )
    sections = [headings[i] + headings[i + 1] for i in range(0, len(headings) - 1, 2)]
    if not sections:
        sections = [text]  # Fallback: Treat as one section
    return sections

def summarize_with_huggingface(section):
    """
    Summarizes a section using Hugging Face Transformers.
    """
    chunk_size = 1024
    chunks = [section[i:i + chunk_size] for i in range(0, len(section), chunk_size)]
    
    summary = ""
    for chunk in chunks:
        summarized = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summary += summarized[0]['summary_text'] + " "
    
    return summary.strip()

def analyze_with_grok(summary):
    """
    Performs detailed analysis of the summary using Grok API.
    """
    prompt_template = """
    You are an expert financial analyst. Based on the following summary, extract:
    1. Future growth prospects.
    2. Key changes in the business.
    3. Key triggers (opportunities or risks).
    4. Material impacts on next year's earnings and growth.

    Summary:
    {summary}
    """
    prompt = PromptTemplate(
        input_variables=["summary"],
        template=prompt_template,
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(summary=summary)

def generate_insights_from_pdf(pdf_path):
    """
    Main function to extract and analyze key insights from the PDF.
    """
    # Step 1: Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        raise ValueError("[ERROR] The PDF appears to be empty or text could not be extracted.")

    # Step 2: Preprocess text
    cleaned_text = preprocess_text(raw_text)

    # Step 3: Split text into sections
    sections = split_into_sections(cleaned_text)
    print(f"[INFO] Found {len(sections)} sections for analysis.")

    # Step 4: Analyze each section
    insights = {}
    for idx, section in enumerate(sections, start=1):
        section_title = f"Section {idx}"
        try:
            print(f"\nProcessing {section_title}...")

            # Summarize section
            summary = summarize_with_huggingface(section)
            print(f"[INFO] Summary for {section_title}: {summary}")

            # Analyze summary with Grok
            detailed_insights = analyze_with_grok(summary)
            print(f"[INFO] Detailed analysis for {section_title}: {detailed_insights}")

            insights[section_title] = {
                "Summary": summary,
                "Detailed Insights": detailed_insights
            }
        except Exception as e:
            insights[section_title] = {"Error": str(e)}
            print(f"[ERROR] Failed to process {section_title}: {e}")

    return insights

if __name__ == "__main__":
    # Input PDF file path
    pdf_path =  "company_report.pdf"  # Replace with your PDF file path

    try:
        print("\n[INFO] Extracting insights from PDF...\n")
        insights = generate_insights_from_pdf(pdf_path)

        # Save insights to a JSON file
        output_file = "investor_insights.json"
        with open(output_file, "w") as f:
            json.dump(insights, f, indent=4)

        print(f"\n[INFO] Key insights extracted successfully and saved to {output_file}!")
    except Exception as e:
        print(f"[ERROR] {e}")
