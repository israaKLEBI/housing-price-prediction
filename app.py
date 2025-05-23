import streamlit as st
import pandas as pd
import joblib

def main():
    # Charger le modèle et les colonnes
    try:
        model = joblib.load("model.pkl")
        columns = joblib.load("columns.pkl")
    except FileNotFoundError:
        st.error("Error/Erreur: Files 'model.pkl' or 'columns.pkl' not found/Fichiers 'model.pkl' ou 'columns.pkl' introuvables.")
        return

    # Titre bilingue
    st.title("Bienvenue chez Israa-Immobilière 🏠")
    st.title("House Price Estimation/Estimation du Prix d'une Maison")
    st.write("Fill in the details below to estimate the price/Remplissez les informations ci-dessous pour estimer le prix :")

    # Initialisation des données d'entrée
    input_data = {col: 0 for col in columns}
    input_df = pd.DataFrame([input_data], columns=columns)

    # Formulaire
    with st.form("housing_form"):
        # Champs numériques
        st.subheader("House Features/Caractéristiques de la maison")
        input_data['area'] = st.number_input("Area/Surface (square feet/pieds carrés)", min_value=0, value=5000, step=100)
        input_data['bedrooms'] = st.number_input("Bedrooms/Chambres", min_value=1, value=3, step=1)
        input_data['bathrooms'] = st.number_input("Bathrooms/Salles de bain", min_value=1, value=2, step=1)
        input_data['stories'] = st.number_input("Stories/Étages", min_value=1, value=2, step=1)
        input_data['parking'] = st.number_input("Parking/Parking", min_value=0, value=1, step=1)

        # Champs booléens
        input_data['mainroad_yes'] = 1 if st.checkbox("Main road/Route principale") else 0
        input_data['guestroom_yes'] = 1 if st.checkbox("Guest room/Chambre d'amis") else 0
        input_data['basement_yes'] = 1 if st.checkbox("Basement/Sous-sol") else 0
        input_data['hotwaterheating_yes'] = 1 if st.checkbox("Hot water heating/Chauffage à l'eau chaude") else 0
        input_data['airconditioning_yes'] = 1 if st.checkbox("Air conditioning/Climatisation") else 0
        input_data['prefarea_yes'] = 1 if st.checkbox("Preferred area/Zone préférée") else 0

        # État de l'ameublement
        furnishing_option = st.selectbox(
            "Furnishing status/État de l'ameublement",
            options=["Furnished/Meublé", "Semi-furnished/Semi-meublé", "Unfurnished/Non meublé"],
            index=1
        )
        # Réinitialiser les colonnes furnishingstatus
        input_data['furnishingstatus_furnished'] = 0
        input_data['furnishingstatus_semi-furnished'] = 0
        input_data['furnishingstatus_unfurnished'] = 0
        if furnishing_option == "Furnished/Meublé":
            input_data['furnishingstatus_furnished'] = 1
        elif furnishing_option == "Semi-furnished/Semi-meublé":
            input_data['furnishingstatus_semi-furnished'] = 1
        else:  # Unfurnished/Non meublé
            input_data['furnishingstatus_unfurnished'] = 1

        # Bouton de soumission
        submitted = st.form_submit_button("Estimate Price/Estimer le prix")

    # Prédiction
    if submitted:
        input_df = pd.DataFrame([input_data], columns=columns)
        try:
            prediction = model.predict(input_df)[0]
            st.success(f"Estimated Price/Prix estimé : {prediction:,.2f} DT")
        except Exception as e:
            st.error(f"Error/Erreur : {str(e)}")

if __name__ == "__main__":
    main()