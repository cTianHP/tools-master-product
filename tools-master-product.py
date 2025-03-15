import pandas as pd
import streamlit as st

def transform_data(df, branch_info):
    fixed_columns = ["NO", "Subdept", "Katagori", "Sub Katagori", "PLU", "Barcode", "Descp", "Aktif", "Merk", "Divisi"]
    tag_columns = [col for col in df.columns if col.startswith("Tag_")]
    transformed_rows = []
    
    for _, row in df.iterrows():
        for tag_col in tag_columns:
            if pd.notna(row[tag_col]):
                branch_code = tag_col[-3:]
                branch_data = branch_info.get(branch_code, {"KODE BRANCH": None, "NAMA BRANCH": None})
                transformed_rows.append({
                    "NO": row["NO"],
                    "Subdept": row["Subdept"],
                    "Katagori": row["Katagori"],
                    "Sub Katagori": row["Sub Katagori"],
                    "PLU": int(row["PLU"]),
                    "Barcode": row["Barcode"],
                    "Descp": row["Descp"],
                    "Aktif": row["Aktif"],
                    "Merk": row["Merk"],
                    "Divisi": row["Divisi"],
                    "BranchCode": branch_code,
                    "KODE BRANCH": branch_data["KODE BRANCH"],
                    "NAMA BRANCH": branch_data["NAMA BRANCH"],
                    "Tag": row[tag_col]
                })
    
    return pd.DataFrame(transformed_rows)

data_branch = { "PKU": {"KODE BRANCH": "1AZ1", "NAMA BRANCH": "PEKANBARU"}, "JBI": {"KODE BRANCH": "1DZ1", "NAMA BRANCH": "JAMBI"}, "BJM": {"KODE BRANCH": "1GZ1", "NAMA BRANCH": "BANJARMASIN"}, "KWG": {"KODE BRANCH": "1JZ1", "NAMA BRANCH": "KARAWANG"}, "PRG": {"KODE BRANCH": "1MZ1", "NAMA BRANCH": "PARUNG"}, "PNK": {"KODE BRANCH": "1PZ1", "NAMA BRANCH": "PONTIANAK"}, "LBK": {"KODE BRANCH": "1SZ1", "NAMA BRANCH": "LOMBOK"}, "KBI": {"KODE BRANCH": "1VZ1", "NAMA BRANCH": "KOTABUMI"}, "MDO": {"KODE BRANCH": "1YZ1", "NAMA BRANCH": "MANADO"}, "RBG": {"KODE BRANCH": "2AZ1", "NAMA BRANCH": "REMBANG"}, "BTM": {"KODE BRANCH": "2DZ1", "NAMA BRANCH": "BATAM"}, "SRG": {"KODE BRANCH": "2GZ1", "NAMA BRANCH": "SERANG"}, "CJR": {"KODE BRANCH": "2JZ1", "NAMA BRANCH": "CIANJUR"}, "MDU": {"KODE BRANCH": "2MZ1", "NAMA BRANCH": "MADIUN"}, "TGL": {"KODE BRANCH": "2PZ1", "NAMA BRANCH": "TEGAL"}, "GTO": {"KODE BRANCH": "2SZ1", "NAMA BRANCH": "GORONTALO"}, "LWU": {"KODE BRANCH": "2VZ1", "NAMA BRANCH": "LUWU"}, "BDG": {"KODE BRANCH": "BZ01", "NAMA BRANCH": "BANDUNG"}, "BKS": {"KODE BRANCH": "CZ01", "NAMA BRANCH": "BEKASI"}, "SMG": {"KODE BRANCH": "HZ01", "NAMA BRANCH": "SEMARANG"}, "CLC": {"KODE BRANCH": "IZ01", "NAMA BRANCH": "CILACAP"}, "CS2": {"KODE BRANCH": "JZ01", "NAMA BRANCH": "CILEUNGSI 2"}, "CKK": {"KODE BRANCH": "KZ01", "NAMA BRANCH": "CIKOKOL"}, "LPG": {"KODE BRANCH": "LZ01", "NAMA BRANCH": "LAMPUNG"}, "MLG": {"KODE BRANCH": "MZ01", "NAMA BRANCH": "MALANG"}, "BG2": {"KODE BRANCH": "NZ01", "NAMA BRANCH": "BANDUNG 2"}, "KTN": {"KODE BRANCH": "OZ01", "NAMA BRANCH": "KLATEN"}, "PLG": {"KODE BRANCH": "PZ01", "NAMA BRANCH": "PALEMBANG"}, "BLI": {"KODE BRANCH": "QZ01", "NAMA BRANCH": "BALI"}, "MKS": {"KODE BRANCH": "RZ01", "NAMA BRANCH": "MAKASAR"}, "BLJ": {"KODE BRANCH": "TZ01", "NAMA BRANCH": "BALARAJA"}, "SDJ": {"KODE BRANCH": "UZ01", "NAMA BRANCH": "SIDOARJO"}, "PBN": {"KODE BRANCH": "VZ01", "NAMA BRANCH": "PLUMBON"}, "MDN": {"KODE BRANCH": "WZ01", "NAMA BRANCH": "MEDAN"}, "BGR": {"KODE BRANCH": "XZ01", "NAMA BRANCH": "BOGOR"}, "JBR": {"KODE BRANCH": "YZ01", "NAMA BRANCH": "JEMBER"} }

st.title("Transformasi dan Filter Data Produk")
uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    transformed_df = transform_data(df, data_branch)
    
    divisi_filter = st.selectbox("Pilih Divisi", [""] + list(set(transformed_df["Divisi"].dropna())))
    if divisi_filter:
        transformed_df = transformed_df[transformed_df["Divisi"] == divisi_filter]
    
    plu_filter = st.text_input("Filter PLU")
    descp_filter = st.text_input("Filter Descp")
    branch_filter = st.multiselect("Filter Nama Branch", list(set(transformed_df["NAMA BRANCH"].dropna())))
    tag_filter = st.multiselect("Filter Tag", list(set(transformed_df["Tag"].dropna())))
    
    if plu_filter:
        transformed_df = transformed_df[transformed_df["PLU"].astype(str).str.contains(plu_filter, na=False)]
    if descp_filter:
        transformed_df = transformed_df[transformed_df["Descp"].astype(str).str.contains(descp_filter, case=False, na=False)]
    if branch_filter:
        transformed_df = transformed_df[transformed_df["NAMA BRANCH"].isin(branch_filter)]
    if tag_filter:
        transformed_df = transformed_df[transformed_df["Tag"].isin(tag_filter)]
    
    st.dataframe(transformed_df)
