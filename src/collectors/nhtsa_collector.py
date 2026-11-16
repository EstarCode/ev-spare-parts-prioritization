# NHTSA Datasets and APIs Data Collector Module.
import requests
from typing import Dict, Any
from src.collectors.base_collector import BaseCollector
from src.utils.date_utils import get_current_date_str
from src.utils.file_utils import save_json

# Data collector for NHTSA Datasets and APIs (nhtsa). Ingests, parses, and normalizes evidence records for the EV spare-parts study.
class NhtsaCollector(BaseCollector):
    def __init__(self):
        super().__init__(
            source_id="nhtsa",
            source_name="NHTSA Datasets and APIs",
            source_url="https://www.nhtsa.gov/nhtsa-datasets-and-apis",
            evidence_type="GOVERNMENT_DATASET",
            raw_dir_name="nhtsa"
        )
        self.api_base = "https://api.nhtsa.gov"

    def collect(self) -> Dict[str, Any]:
        self.logger.info("Executing NHTSA API Collector for Complaints and Recalls...")
        complaints_list = []
        recalls_list = []
        
        vehicles_to_query = [
            ("toyota", "bz4x", "2023"),
            ("toyota", "bz4x", "2024"),
            ("volkswagen", "id.4", "2023"),
            ("volkswagen", "id.4", "2022"),
            ("byd", "seagull", "2024"),
            ("changan", "benben", "2023")
        ]
        
        current_date = get_current_date_str()
        
        for make, model, year in vehicles_to_query:
            c_url = f"{self.api_base}/complaints/complaintsByVehicle?make={make}&model={model}&modelYear={year}"
            self.logger.info(f"Querying NHTSA Complaints: {make} {model} {year}")
            try:
                res = requests.get(c_url, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", [])
                    self.logger.info(f"Found {len(results)} complaints for {make} {model} {year}")
                    
                    save_json(data, self.raw_dir / f"complaints_{make}_{model}_{year}.json")
                    
                    for item in results:
                        comp = item.get("components", "") or ""
                        summary = item.get("summary", "") or ""
                        
                        odi = str(item.get("odiNumber", ""))
                        complaint_rec = {
                            "complaint_id": f"NHTSA-CMP-{odi}",
                            "manufacturer": item.get("manufacturer", make.upper()),
                            "model": model.upper(),
                            "model_year": year,
                            "complaint_date": item.get("dateComplaintFiled", ""),
                            "component": comp,
                            "summary": summary[:400].replace("\n", " "),
                            "crash": "Yes" if item.get("crash", False) else "No",
                            "fire": "Yes" if item.get("fire", False) else "No",
                            "injuries": str(item.get("numberOfInjuries", 0)),
                            "deaths": str(item.get("numberOfDeaths", 0)),
                            "source_url": c_url,
                            "collection_date": current_date
                        }
                        complaints_list.append(complaint_rec)
                else:
                    self.log_error(c_url, f"HTTP_{res.status_code}", f"NHTSA complaints request returned {res.status_code}")
            except Exception as e:
                self.log_error(c_url, "REQUEST_EXCEPTION", str(e))

            r_url = f"{self.api_base}/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
            self.logger.info(f"Querying NHTSA Recalls: {make} {model} {year}")
            try:
                res = requests.get(r_url, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", [])
                    self.logger.info(f"Found {len(results)} recalls for {make} {model} {year}")
                    
                    save_json(data, self.raw_dir / f"recalls_{make}_{model}_{year}.json")
                    
                    for item in results:
                        camp_num = item.get("NHTSACampaignNumber", "")
                        recall_rec = {
                            "recall_number": camp_num,
                            "manufacturer": item.get("Manufacturer", make.upper()),
                            "model": model.upper(),
                            "model_year": year,
                            "component": item.get("Component", ""),
                            "recall_description": (item.get("Summary", "") or "")[:400].replace("\n", " "),
                            "consequence": (item.get("Consequence", "") or item.get("Conequence", "") or "")[:400].replace("\n", " "),
                            "remedy": (item.get("Remedy", "") or "")[:400].replace("\n", " "),
                            "source_url": r_url,
                            "collection_date": current_date
                        }
                        recalls_list.append(recall_rec)
                else:
                    self.log_error(r_url, f"HTTP_{res.status_code}", f"NHTSA recalls request returned {res.status_code}")
            except Exception as e:
                self.log_error(r_url, "REQUEST_EXCEPTION", str(e))

        self.logger.info(f"NHTSA collection completed: {len(complaints_list)} complaints, {len(recalls_list)} recalls.")
        save_json(complaints_list, self.raw_dir / "all_extracted_complaints.json")
        save_json(recalls_list, self.raw_dir / "all_extracted_recalls.json")
        
        return {
            "complaints": complaints_list,
            "recalls": recalls_list
        }
