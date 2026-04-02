import pandas as pd
import io
from fastapi import Response

def create_pivot_csv(csv_data: str):
    try:
        df = pd.read_csv(io.StringIO(csv_data))

        cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        num_cols = df.select_dtypes(include=['number']).columns.tolist()

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            # ✅ Pivot 1: Category wise Sum
            if len(cat_cols) > 0 and len(num_cols) > 0:
                pivot1 = df.groupby(cat_cols[0])[num_cols].sum().reset_index()
                pivot1.to_excel(writer, sheet_name="Category Sum", index=False)

            # ✅ Pivot 2: Category wise Mean
            if len(cat_cols) > 0 and len(num_cols) > 0:
                pivot2 = df.groupby(cat_cols[0])[num_cols].mean().reset_index()
                pivot2.to_excel(writer, sheet_name="Category Avg", index=False)

            # ✅ Pivot 3: Count of records per category
            if len(cat_cols) > 0:
                pivot3 = df.groupby(cat_cols[0]).size().reset_index(name="Count")
                pivot3.to_excel(writer, sheet_name="Category Count", index=False)

            # ✅ Pivot 4: Overall Summary (describe)
            pivot4 = df.describe().reset_index()
            pivot4.to_excel(writer, sheet_name="Summary Stats", index=False)

        output.seek(0)

        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=pivot_report.xlsx"
            }
        )

    except Exception as e:
        return Response(
            content=f"Error: {str(e)}",
            status_code=500
        )
