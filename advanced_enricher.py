import requests
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from difflib import SequenceMatcher
import time
import re

# Yapılandırma
EMAIL = "hkaraca@turktelekom.com.tr" # Crossref için
SIMILARITY_THRESHOLD = 0.80 # %80 altı eşleşmeleri reddet

def clean_text(text):
    """Metni karşılaştırma için temizler: küçük harf, noktalama yok."""
    if not text: return ""
    # LaTeX komutlarını temizle (basitçe)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = text.replace('{', '').replace('}', '')
    # Sadece alfanümerik karakterler
    text = re.sub(r'[^a-z0-9\s]', '', text.lower())
    return " ".join(text.split())

def calculate_similarity(text1, text2):
    """İki metin arasındaki benzerlik oranını (0.0 - 1.0) döndürür."""
    if not text1 or not text2:
        return 0.0
    return SequenceMatcher(None, clean_text(text1), clean_text(text2)).ratio()

def get_bib_from_doi(doi):
    """DOI vererek Crossref'ten temiz BibTeX çeker."""
    try:
        url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
        headers = {"User-Agent": f"mailto:{EMAIL}"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"    ! DOI fetch hatası: {e}")
    return None

def search_crossref(title, author):
    """Crossref API'sinde arama yapar."""
    try:
        query = f"{title} {author}"
        params = {'query.bibliographic': query, 'rows': 1, 'mailto': EMAIL}
        resp = requests.get("https://api.crossref.org/works", params=params, timeout=5)
        data = resp.json()
        items = data.get('message', {}).get('items', [])
        
        if items:
            item = items[0]
            found_title = item.get('title', [''])[0]
            score = calculate_similarity(title, found_title)
            return {'source': 'Crossref', 'doi': item.get('DOI'), 'title': found_title, 'score': score, 'data': item}
    except Exception:
        pass
    return None

def search_semantic_scholar(title):
    """Semantic Scholar API'sinde arama yapar."""
    try:
        # Semantic Scholar Graph API
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': title,
            'limit': 1,
            'fields': 'title,authors,externalIds,year,venue'
        }
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                item = data['data'][0]
                found_title = item.get('title', '')
                score = calculate_similarity(title, found_title)
                doi = item.get('externalIds', {}).get('DOI')
                return {'source': 'SemanticScholar', 'doi': doi, 'title': found_title, 'score': score, 'data': item}
    except Exception:
        pass
    return None

def search_dblp(title):
    """DBLP API'sinde arama yapar."""
    try:
        url = "https://dblp.org/search/publ/api"
        params = {'q': title, 'format': 'json', 'h': 1}
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            hits = data.get('result', {}).get('hits', {}).get('hit', [])
            if hits:
                info = hits[0].get('info', {})
                found_title = info.get('title', '')
                score = calculate_similarity(title, found_title)
                doi = info.get('doi')
                return {'source': 'DBLP', 'doi': doi, 'title': found_title, 'score': score, 'data': info}
    except Exception:
        pass
    return None

def enrich_bib_advanced(input_file, output_file):
    # Dosya okuma ve yazma işlemlerini düzeltelim
    with open(input_file, 'r', encoding='utf-8') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    print(f"Toplam {len(bib_database.entries)} referans taranacak. Gelişmiş mod devrede...\n")
    
    # Döngü öncesi writer tanımlayalım
    writer = BibTexWriter()
    
    updated_entries = [] # Güncellenenleri burada tutalım
    
    # Bib database'i yerinde güncelleyeceğiz, yeni liste oluşturmaya gerek yok
    # ama entry'leri tek tek güncelleyeceğiz.
    
    for i, entry in enumerate(bib_database.entries):
        original_id = entry.get('ID', '')
        # Başlıktaki LaTeX koruma parantezlerini temizle (örneğin {Machine Learning})
        raw_title = entry.get('title', '')
        title = raw_title.replace('{', '').replace('}', '').replace('\\', '').strip()
        author = entry.get('author', '').replace('{', '').replace('}', '')
        
        if not title: 
            print(f"[{i+1}] {original_id}: Başlık yok, atlanıyor.")
            entry['bibsource'] = "Original/Manual"
            updated_entries.append(entry)
            continue
        
        print(f"[{i+1}/{len(bib_database.entries)}] {original_id}")
        print(f"  Aranan: {title[:50]}...")
        
        # Adayları topla
        candidates = []
        
        # 1. Crossref Ara
        res_cr = search_crossref(title, author)
        if res_cr: 
            # Score'u yeniden hesapla emin olmak için
            res_cr['score'] = calculate_similarity(title, res_cr['title'])
            candidates.append(res_cr)
            print(f"  - Crossref: {res_cr['score']:.2f}")

        # 2. Semantic Scholar Ara (Eğer Crossref kesin değilse)
        best_score = max([c['score'] for c in candidates]) if candidates else 0
        if best_score < 0.95:
             res_ss = search_semantic_scholar(title)
             if res_ss: 
                res_ss['score'] = calculate_similarity(title, res_ss['title'])
                candidates.append(res_ss)
                print(f"  - SemScholar: {res_ss['score']:.2f}")
        
        # 3. DBLP Ara (Hala iyi sonuç yoksa)
        best_score = max([c['score'] for c in candidates]) if candidates else 0
        if best_score < 0.90:
            res_dblp = search_dblp(title)
            if res_dblp: 
                res_dblp['score'] = calculate_similarity(title, res_dblp['title'])
                candidates.append(res_dblp)
                print(f"  - DBLP: {res_dblp['score']:.2f}")

        if not candidates:
            print("  -> Hiçbir kaynakta bulunamadı.")
            entry['bibsource'] = "Original/Manual"
            updated_entries.append(entry)
            continue
            
        # En iyi adayı seç
        best_match = max(candidates, key=lambda x: x['score'])
        
        # Eşik kontrolü
        if best_match['score'] < SIMILARITY_THRESHOLD:
            print(f"  -> Bulundu ama benzerlik düşük ({best_match['score']:.2f} < {SIMILARITY_THRESHOLD}). Reddedildi.")
            entry['bibsource'] = "Original/Manual"
            updated_entries.append(entry)
            continue
        
        # DOI Kontrolü ve Güncelleme
        final_bib_str = None
        
        # Provenance (Köken) bilgisini takip et
        provenance = "Original/Manual"
        
        found_doi = best_match.get('doi')
        if found_doi:
            print(f"  -> Eşleşme: {best_match['source']} (DOI: {found_doi})")
            # DOI varsa, en temiz veriyi Crossref'ten o DOI ile çekmeyi dene
            try:
                final_bib_str = get_bib_from_doi(found_doi)
                if final_bib_str:
                     clean_db = bibtexparser.loads(final_bib_str)
                     if clean_db.entries:
                        clean_entry = clean_db.entries[0]
                        # Cite key'i koru!
                        clean_entry['ID'] = original_id
                        entry.clear()
                        entry.update(clean_entry)
                        
                        # Kaynak bilgisini güncelle
                        if best_match['source'] == 'Crossref':
                            provenance = "Crossref"
                        else:
                            provenance = f"{best_match['source']} -> Crossref (via DOI)"
                            
                        print("  -> Veri güncellendi (DOI Kaynaklı).")
            except Exception as e:
                print(f"  -> DOI işleme hatası: {e}")
        else:
            # DOI yoksa veya çekilemediyse orijinali koru
            print("  -> DOI doğrulanamadı, orijinal veri korundu.")
        
        # Kaynak bilgisini entry'e ekle
        entry['bibsource'] = provenance
        updated_entries.append(entry)
        
        print("-" * 40)
        time.sleep(0.5) # API nezaketi

    # Kaydet
    bib_database.entries = updated_entries
    with open(output_file, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file, writer=writer)
    print(f"\nİşlem tamam! Sonuç: {output_file}")

if __name__ == "__main__":
    enrich_bib_advanced("refs.bib", "zengin_v2.bib")
