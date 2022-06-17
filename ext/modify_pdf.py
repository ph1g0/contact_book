# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:36:37 2022

@author: ph1g0
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



def fillPdf(data_dict, input_pdf):
    """
    Identify form fields in input PDF, fill out with data_dict
    and generate output PDF
    """
    output_pdf = "output.pdf"
    
    # Read PDF and save it in template_pdf
    template_pdf = pdfrw.PdfReader(input_pdf)
    
    # Loop through the pages of the pdf and identify form fields (key)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]

                    # Fill out form field with value in data_dict
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
    pdfrw.PdfWriter().write(output_pdf, template_pdf)
    