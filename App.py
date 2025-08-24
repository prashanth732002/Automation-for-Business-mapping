import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Branch Role Mapping", layout="centered")

st.title("📊 Branch Role Mapping Tool")
st.write("Upload your Excel file and get a cleaned role mapping output (SM, AM, DM, RM, SH).")

# File upload
uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Rename BM as SM for consistency
    df.rename(columns={"BM Names": "SM Name", "BM Emp ID": "SM Emp ID"}, inplace=True)

    # Define roles
    roles = {
        "SM": ("SM Name", "SM Emp ID"),
        "AM": ("AM Name", "AM Emp ID"),
        "DM": ("DM Name", "DM Emp ID"),
        "RM": ("RM Name", "RM Emp ID"),
        "SH": ("SH Name", "SH Emp ID"),
    }

    role_data = []

    for role, (name_col, emp_col) in roles.items():
        if name_col in df.columns and emp_col in df.columns:
            temp = df[["Branch", "Branch ID", "State", name_col, emp_col]].copy()
            temp.columns = ["Branch", "Branch ID", "State", "Name", "Emp ID"]
            temp["Role"] = role
            role_data.append(temp)

    # Combine all role DataFrames
    final_df = pd.concat(role_data, ignore_index=True)

    # Show sample data
    st.subheader("🔍 Processed Preview")
    st.dataframe(final_df.head(20))

    # Download as Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Role_Mapping")
        return output.getvalue()

    excel_data = to_excel(final_df)

    st.download_button(
        label="⬇️ Download Excel File",
        data=excel_data,
        file_name="Branch_Role_Mapping.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Download as CSV
    csv_data = final_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV File",
        data=csv_data,
        file_name="Branch_Role_Mapping.csv",
        mime="text/csv",
    )
