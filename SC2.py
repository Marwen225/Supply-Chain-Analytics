import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

# Charger les données
data = pd.read_csv("supply_chain_data.csv")

st.title("Analyse de la Chaîne d'Approvisionnement")

# Afficher les premières lignes du dataset
st.header("Aperçu des données")
st.dataframe(data.head())

# Description statistique
st.header("Statistiques descriptives")
st.write(data.describe())

# Relation entre prix et revenus générés
st.header("Relation entre le prix et les revenus générés")
fig1 = px.scatter(data, x='Price',  # Correction ici
                  y='Revenue generated', 
                  color='Product type', 
                  hover_data=['Number of products sold'], 
                  trendline="ols")
st.plotly_chart(fig1)

# Ventes par type de produit
st.header("Ventes par Type de Produit")
ventes = data.groupby('Product type')['Number of products sold'].sum().reset_index()
fig2 = px.pie(ventes, values='Number of products sold', names='Product type', 
              title='Ventes par Type de Produit', 
              hole=0.5,
              color_discrete_sequence=px.colors.qualitative.Pastel)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2)

# Revenus totaux par transporteur
st.header("Revenus Totaux par Transporteur")
revenus_transporteur = data.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=revenus_transporteur['Shipping carriers'], 
                      y=revenus_transporteur['Revenue generated']))
fig3.update_layout(title='Revenus Totaux par Transporteur', 
                   xaxis_title='Transporteur', 
                   yaxis_title='Revenus Générés')
st.plotly_chart(fig3)

# Temps de livraison moyen et coûts de fabrication moyens
st.header("Temps de Livraison Moyen et Coûts de Fabrication Moyens")
delai_moyen = data.groupby('Product type')['Lead time'].mean().reset_index()
couts_fabrication_moyens = data.groupby('Product type')['Manufacturing costs'].mean().reset_index()
resultats = pd.merge(delai_moyen, couts_fabrication_moyens, on='Product type')
resultats.rename(columns={'Lead time': 'Temps de Livraison Moyen', 'Manufacturing costs': 'Coûts de Fabrication Moyens'}, inplace=True)
st.dataframe(resultats)

# Revenus par SKU
st.header("Revenus Générés par SKU")
fig4 = px.line(data, x='SKU', y='Revenue generated', title='Revenus Générés par SKU')
st.plotly_chart(fig4)

# Niveaux de stock par SKU
st.header("Niveaux de Stock par SKU")
fig5 = px.line(data, x='SKU', y='Stock levels', title='Niveaux de Stock par SKU')
st.plotly_chart(fig5)

# Quantité commandée par SKU
st.header("Quantité Commandée par SKU")
fig6 = px.bar(data, x='SKU', y='Order quantities', title='Quantité Commandée par SKU')
st.plotly_chart(fig6)

# Coûts de transport par transporteur
st.header("Coûts de Transport par Transporteur")
fig7 = px.bar(data, x='Shipping carriers', y='Shipping costs', title='Coûts de Transport par Transporteur')
st.plotly_chart(fig7)

# Répartition des coûts par mode de transport
st.header("Répartition des Coûts par Mode de Transport")
fig8 = px.pie(data, values='Costs', names='Transportation modes', 
              title='Répartition des Coûts par Mode de Transport', 
              hole=0.5,
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig8)

# Taux de défaut par type de produit
st.header("Taux de Défaut par Type de Produit")
taux_defaut_produit = data.groupby('Product type')['Defect rates'].mean().reset_index()
fig9 = px.bar(taux_defaut_produit, x='Product type', y='Defect rates', title='Taux de Défaut par Type de Produit')
st.plotly_chart(fig9)

# Taux de défaut par mode de transport
st.header("Taux de Défaut par Mode de Transport")
tableau_croisé = pd.pivot_table(data, values='Defect rates', index=['Transportation modes'], aggfunc='mean')
fig10 = px.pie(values=tableau_croisé["Defect rates"], names=tableau_croisé.index, title='Taux de Défaut par Mode de Transport', hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig10)
