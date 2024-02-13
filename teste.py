import PyPDF2

def analyze_pdf_structure(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        fillable_fields = pdf_reader.get_form_text_fields()
    return fillable_fields

def fill_pdf_fields(input_pdf_path, output_pdf_path, data_to_fill):
    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()
        print(len(reader.pages[0].annotations))

        # Copy all pages from reader to writer
        for page_number in range(len(reader.pages)):
            writer.add_page(reader.pages[page_number])

        # Update the fields
        writer.update_page_form_field_values(writer.pages[0], data_to_fill)
        print(writer.pages[0].annotations[0])

        # Write the modified content to a new file
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

# Usage example
input_pdf_path = 'teste.pdf'
output_pdf_path = 'filled_base.pdf'
fillable_fields = analyze_pdf_structure(input_pdf_path)

# Define the data you want to fill
data_to_fill = {field_name: 'Your Value' for field_name in fillable_fields.keys()}

# Fill the PDF
fill_pdf_fields(input_pdf_path, output_pdf_path, data_to_fill)

