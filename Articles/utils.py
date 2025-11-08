# utils.py
import os
import glob
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional

logger = logging.getLogger("Source_Code")

class Utils:

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    REQUEST_KW = {"headers": {"User-Agent": USER_AGENT}, "timeout": 20}

    @staticmethod
    def ensure_dirs(path="Articles"):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def read_input_excel(path: str) -> pd.DataFrame:
        df = pd.read_excel(path)
        df.columns = [c.strip() for c in df.columns]
        if "URL_ID" not in df.columns or "URL" not in df.columns:
            df = df.rename(columns={df.columns[0]: "URL_ID", df.columns[1]: "URL"})
        return df[["URL_ID", "URL"]]

    @staticmethod
    def load_wordlist_file(path: str) -> List[str]:
        words = []
        if not os.path.isfile(path):
            logger.warning("File not found: %s", path)
            return words
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                token = line.strip().split("|")[0].strip()
                if token:
                    words.append(token.lower())
        return words

    @staticmethod
    def load_stopwords(folder_or_glob: str = "Data/stopwords/StopWords_*.txt") -> set:
        sw = set()
        paths = glob.glob(folder_or_glob)
        if not paths:
            logger.warning("No stopword files found for pattern: %s", folder_or_glob)
        for p in paths:
            if os.path.isfile(p):
                sw.update(Utils.load_wordlist_file(p))
        return sw

    @staticmethod
    def load_master_dictionary(base_path: str = "Data/MasterDictionary") -> Tuple[set, set]:
        pos_path = os.path.join(base_path, "positive-words.txt")
        neg_path = os.path.join(base_path, "negative-words.txt")
        pos = set(Utils.load_wordlist_file(pos_path)) if os.path.isfile(pos_path) else set()
        neg = set(Utils.load_wordlist_file(neg_path)) if os.path.isfile(neg_path) else set()
        return pos, neg

    @staticmethod
    def fetch_html(url: str) -> Optional[str]:
        try:
            resp = requests.get(url, **Utils.REQUEST_KW)
            if resp.status_code == 200:
                return resp.text
            logger.warning("Non-200 response for %s: %s", url, resp.status_code)
        except Exception as e:
            logger.error("Request failed for %s: %s", url, e)
        return None

    @staticmethod
    def extract_article_title_body(html: str) -> Tuple[str, str]:
        soup = BeautifulSoup(html, "lxml")
        title = ""
        h1 = soup.find("h1")
        if h1: title = h1.get_text(" ", strip=True)
        if not title:
            og = soup.find("meta", property="og:title")
            if og and og.get("content"): title = og["content"].strip()
        if not title and soup.title and soup.title.string: title = soup.title.string.strip()

        candidates = soup.find_all("article") or [soup.body]
        body_texts = [" ".join(p.get_text(" ", strip=True) for p in c.find_all("p")) for c in candidates]
        body = max(body_texts, key=len, default="").strip()
        if title and body.lower().startswith(title.lower()):
            body = body[len(title):].lstrip()
        return title, body

    @staticmethod
    def save_article(url_id: str, title: str, body: str, folder="Articles"):
        Utils.ensure_dirs(folder)
        out_path = os.path.join(folder, f"{url_id}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            if title: f.write(title + "\n\n")
            f.write(body)
        return out_path
