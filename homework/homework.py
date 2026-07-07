"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    import glob
    import os

    import pandas as pd

    input_dir = "files/input"
    output_dir = "files/output"

    os.makedirs(output_dir, exist_ok=True)

    zip_files = sorted(glob.glob(os.path.join(input_dir, "*.csv.zip")))

    if not zip_files:
        zip_files = sorted(glob.glob("*.csv.zip"))

    if not zip_files:
        raise FileNotFoundError("No se encontraron archivos .csv.zip en files/input/")

    data = pd.concat((pd.read_csv(file, compression="zip") for file in zip_files),ignore_index=True,)

    client = data[[
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]].copy()

    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    month_to_number = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,}

    campaign = data[[
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",]].copy()

    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    campaign["last_contact_date"] = pd.to_datetime({
        "year": 2022,
        "month": campaign["month"].map(month_to_number),
        "day": campaign["day"],}).dt.strftime("%Y-%m-%d")

    campaign = campaign[
    [
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "last_contact_date",]]

    economics = data[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months",
        ]
    ].copy()

    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)
    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """
    



if __name__ == "__main__":
    clean_campaign_data()
