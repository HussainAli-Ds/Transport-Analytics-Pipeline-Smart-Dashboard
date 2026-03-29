import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Transport Dashboard", layout="wide")

DB_URL = "postgresql+psycopg2://hussainali:hussain12@localhost:5432/supplier"
engine = create_engine(DB_URL)

# =========================
# GLOBAL NUMBER FORMAT
# =========================
pd.options.display.float_format = '{:,.2f}'.format

# =========================
# FORMAT FUNCTION
# =========================
def format_numbers(df):
    return df.style.format({
        "trips": "{:,}",
        "zkb_qty_cft": "{:,.2f}",
        "tons": "{:,.2f}",
        "Trips": "{:,}",
        "CFT": "{:,.2f}",
        "Tons": "{:,.2f}"
    })

# =========================
# EXCEL EXPORT
# =========================
def convert_to_excel(df):
    output = io.BytesIO()
    try:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
    except:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    return output.getvalue()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    query = "SELECT * FROM transportors"
    df = pd.read_sql(query, engine)

    df["dated"] = pd.to_datetime(df["dated"], errors="coerce")
    df = df.dropna(subset=["dated"])

    return df

df = load_data()

# =========================
# EMPTY CHECK
# =========================
if df.empty:
    st.error("🚨 No data found in database")
    st.stop()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("🔍 Filters")

min_date = df["dated"].min()
max_date = df["dated"].max()

start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

transporters = st.sidebar.multiselect(
    "Transporter",
    df["transporter"].unique(),
    default=df["transporter"].unique()
)

locations = st.sidebar.multiselect(
    "Location",
    df["to_location"].unique(),
    default=df["to_location"].unique()
)

materials = st.sidebar.multiselect(
    "Material",
    df["material"].unique(),
    default=df["material"].unique()
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["dated"] >= pd.to_datetime(start_date)) &
    (df["dated"] <= pd.to_datetime(end_date)) &
    (df["transporter"].isin(transporters)) &
    (df["to_location"].isin(locations)) &
    (df["material"].isin(materials))
]

# =========================
# PRINT BUTTON
# =========================
st.markdown("""
<script>
function printPage() {
    window.print();
}
</script>
<button onclick="printPage()" style="
    background-color:#4CAF50;
    color:white;
    padding:10px 20px;
    border:none;
    border-radius:5px;
    cursor:pointer;
">
🖨️ Print Report
</button>
""", unsafe_allow_html=True)

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📊 Dashboard", "📋 Summary"])

# =========================================================
# DASHBOARD TAB
# =========================================================
with tab1:

    st.title("📊 Transport Dashboard")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    total_trips = filtered_df["trips"].sum()
    total_tons = filtered_df["tons"].sum()

    top_transporter = (
        filtered_df.groupby("transporter")["trips"]
        .sum().sort_values(ascending=False).index[0]
        if not filtered_df.empty else "-"
    )

    top_material = (
        filtered_df["material"].value_counts().index[0]
        if not filtered_df.empty else "-"
    )

    col1.metric("Total Trips", f"{total_trips:,}")
    col2.metric("Total Tons", f"{total_tons:,.2f}")
    col3.metric("Top Transporter", top_transporter)
    col4.metric("Top Material", top_material)

    st.divider()

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Trips by Transporter")
        st.bar_chart(filtered_df.groupby("transporter")["trips"].sum())

    with c2:
        st.subheader("Tons by Material")
        st.bar_chart(filtered_df.groupby("material")["tons"].sum())

    # Location Analysis
    st.subheader("📍 Location Analysis")

    loc_df = filtered_df.groupby("to_location").agg({
        "trips": "sum",
        "tons": "sum"
    }).sort_values("trips", ascending=False)

    st.dataframe(
        loc_df.style.format({
            "trips": "{:,}",
            "tons": "{:,.2f}"
        }),
        use_container_width=True
    )

    # Material Summary
    st.subheader("📦 Material Summary")

    mat_df = filtered_df.groupby("material").agg({
        "trips": "sum",
        "zkb_qty_cft": "sum",
        "tons": "sum"
    }).rename(columns={"zkb_qty_cft": "CFT"})

    st.dataframe(
        mat_df.style.format({
            "trips": "{:,}",
            "CFT": "{:,.2f}",
            "tons": "{:,.2f}"
        }),
        use_container_width=True
    )

    # DOWNLOAD FILTERED DATA
    st.subheader("⬇️ Download Filtered Data")

    excel_data = convert_to_excel(filtered_df)

    st.download_button(
        label="📥 Download Excel",
        data=excel_data,
        file_name="filtered_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "📥 Download CSV",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

    # Detailed Data
    st.subheader("📄 Detailed Data")

    st.dataframe(format_numbers(filtered_df), use_container_width=True)

# =========================================================
# SUMMARY TAB
# =========================================================
with tab2:

    st.title("📋 Transport Summary (Excel Style)")

    s1, s2 = st.columns(2)

    summary_start = s1.date_input("Start Date", min_date, key="s1")
    summary_end = s2.date_input("End Date", max_date, key="s2")

    summary_df = df[
        (df["dated"] >= pd.to_datetime(summary_start)) &
        (df["dated"] <= pd.to_datetime(summary_end))
    ]

    if summary_df.empty:
        st.warning("No data in selected range")
        st.stop()

    grouped = summary_df.groupby(
        ["transporter", "material"]
    ).agg(
        Trips=("trips", "sum"),
        CFT=("zkb_qty_cft", "sum"),
        Tons=("tons", "sum")
    ).reset_index()

    # EXPORT SUMMARY
    st.subheader("⬇️ Export Summary")

    summary_excel = convert_to_excel(grouped)

    st.download_button(
        label="📥 Download Summary",
        data=summary_excel,
        file_name="summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # DISPLAY SUMMARY
    grand_trips = 0
    grand_cft = 0
    grand_tons = 0

    for t in grouped["transporter"].unique():

        sub = grouped[grouped["transporter"] == t]

        st.markdown(f"### 🚚 {t}")

        st.dataframe(format_numbers(sub), use_container_width=True)

        t_trips = sub["Trips"].sum()
        t_cft = sub["CFT"].sum()
        t_tons = sub["Tons"].sum()

        grand_trips += t_trips
        grand_cft += t_cft
        grand_tons += t_tons

        st.markdown(
            f"**Total → Trips:** {t_trips:,} | **CFT:** {t_cft:,.2f} | **Tons:** {t_tons:,.2f}"
        )

        st.divider()

    # GRAND TOTAL
    st.subheader("📊 Grand Total")

    g1, g2, g3 = st.columns(3)
    g1.metric("Trips", f"{grand_trips:,}")
    g2.metric("CFT", f"{grand_cft:,.2f}")
    g3.metric("Tons", f"{grand_tons:,.2f}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
**Created by Hussain-Ali**  
📧 ha780383@gmail.com  
📞 03357897412 | 03318782469  
""")