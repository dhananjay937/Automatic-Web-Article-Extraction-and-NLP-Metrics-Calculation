# 🧠 Automatic Web Article Extraction and NLP Metrics Calculation  

## 📌 Objective  
This project automates the extraction of text from multiple web pages, analyzes the content, and calculates key NLP metrics such as **sentiment scores**, **readability**, and **word statistics**.  
It helps quickly understand the nature of the content without manually reading each article.

---

## 🚀 Features  
- Automated extraction of article titles and bodies from multiple URLs  
- NLP metrics computation (sentiment, subjectivity, readability, and complexity)  
- Graceful handling of missing/invalid data  
- Modular and reusable codebase  
- Automatic Excel output generation  

---

## ⚙️ How It Works  

### 1️⃣ Input Reading  
- Reads a list of URLs (`URL_ID`, `URL`) from `Input.xlsx`  
- Validates URLs and skips missing entries  

### 2️⃣ Web Scraping  
- Fetches HTML using `requests`  
- Extracts article title and body via `BeautifulSoup`  
- Saves each article in `/Articles/{URL_ID}.txt`  

### 3️⃣ NLP Metric Computation  
The `NLP.compute_metrics()` method calculates:  
- Positive Score  
- Negative Score  
- Polarity & Subjectivity  
- Average Sentence Length  
- Percentage of Complex Words  
- Fog Index (Readability)  
- Complex Word Count & Total Word Count  
- Average Syllables per Word  
- Personal Pronoun Count  
- Average Word Length  

### 4️⃣ Output Storage  
- Results are saved to `../Data/Output/Output Data Structure.xlsx`  
- Already processed URLs are skipped automatically  

---

## 🧩 Project Structure  

```text
Source_Code/
├── main.py               # Main pipeline script
├── utils.py              # Excel, HTML, and file utilities
├── nlp_metrics.py        # NLP metric computation
│
├── ../Data/
│   ├── Input/Input.xlsx         # List of URLs
│   ├── StopWords/               # Stopword files
│   ├── MasterDictionary/        # positive-words.txt, negative-words.txt
│   └── Output/                  # Output Excel file
│
└── Articles/                    # Extracted article text file

```


---

## 📦 Dependencies  

Install the required Python libraries:

```bash
pip install pandas openpyxl requests beautifulsoup4 lxml
```
---

## 🧰 How to Run

Open a terminal and navigate to the `Source_Code/` folder:

```bash
cd Source_Code
```

Run the main script:

```bash
python main.py
```

**Output:**

* Extracted articles → `Articles/`
* NLP metrics → `../Data/Output/Output Data Structure.xlsx`

---

## 📁 Folder Preparation

Before running, ensure these folders and files exist:

* `../Data/Input/Input.xlsx`
* `../Data/StopWords/`
* `../Data/MasterDictionary/`
* `../Data/Output/`

> The script will automatically create missing folders where necessary.

---

## 🧾 Conclusion

This project demonstrates a complete **end-to-end NLP automation pipeline** for:

* Web content extraction
* Text analysis and NLP metrics computation
* Structured result reporting

---



