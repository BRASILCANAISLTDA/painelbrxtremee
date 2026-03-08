import requests
import json
import re

# COLOQUE SEU LINK M3U ABAIXO
M3U_URL = "https://drive.google.com/file/d/1vKK2BLoFf5D3XLk6emMiHjf_kSENrOxL/view?usp=drive_link, https://drive.google.com/file/d/1hsgIgHruheVVohyk9f_0HD5_l2EEZ1Ty/view?usp=drive_link, https://drive.google.com/file/d/1-wxqQ_liEZRQgmT4c95x1OdXIEc6shLH/view?usp=drive_link, https://drive.google.com/file/d/1a4j_ye4y7LYgAIt4sebXHdzh5eUmflkD/view?usp=drive_link, https://drive.google.com/file/d/1zYsjUOD0yaYyGTH4GXOxVkPYndoXItRf/view?usp=drive_link, https://drive.google.com/file/d/1cibQesdkDkay_fBjNkosB2q17U0SlUk3/view?usp=drive_link, https://drive.google.com/file/d/1ln9JEKkxsEqbLzS3CBDBP9zMIeGpjUFN/view?usp=drive_link, https://drive.google.com/file/d/1FehlTafkfp3iNmlbNVRwQgMZzF10-g7F/view?usp=drive_link, https://drive.google.com/file/d/1M7z_Rc81VlOwfO28fnWwATDdPomCV5Dl/view?usp=drive_link, https://drive.google.com/file/d/17ypu7do9W8dzCYD_y0cOAuAco0PAaCpn/view?usp=drive_link"

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
