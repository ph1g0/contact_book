# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:36:37 2022

@author: phigo
"""

"""This module deals with accessing and modifying PDFs"""

import pdfrw



# Set up variables to find form fields in the pdf
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'



def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    """Identify form fields in input PDF and generate output PDF"""
    # Read PDF and save it in template_pdf
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    
    # Loop through the pages of the pdf and identify form fields (key)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    
                    # Fill out form fields with values in data_dict
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
                            
    # The following code is necessary to show the values in the form fields
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    
def fill_simple_pdf_file(data, template_input, template_output):
    """Fill out form fields in the PDF with values in data_dict"""
    data_dict = {
        'Textfeld 1': data.get('name', ''),
        'Textfeld 2': data.get('street', ''),
        'Textfeld 3': data.get('city', ''),
    }
    return fill_pdf(template_input, template_output, data_dict)



if __name__ == '__main__':
    pdf_template = "test_form.pdf"
    pdf_output = "output.pdf"
    
    sample_data_dict = {
        'name': 'Marius Paparius',
        'street': 'Wolfsleite 23',
        'city': '91074 Herzogenaurach',
    }
    fill_simple_pdf_file(sample_data_dict, pdf_template, pdf_output)