import requests
import json
import re

# COLOQUE SEU LINK M3U ABAIXO
M3U_URL = "SEU_LINK_AQUI"

def processar():
    try:
        r = requests.get(M3U_URL, timeout=30)
        lines = r.text.splitlines()
        
        canais = []
        categorias = []
        
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                # Busca a categoria
                cat_match = re.search(r'group-title="([^"]+)"', line)
                cat_name = cat_match.group(1) if cat_match else "Geral"
                
                # Busca o nome do canal
                name_match = re.search(r',(.+)$', line)
                stream_name = name_match.group(1).strip() if name_match else "Canal"
                
                # Pega a URL na linha seguinte
                if i + 1 < len(lines):
                    url = lines[i+1].strip()
                    if url.startswith('http'):
                        canais.append({
                            "name": stream_name,
                            "category_name": cat_name,
                            "url": url
                        })
                        if cat_name not in categorias:
                            categorias.append(cat_name)

        # Salva no formato que o Smarters entende
        resultado = {
            "live": canais,
            "categories": [{"category_id": str(i), "category_name": c} for i, c in enumerate(categorias)]
        }

        with open('canais.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)
        print("Sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    processar()
