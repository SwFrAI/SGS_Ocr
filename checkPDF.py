def open_check_pdf(path, option="*April"):
    import pandas as pd
    import pdfplumber, re, os, time, json
    from pikepdf import Pdf
    import PyPDF2
    from urllib.request import urlopen

    with pdfplumber.open(path) as pdf:
        p0 = pdf.pages[0]
        table = p0.extract_table()
        im = p0.to_image()
    im.reset().draw_rects(p0.chars)
    text = p0.extract_text()
    pattern = re.compile(r'物性.{}'.format(option), re.DOTALL)
    if re.search(pattern, text) != None:
        datas = re.search(pattern, text).group(0)
        print("屬於非表格式")
        print("=" * 50)
        return datas
    elif p0.extract_tables() != []:
        datas = p0.extract_tables()[0]
        print("屬於表格式")
        print("=" * 50)
        return datas
    else:
        return "無法辨識的格式"

if __name__ == '__main__':
    print(open_check_pdf(r'PA-757H-TDS-ASTM.pdf'))
