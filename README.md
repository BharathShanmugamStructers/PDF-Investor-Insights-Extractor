# **PDF Investor Insights Extractor**

A Python-based solution to extract and analyze key information from company PDF reports for investors. This tool combines the power of **Hugging Face Transformers** and **Grok API** via **LangChain** to summarize text, provide in-depth insights, and structure information for decision-making.

---

## **Features**

1. **Text Extraction**: 
   - Extracts text from PDF files using `pdfplumber`.

2. **Hybrid Analysis**:
   - Summarizes content using Hugging Face's `facebook/bart-large-cnn` model.
   - Performs detailed reasoning with the Grok API via LangChain.

3. **Investor-Focused Insights**:
   - Identifies and structures:
     - Future growth prospects.
     - Key changes in the business.
     - Key triggers (opportunities or risks).
     - Material impacts on next year's earnings and growth.

4. **Structured Output**:
   - Outputs results in both the console and a JSON file for easy access.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/pdf-investor-insights.git
cd pdf-investor-insights
```

### **2. Install Dependencies**
Make sure you have Python 3.8+ installed. Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### **3. Set Up Grok API Key**
- Obtain a Grok API key from [Grok](https://www.grok.com/).
- Replace `YOUR_GROK_API_KEY` in the script with your actual API key.

---

## **Usage**

### **1. Place Your PDF**
Save the target company report PDF in the project directory (e.g., `company_report.pdf`).

### **2. Run the Script**
```bash
python main.py
```

### **3. View Output**
- **Console**: See the summarized and detailed insights for each section.
- **JSON File**: Results are saved in `investor_insights.json` in the same directory.

---

## **Example Output**

### **Console**
```
[INFO] Found 3 sections for analysis.

Processing Section 1...
[INFO] Summary for Section 1: Company is diversifying into renewable energy.
[INFO] Detailed analysis for Section 1:
1. Future growth prospects: Diversification into renewable energy.
2. Key changes: Closure of underperforming units.
3. Key triggers: Regulatory risks and global demand.
4. Material impacts: 15% projected growth in 2024.

[INFO] Key insights extracted successfully and saved to investor_insights.json!
```

### **JSON File**
```json
{
    "Section 1": {
        "Summary": "Company is diversifying into renewable energy.",
        "Detailed Insights": {
            "Future growth prospects": "Diversification into renewable energy.",
            "Key changes": "Closure of underperforming units.",
            "Key triggers": "Regulatory risks and global demand.",
            "Material impacts": "15% projected growth in 2024."
        }
    }
}
```

---

## **Project Structure**

```
pdf-investor-insights/
├── main.py             # Main script for extracting and analyzing insights
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── company_report.pdf  # Sample PDF (replace with your own)
```

---

## **Technologies Used**

- **Python Libraries**:
  - `pdfplumber` - Extract text from PDF files.
  - `transformers` - Summarization with Hugging Face models.
  - `langchain` - Integration of the Grok API for detailed analysis.

- **APIs**:
  - **Grok API** - Context-aware reasoning for detailed insights.

---

## **Customization**

1. **Enhancing Summarization**:
   - Replace `facebook/bart-large-cnn` with another Hugging Face model (e.g., T5).

2. **Adapting to Other Document Types**:
   - Update the `split_into_sections` function to handle different heading formats.

---

## **Contributing**

Feel free to fork the repository and submit pull requests to improve the functionality. Suggestions and bug reports are welcome!

