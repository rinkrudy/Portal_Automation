import requests
from patent_client import GlobalDossier
import json
from datetime import date, datetime
import pandas as pd




class GlobalDossierApi:
    def __init__(self) -> None:
        # 발급받은 인증 토큰 (예시 토큰)
        self._client = GlobalDossier.objects
    """
    {
    "applicationNumberText": "15958569",
    "mailRoomDate": "2019-11-22T14:08:46.000Z",
    "documentCode": "N417",
    "documentDescription": "Electronic Filing System Acknowledgment Receipt",
    "documentCategory": "PROSECUTION",
    "accessLevelCategory": "PUBLIC",
    "documentIdentifier": "K3ATFLD1RXEAPX3",
    "pageCount": 3,
    "pdfUrl": "pdfDocument/15958569/K3ATFLD1RXEAPX3"
    },
    """

    def find_items(self, target):
        return [item for item in self if item == target]
    

    def get_documents(self, app_number):
        try:
            response =  self._client.get(app_number, type="application")
            country = app_number[:2]
            applications = dict(response.items())["applications"]
            print(applications)
            target_application = [item for item in applications if (item.app_num == app_number[2:]) and (item.country_code == country)][0]
            list_doc = target_application.document_list.docs

            return list_doc
        
        except Exception as e :
            print(e)

    

    def get_dossier(self, app_number):  
        try:
            list_doc = self.get_documents(app_number)

            arr_dict_result = []

            for doc in list_doc:
                print(doc)
                arr_dict_result.append({"Date" : doc.date, "Doc_Desc" : doc.doc_desc,"Doc_Format" : doc.doc_format, "Doc_Code_Desc" : doc.doc_code_desc})
            

            df_result = pd.DataFrame(arr_dict_result)
            
            return  df_result.sort_values(by = "Date", ascending=False).reset_index(drop=True)


        except Exception as e:
            print(e)
            return None



    def download_pdf(self, app_number, doc_desc, date: datetime.date, download_path):
        arr_docs = self.get_documents(app_number)

        for doc in arr_docs:
            print(type(doc.date))
            print(doc.date)
            print(doc.date == date)            

        target_doc =  [item for item in arr_docs if ((item.doc_desc == doc_desc) and (item.date == date))][0]

        target_doc.download(download_path)
        

        
        
    def parse_global_dossier_to_dict(self, inst_global_dossier):
        extract_keys_basic_type = ["app_num", "app_date", "country_code", ]
        dict_app_info = dict(inst_global_dossier.items())
        dict_result = {}
        print(dict(dict_app_info["doc_num"]))
        for key in extract_keys_basic_type:
            dict_result[key] = dict_app_info[key]
        
        arr_priority = []
        for priority in dict_app_info["priority_claim_list"]:
            dict_priority = dict(priority.items())
            arr_priority.append("_".join([dict_priority["country"], dict_priority["doc_number"], dict_priority["kind_code"]]))
        
        
        dict_result["priority_claim_list"] = "/".join(arr_priority)

        arr_pub = []
        for pub in dict_app_info["pub_list"]:
            dict_pub = dict(pub.items())
            arr_pub.append("_".join([dict_pub["pub_country"], dict_pub["pub_num"], dict_pub["kind_code"]]))
            
        dict_result["pub_list"] = "/".join(arr_pub)
        
        
        return dict_result
    
    



    """
        Gobal Dossier instance info
        {'app_num': '15958569'
        ,'app_date': datetime.date(2018, 4, 20)
        ,'country_code': 'US'
        ,'kind_code': 'A'
        ,'doc_num': GlobalDossierDocumentNumber(country='US', doc_number='201815958569', format=None, date=datetime.date(2018, 4, 20), kind_code='A')
        ,'title': 'PHASED ARRAY MODULAR HIGH-FREQUENCY SOURCE'
        ,'applicant_names': ['KRAUS, PHILIP ALLAN'
        ,'CHUA, THAI CHENG'
        ,'AMORMINO, CHRISTIAN'
        ,'DZILNO, DMITRY A.']
        ,'ip_5': True
        ,'priority_claim_list': [GlobalDossierPriorityClaim(country='US', doc_number='15958569', kind_code='A')]
        ,'pub_list': [GlobalDossierPublication(pub_country='US', pub_num='20190326096', kind_code='A1', pub_date=datetime.date(2019, 10, 24)), GlobalDossierPublication(pub_country='US', pub_num='10504699', kind_code='B2', pub_date=datetime.date(2019, 12, 10))]
        }
    """

    def get_family(self, app_number, filter_country_codes = ["US", "KR","JP", "CN"]):
        arr_dict_result = []
        # extract_keys_ = ["app_num", "app_date", "country_code", "title", "applicant_names", "priority_claim_list", "pub_list"]
        try:
            response =  self._client.get(app_number, type="application")
            print(dict(response.items()))
            applications = dict(response.items())["applications"]

            for app in applications:
                dict_result = self.parse_global_dossier_to_dict(app)    
                arr_dict_result.append(dict_result)

            df_result = pd.DataFrame(arr_dict_result)
            print(df_result)
            df_filtered = df_result[df_result["country_code"].isin(filter_country_codes)].reset_index(drop=True)
            
            return df_filtered

        except Exception as e:
            print(e)
            return None

