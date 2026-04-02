import pandas as pd
import io
from fastapi import Response

def create_pivot_csv(csv_data: str):
    # CSV Data ko Pandas mein lo
    df = pd.read_csv(io.StringIO(csv_data))
    
    cat_cols = df.select_dtypes(exclude=['number']).columns
    num_cols = df.select_dtypes(include=['number']).columns

    # Category ke basis par Numbers ka Total (Sum)
    if len(cat_cols) > 0 and len(num_cols) > 0:
        pivot_df = df.groupby(cat_cols[0])[num_cols].sum().reset_index()
    else:
        pivot_df = df.describe().reset_index()

    # Wapas CSV format mein convert karo
    output = io.StringIO()
    pivot_df.to_csv(output, index=False)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=pivot_report.csv"}
    )
