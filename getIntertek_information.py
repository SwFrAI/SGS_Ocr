import pandas as pd
import pdfplumber, re, os, time, json
from pikepdf import Pdf
import PyPDF2
from urllib.request import urlopen

def getTest_information(text):
    #取得名稱 & 日期 & 編號
    pattern_number = '[Nn]umber\s{0,5}:\s{0,5}(.*\w)'
    pattern_name = '[Ss]ample [Dd]escription\s{0,5}:\s{0,5}(.*\w)'
    pattern_date = '[Dd]ate\s{0,5}:\s{0,5}(.*\w)'
    
    match_number = re.search(pattern_number, text)
    match_name = re.search(pattern_name, text)
    match_date = re.search(pattern_date, text)
    
    number = match_number.group(1)
    name = match_name.group(1)
    date = match_date.group(1)
    
    return number, name, date


def check_res_dict(res_dict):
    for key in res_dict:
        
        if key == '測試項目':
            for line in res_dict[key]:
                print(line)
        else:
            print(key, res_dict[key])


def get_pdf_data(path):
    res_dict = {}
    test_item_list = []

    with pdfplumber.open(path) as pdf:
        for index, p_name in enumerate(pdf.pages):
            text = p_name.extract_text()
            
            if index == 0:                   
                number, name, date = getTest_information(text)            
                #print(number, name, date)
                res_dict["報告編號"] = number
                res_dict["樣品名稱"] = name
                res_dict["檢測日期"] = date

            if p_name.extract_table() != None:        
                table_data = p_name.extract_table()
                
                if 'test item' in table_data[0][0].lower():                
                    for line in table_data[1:]:
                        if line[0] != None:
                            
                            test_item = line[0].replace('\n', "")
                            result_value = line[3]
                            rl_value = line[4]
                            
                            if test_item != None and result_value != None:
                                #print(test_item)#, result_value, rl_value)
                                test_item_list.append([test_item, result_value, rl_value])
                                
                    res_dict["測試項目"] = test_item_list
    return res_dict, number


def write_json(path, file_name, data_json):

    with open(r'{}\{}.json'.format(path, file_name), 'w', encoding='utf-8-sig') as f:
        time.sleep(1)
        json.dump(data_json, f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    input_path = r"data\Intertek\TWNC00883087--MGB_MIP_MCB_MHC_MFI_MPA+Series.pdf"

    data_json, report_number = get_pdf_data(input_path)
    write_json('final', report_number, data_json)