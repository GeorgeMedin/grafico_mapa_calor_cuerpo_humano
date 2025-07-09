# pip install beautifulsoup4 lxml matplotlib streamlit

import streamlit as st
import pandas as pd
from matplotlib import cm
from bs4 import BeautifulSoup

# ========================
# 🔧 Estilos para ancho total
# ========================
st.set_page_config(layout="wide")

# ========================
# 📊 Datos simulados
# ========================
data = pd.DataFrame({
    'parte_del_cuerpo': [
        'cabeza', 'tronco_frontal', 'abdomen', 'piernas', 'piernas', 'cuello',
        'cabeza', 'piernas', 'manos', 'brazos', 'pies', 'tronco_posterior',
        'piernas', 'piernas', 'piernas', 'abdomen', 'abdomen', 'tronco_frontal',
        'tronco_frontal', 'tronco_posterior', 'tronco_posterior', 'tronco_posterior',
        'tronco_posterior', 'manos', 'manos', 'manos', 'manos', 'pies', 'pies',
        'pies', 'pies', 'pies', 'pies', 'brazos', 'brazos', 'brazos', 'cuello',
        'cuello', 'cuello', 'cuello', 'cuello', 'cabeza', 'cabeza', 'cabeza',
        'cabeza'
    ]
})

zonas = data['parte_del_cuerpo'].unique().tolist()
zona_filtrada = st.selectbox("Filtrar por parte del cuerpo", ["Todas"] + zonas)

if zona_filtrada != "Todas":
    data = data[data['parte_del_cuerpo'] == zona_filtrada]

conteo = data['parte_del_cuerpo'].value_counts().to_dict()
total = sum(conteo.values())
max_val = max(conteo.values()) if conteo else 1

def valor_a_color(count):
    norm = 1 - (count / max_val)
    r, g, b, _ = cm.RdYlGn(norm)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

colores = {
    parte: {
        'color': valor_a_color(count),
        'valor': count,
        'porcentaje': round(count / total * 100, 1) if total > 0 else 0
    } for parte, count in conteo.items()
}

# ========================
# 🧬 SVG + colores
# ========================
with open("cuerpoHumano.svg", "r", encoding="utf-8") as file:
    svg_content = file.read()

soup = BeautifulSoup(svg_content, 'xml')
for style_tag in soup.find_all('style'):
    style_tag.decompose()

for ellipse in soup.find_all('ellipse'):
    parte = ellipse.get('id')
    if parte in colores:
        ellipse['fill'] = colores[parte]['color']
        ellipse['stroke'] = 'none'
        tooltip = soup.new_tag("title")
        tooltip.string = (
            f"{parte}\n"
            f"Valor: {colores[parte]['valor']}\n"
            f"{colores[parte]['porcentaje']}% del total"
        )
        ellipse.append(tooltip)
    else:
        ellipse['fill'] = '#f0f0f0'
        ellipse['stroke'] = 'none'

svg_str = str(soup)

# ========================
# 🖼️ Layout visual
# ========================
col1, col2 = st.columns([5, 4])

with col1:
    st.markdown(
        f"""
        <div style="width:100%; text-align:center;">
            {svg_str}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    df_tabla = pd.DataFrame([
        {
            "Parte del cuerpo": parte,
            "Ocurrencias": info["valor"],
            "% del total": f"{info['porcentaje']}%"
        } for parte, info in colores.items()
    ])
    
    st.dataframe(df_tabla, use_container_width=True)

    chart_data = pd.DataFrame({
        "parte_del_cuerpo": list(colores.keys()),
        "valor": [info["valor"] for info in colores.values()]
    }).sort_values(by="valor", ascending=False)

    st.bar_chart(chart_data.set_index("parte_del_cuerpo"))


    data2 = [
    {
        "Categoria General": "Cabeza",
        "Subpartes Incluidas": "Cráneo, cara, frente, ojos, nariz, boca, orejas, mentón, mandíbula, cuero cabelludo",
        "Subpartes Comunes": "Cabeza, cara, frente, boca, nariz, ojos, orejas, mandíbula, cráneo"
    },
    {
        "Categoria General": "Cuello",
        "Subpartes Incluidas": "Cuello, garganta, cervicales, nuca",
        "Subpartes Comunes": "Cuello, garganta, parte trasera del cuello, cervical"
    },
    {
        "Categoria General": "Tronco Frontal",
        "Subpartes Incluidas": "Pecho, tórax, esternón, costillas, clavícula, pecho superior",
        "Subpartes Comunes": "Pecho, tórax, clavícula, pecho, parte frontal del tronco"
    },
    {
        "Categoria General": "Tronco Posterior",
        "Subpartes Incluidas": "Espalda alta, espalda baja, columna dorsal, zona lumbar",
        "Subpartes Comunes": "Espalda, columna, espalda baja, parte trasera del torso"
    },
    {
        "Categoria General": "Abdomen",
        "Subpartes Incluidas": "Abdomen superior e inferior, ombligo, flancos laterales",
        "Subpartes Comunes": "Abdomen, barriga, estómago, panza, ombligo"
    },
    {
        "Categoria General": "Cadera / Pelvis / Glúteos / Genitales",
        "Subpartes Incluidas": "Caderas, glúteos, pelvis, ingle, pubis, genitales externos",
        "Subpartes Comunes": "Cadera, glúteos, nalgas, pelvis, parte íntima, testículos, vagina"
    },
    {
        "Categoria General": "Brazos",
        "Subpartes Incluidas": "Hombros, brazo superior, codo, antebrazo",
        "Subpartes Comunes": "Hombro, brazo, codo, antebrazo"
    },
    {
        "Categoria General": "Manos",
        "Subpartes Incluidas": "Muñeca, palma, dedos de la mano",
        "Subpartes Comunes": "Mano, dedos, muñeca, palma"
    },
    {
        "Categoria General": "Piernas",
        "Subpartes Incluidas": "Muslo, rodilla, pantorrilla, gemelos",
        "Subpartes Comunes": "Pierna, muslo, rodilla, pantorrilla, canilla, gemelo"
    },
    {
        "Categoria General": "Pies",
        "Subpartes Incluidas": "Tobillo, talón, planta del pie, dedos del pie",
        "Subpartes Comunes": "Pie, talón, tobillo, dedos del pie, planta"
    }
]
    
df_tabla2 = pd.DataFrame(data2)

st.dataframe(df_tabla2, use_container_width=True)

