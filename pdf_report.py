from fpdf import FPDF

def generate_pdf(route_report):

    pdf = FPDF()

    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,"Shivamogga Bus Delay Analysis",ln=True)

    for i,row in route_report.iterrows():

        text = f"Route {row['route_id']} Avg Delay: {row['avg_delay']}"

        pdf.cell(200,10,text,ln=True)

    pdf.output("output/report.pdf")