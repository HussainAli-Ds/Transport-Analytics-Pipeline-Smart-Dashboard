from sqlalchemy import create_engine, text
from config import DB_URL

engine = create_engine(DB_URL)

def insert_data(df):

    if df.empty:
        print("⚠️ No valid data")
        return

    records = df.to_dict(orient="records")

    query = """
    INSERT INTO transportors (
        dated, transporter, vehicle_no, material,
        zkb_slip_no, supplier_slip_no, location,
        from_location, to_location, trips,
        zkb_qty_cft, tons
    )
    VALUES (
        :dated, :transporter, :vehicle_no, :material,
        :zkb_slip_no, :supplier_slip_no, :location,
        :from_location, :to_location, :trips,
        :zkb_qty_cft, :tons
    )
    ON CONFLICT (dated, transporter, vehicle_no, material, zkb_slip_no)
    DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(text(query), records)

    print(f"✅ Inserted {len(records)} rows")