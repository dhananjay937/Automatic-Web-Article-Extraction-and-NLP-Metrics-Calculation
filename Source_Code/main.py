# main.py
import os
import sys
import logging
import pandas as pd

from utils import Utils
from nlp_metrics import NLP, Metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Source_Code")

def main():
    # Base folder for data relative to this script
    base_data = os.path.join("..", "Data")  # relative to Source_Code/
    input_path = os.path.join(base_data, "Input", "Input.xlsx")
    output_path = os.path.join(base_data, "Output", "Output Data Structure.xlsx") 
    
    # Ensure the output directory exists
    Utils.ensure_dirs(os.path.dirname(output_path))

    if not os.path.exists(input_path):
        logger.error("Input.xlsx not found at %s", input_path)
        sys.exit(1)

    # Load stopwords and master dictionary
    stopwords = Utils.load_stopwords(os.path.join(base_data, "StopWords", "StopWords_*.txt"))
    pos_words, neg_words = Utils.load_master_dictionary(os.path.join(base_data, "MasterDictionary"))

    if not pos_words or not neg_words:
        logger.warning("Master dictionary files missing or empty.")

    df_input = Utils.read_input_excel(input_path)

    existing_df = None
    processed_ids = set()
    if os.path.exists(output_path):
        try:
            existing_df = pd.read_excel(output_path)
            processed_ids = set(str(x).strip() for x in existing_df["URL_ID"] if pd.notna(x))
            logger.info("Found %d already processed rows.", len(processed_ids))
        except Exception as e:
            logger.warning("Could not read existing output file: %s", e)

    rows: list[Metrics] = []
    for _, row in df_input.iterrows():
        url_id = str(row["URL_ID"]).strip()
        url = str(row["URL"]).strip()
        if url_id in processed_ids:
            logger.info("Skipping %s (already processed)", url_id)
            continue

        logger.info("Processing %s | %s", url_id, url)
        html = Utils.fetch_html(url)
        if not html:
            logger.error("Skipping %s (no HTML)", url_id)
            continue

        title, body = Utils.extract_article_title_body(html)
        if not body:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            body = " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))

        Utils.save_article(url_id, title, body)
        metrics = NLP.compute_metrics(title, body, stopwords, pos_words, neg_words, url_id, url)
        rows.append(metrics)

    # Prepare output
    cols = [
        "URL_ID","URL","POSITIVE SCORE","NEGATIVE SCORE","POLARITY SCORE","SUBJECTIVITY SCORE",
        "AVG SENTENCE LENGTH","PERCENTAGE OF COMPLEX WORDS","FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE",
        "COMPLEX WORD COUNT","WORD COUNT","SYLLABLE PER WORD","PERSONAL PRONOUNS","AVG WORD LENGTH"
    ]

    new_data = [[
        m.url_id, m.url, m.positive_score, m.negative_score, round(m.polarity_score,6),
        round(m.subjectivity_score,6), round(m.avg_sentence_length,6), round(m.percent_complex_words,6),
        round(m.fog_index,6), round(m.avg_words_per_sentence,6), m.complex_word_count, m.word_count,
        round(m.syllables_per_word,6), m.personal_pronouns, round(m.avg_word_length,6)
    ] for m in rows]

    if existing_df is not None and not existing_df.empty:
        combined_df = pd.concat([existing_df, pd.DataFrame(new_data, columns=cols)], ignore_index=True)
        combined_df.drop_duplicates(subset=["URL_ID"], keep="first", inplace=True)
        combined_df.to_excel(output_path, index=False)
    else:
        pd.DataFrame(new_data, columns=cols).to_excel(output_path, index=False)

    logger.info("Saved metrics to %s", output_path)

if __name__ == "__main__":
    main()
