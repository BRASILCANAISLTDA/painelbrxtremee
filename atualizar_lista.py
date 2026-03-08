import requests
import json
import re

M3U_URL = "https://drive.google.com/file/d/1vKK2BLoFf5D3XLk6emMiHjf_kSENrOxL/view
def processar():
    try:
        r = requests.get(M3U_URL, timeout=30)
        lines = r.text.splitlines()
        canais = []
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                # Busca categoria em group-title ou tvg-type
                cat = re.search(r'group-title="([^"]+)"', line)
                cat_name = cat.group(1) if cat else "Geral"
                
                # Busca o nome após a última vírgula
                name = line.split(',')[-1].strip()
                
                if i + 1 < len(lines):
                    url = lines[i+1].strip()
                    if url.startswith('http'):
                        canais.append({"name": name, "category_name": cat_name, "url": url})

        # O Smarters espera os campos 'live' e 'categories'
        cats = list(set([c['category_name'] for c in canais]))
        resultado = {
            "live": canais,
            "categories": [{"category_id": str(i), "category_name": c} for i, c in enumerate(cats)]
        }
        with open('canais.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    processar()
