from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.styles.borders import Border, Side, BORDER_THIN
from io import BytesIO
from ..model import Order, Status


def generate_xlsx_report():
    colors = {
        Status.NEW.value: "2192FF",
        Status.IN_PROGRESS.value: "FDFF00",
        Status.COMPLETED.value: "38E54D",
    }

    thin_border = Border(
        left=Side(border_style=BORDER_THIN),
        right=Side(border_style=BORDER_THIN),
        top=Side(border_style=BORDER_THIN),
        bottom=Side(border_style=BORDER_THIN),
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    ws.append(["ID", "Name", "Description", "Creation Date", "Status"])

    for cell in ws["1:1"]:
        cell.font = Font(bold=True)
        cell.border = thin_border

    orders = Order.query.all()
    for order in orders:
        row = [
            order.id,
            order.name,
            order.description,
            order.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
            order.status.value,
        ]
        ws.append(row)
        fill = PatternFill(
            start_color=colors[order.status.value],
            end_color=colors[order.status.value],
            fill_type="solid",
        )
        for cell in ws[ws.max_row]:
            cell.fill = fill
            cell.border = thin_border

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column_letter].width = adjusted_width

    report = BytesIO()
    wb.save(report)
    report.seek(0)

    return report
