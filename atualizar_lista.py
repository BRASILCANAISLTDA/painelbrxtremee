import requests
import json
import re

# O uso de """ evita que o link quebre a linha no Python
M3U_URL = """https://drive.google.com/file/d/1vKK2BLoFf5D3XLk6emMiHjf_kSENrOxL/view"""

def processar():
    try:
        print("Iniciando download da lista...")
        # Adicionando um 'User-Agent' para o Google não bloquear o robô
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(M3U_URL, headers=headers, timeout=30)
        r.raise_for_status()
        
        lines = r.text.splitlines()
        canais = []
        categorias_set = set()
        
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                cat_match = re.search(r'group-title="([^"]+)"', line)
                cat_name = cat_match.group(1) if cat_match else "Geral"
                
                name_match = re.search(r',(.+)$', line)
                stream_name = name_match.group(1).strip() if name_match else "Canal"
                
                if i + 1 < len(lines):
                    url = lines[i+1].strip()
                    if url.startswith('http'):
                        canais.append({
                            "name": stream_name,
                            "category_name": cat_name,
                            "url": url
                        })
                        categorias_set.add(cat_name)

        resultado = {
            "live": canais,
            "categories": [{"category_id": str(i), "category_name": c} for i, c in enumerate(sorted(categorias_set))]
        }

        with open('canais.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso! {len(canais)} canais processados.")

    except Exception as e:
        print(f"Erro ao processar: {e}")
        exit(1)

if __name__ == "__main__":
    processar()
