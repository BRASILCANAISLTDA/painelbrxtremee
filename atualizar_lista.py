import requests
import json
import re

# Usamos as aspas triplas para garantir que a URL seja lida como um texto único
M3U_URL = """https://drive.google.com/file/d/1vKK2BLoFf5D3XLk6emMiHjf_kSENrOxL/view"""

def processar():
    try:
        print("Acessando a URL da lista...")
        # O cabeçalho 'User-Agent' simula um navegador para o Google liberar o download
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r = requests.get(M3U_URL, headers=headers, timeout=30)
        r.raise_for_status()
        
        conteudo = r.text
        lines = conteudo.splitlines()
        
        canais = []
        categorias_vistas = set()
        
        for i, line in enumerate(lines):
            if line.startswith('#EXTINF'):
                # Busca a categoria no group-title
                cat_match = re.search(r'group-title="([^"]+)"', line)
                cat_name = cat_match.group(1) if cat_match else "Geral"
                
                # Busca o nome do canal
                name_match = re.search(r',(.+)$', line)
                stream_name = name_match.group(1).strip() if name_match else "Canal"
                
                if i + 1 < len(lines):
                    url_canal = lines[i+1].strip()
                    if url_canal.startswith('http'):
                        canais.append({
                            "name": stream_name,
                            "category_name": cat_name,
                            "url": url_canal
                        })
                        categorias_vistas.add(cat_name)

        # Formata as categorias para o padrão do Smarters
        lista_categorias = [
            {"category_id": str(index), "category_name": nome} 
            for index, nome in enumerate(sorted(categorias_vistas))
        ]
        
        resultado_final = {
            "live": canais,
            "categories": lista_categorias
        }

        with open('canais.json', 'w', encoding='utf-8') as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=4)
        
        print(f"Sucesso! {len(canais)} canais encontrados na URL.")

    except Exception as e:
        print(f"Erro ao ler a URL: {e}")
        exit(1)

if __name__ == "__main__":
    processar()
