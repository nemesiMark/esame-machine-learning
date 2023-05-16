# importo tutte le librerie necessarie
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import streamlit as st
import pandas as pd
import mlem
import toml
import io


# implemento la funzione main
def main():

    # file per settare colori di sfondo e testo
    with open('.streamlit/config.toml', 'r') as f:
        config = toml.load(f)

    # caricamento del modello che avevo precedentemente allenato e salvato tramite il notebook
    new_model = mlem.api.load('model_.mlem')

    # Colonne scelte: 'indus','nox','rm','tax','ptratio','lstat'

    # valori di input, min e max li ho recuperati dal describe del notebook 
    # (altrimenti avrei dovuto creare un df leggendo nuovamente il csv, fare max/min per colonna ed assegnarli a max_value= e min_value=)
    st.header("Input values")
    indus = st.number_input('Enter a NUMBER value indus:', value=0.46, step=0.01, min_value=0.46, max_value=27.74)
    nox = st.number_input('Enter a NUMBER value nox:', value=0.385, step=0.01, min_value=0.385, max_value=0.871)
    rm = st.number_input('Enter a NUMBER value rm:', value=3.561, step=0.01, min_value=3.561, max_value=8.78)
    tax = st.number_input('Enter a NUMBER value tax:', value=187.0, step=0.01, min_value=187.0, max_value=711.0)
    pratio = st.number_input('Enter a NUMBER value ptratio:', value=12.6, step=0.01, min_value=12.6, max_value=22.0)
    lstat = st.number_input('Enter a NUMBER value lstat:', value=1.73, step=0.01, min_value=1.73, max_value=37.97)

    # predizione dei valori dati in input
    st.write("Y_PRED: ",round(new_model.predict([[indus,nox,rm,tax,pratio,lstat]])[0],2))

    # carico file csv
    uploaded_file = st.file_uploader("Choose your file CSV with this COLUMNS: (crim, zn, indus, chas, nox, rm, age, dis, rad, tax, pratio, b, lstat, medv)")
    
    # verifico che il file non sia vuoto
    if uploaded_file is not None:
        df = pd.DataFrame()

        # se non carico un file csv lancio un warning a video
        if uploaded_file.name[-3:] != "csv":
            st.warning("CSV file is required.")
        

        else:
            # leggo il csv e splitto in X e y 
            df = pd.read_csv(uploaded_file)

            df = df.rename(columns={'medv': 'price'})
            X = df.drop(columns=['crim','zn','chas','age','dis','rad','b', 'price'])
            y = df['price']

            # splitto parte del dataframe per avere una parte di train e un' altra di test
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 667)
            y_pred = new_model.predict(X_test)

            # creo il dataframe da scaricare con X_test e aggiungendo una nuova colonna "predict" y_pred
            df1 = X_test
            df1["Predict"] = y_pred

            # calcolo degli errori
            r2score = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred, squared=False)

            # visualizzo gli errori precedentemente calcolati
            st.header("Calcolo errori")
            st.write('R2_score: ', r2score)
            st.write('MAE: ', mae)
            st.write('MSE: ', mse)
            st.write('RMSE: ', rmse)


            # bottone per scaricare X_test + y_pred
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df1.to_excel(writer, index=False)
                writer.save()
                st.download_button(
                    label="Download Excel Result",
                    data=buffer,
                    file_name="trasnformed_file.xlsx",
                    mime="application/vnd.ms-excel")
    

# questo modulo sarà eseguito solo se runnato
if __name__ == "__main__":
    main()