import requests
import json
import re

# O link abaixo já foi ajustado para download direto do seu Google Drive
M3U_URL = "https://docs.google.com/uc?export=download&id=1vKK2BloFf5D3XLk6emMiHjf_kSENrOxL"

def processar():
    try:
        print("Iniciando download da lista...")
        # Adicionado cabeçalho para evitar bloqueios
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(M3U_URL, headers=headers, timeout=30)
        r.raise_for_status()
        
        lines = r.text.splitlines()
        canais = []
        categorias_set = set()
        
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                # Extrai a categoria (group-title)
                cat_match = re.search(r'group-title="([^"]+)"', line)
                cat_name = cat_match.group(1) if cat_match else "Geral"
                
                # Extrai o nome do canal após a vírgula
                name_match = re.search(r',(.+)$', line)
                stream_name = name_match.group(1).strip() if name_match else "Canal sem nome"
                
                # Pega a URL na linha logo abaixo
                if i + 1 < len(lines):
                    url = lines[i+1].strip()
                    if url.startswith('http'):
                        canais.append({
                            "name": stream_name,
                            "category_name": cat_name,
                            "url": url
                        })
                        categorias_set.add(cat_name)

        # Monta a estrutura que o Smarters precisa
        categorias_lista = [{"category_id": str(i), "category_name": c} for i, c in enumerate(sorted(categorias_set))]
        
        resultado = {
            "live": canais,
            "categories": categorias_lista
        }

        # Salva o arquivo final
        with open('canais.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso! {len(canais)} canais processados.")

    except Exception as e:
        print(f"Erro ao processar: {e}")
        exit(1)

if __name__ == "__main__":
    processar()
