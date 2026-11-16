# Source Accessibility and Endpoint Audit Module.
import sys
import time
import yaml
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.http_client import HttpClient
from src.utils.file_utils import save_csv, save_text, ensure_dir
from src.utils.date_utils import get_utc_now_iso
from src.utils.logger import get_logger

logger = get_logger("source_validator")

# Execute Phase 1 accessibility audit across all 19 configured sources. Probes HTTP status codes, measures latency, inspects content for anti-bot challenges (e.g. Cloudflare), and saves raw audit snapshots.
def run_source_audit():
    project_root = Path(__file__).resolve().parent.parent.parent
    config_path = project_root / "config" / "sources.yaml"
    raw_base = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    reports_dir = project_root / "reports"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    client = HttpClient(delay_seconds=1.0, timeout=15)
    audit_results = []
    
    logger.info("Starting comprehensive Phase 1 Source Accessibility Audit...")
    
    for src in config.get("sources", []):
        src_id = src["id"]
        src_name = src["name"]
        url = src["url"]
        logger.info(f"Auditing source: {src_name} ({url})")
        
        raw_folder_map = {
            "adey_market": "adey_market",
            "gezat": "gezat",
            "landin": "landin",
            "cqs": "cqs",
            "toyota_catalogue": "toyota_catalogue",
            "vw_catalogue": "vw_catalogue",
            "nhtsa": "nhtsa",
            "sunny_spare_parts": "sunny_spare_parts",
            "armana_motors": "armana_motors",
            "ethio_ev_spare": "ethio_ev_spare",
            "moenco": "moenco",
            "byd_ethiopia": "byd_ethiopia",
            "sparehub": "sparehub",
            "ev_spare_app": "ev_spare_app",
            "ethiocars": "ethiocars",
            "ethiodrive": "ethiodrive",
            "cargebeya": "cargebeya",
            "quralew": "quralew",
            "autoline": "autoline"
        }
        raw_dir = raw_base / raw_folder_map.get(src_id, src_id)
        ensure_dir(raw_dir)
        
        start_time = time.time()
        status_code, text, json_data, error = client.get(url)
        elapsed = round(time.time() - start_time, 2)
        
        is_accessible = "Yes" if status_code in [200, 301, 302] else "No"
        
        has_relevant_data = "No"
        data_types = "Unknown"
        access_restrictions = "None"
        reliability_score = "Low"
        limitations = ""
        next_action = ""
        
        if is_accessible == "Yes":
            data_types = "HTML" if not json_data else "JSON / API"
            lower_text = text.lower()
            
            save_text(text, raw_dir / "audit_snapshot.html")
            
            if "cf-browser-verification" in lower_text or "cloudflare" in lower_text and "challenge" in lower_text:
                access_restrictions = "Cloudflare Challenge / Anti-bot"
                reliability_score = "Blocked / Anti-bot"
                has_relevant_data = "Blocked"
                limitations = "Requires human interactive challenge or JS solver. Access blocked by anti-bot."
                next_action = "Document access block and examine alternative mirrors or direct APIs."
            elif status_code == 200:
                has_keywords = any(k in lower_text for k in ["byd", "toyota", "volkswagen", "changan", "electric", "ev", "parts", "car", "auto", "nhtsa"])
                if has_keywords:
                    has_relevant_data = "Yes"
                    reliability_score = "High" if src["evidence_type"] in ["OFFICIAL_MANUFACTURER", "AUTHORIZED_DISTRIBUTOR", "GOVERNMENT_DATASET"] else "Medium"
                    limitations = "Public HTML content. Subject to client-side rendering or pagination."
                    next_action = "Implement targeted scraper / parser."
                else:
                    has_relevant_data = "Partial / Generic"
                    reliability_score = "Medium"
                    limitations = "Generic homepage or directory without direct product tables."
                    next_action = "Probe subpages or search endpoints."
            else:
                limitations = f"Received HTTP {status_code}"
                next_action = "Check alternative URL or protocol."
        else:
            access_restrictions = error or f"HTTP {status_code}"
            limitations = f"Connection failed or server error: {error or status_code}"
            next_action = "Record as inaccessible and log error."

        record = {
            "source_id": src_id,
            "source_name": src_name,
            "source_url": url,
            "is_accessible": is_accessible,
            "http_status": status_code,
            "response_time_sec": elapsed,
            "has_relevant_data": has_relevant_data,
            "data_types": data_types,
            "extraction_method": "HTTP_REQUESTS",
            "access_restrictions": access_restrictions,
            "reliability_score": reliability_score,
            "limitations": limitations,
            "next_action": next_action
        }
        audit_results.append(record)
        logger.info(f"Source {src_name}: Accessible={is_accessible}, Status={status_code}, Elapsed={elapsed}s, Data={has_relevant_data}")

    logger.info("Auditing Adey Market Parts URL...")
    adey_parts_url = "https://adey-market.com/categories/vehicle_parts?type=car_spare_parts_general"
    _s_code, t_text, _, _err = client.get(adey_parts_url)
    if t_text:
        save_text(t_text, raw_base / "adey_market" / "parts_audit_snapshot.html")

    save_csv(audit_results, processed_dir / "source_accessibility.csv")
    
    generate_accessibility_report(audit_results, reports_dir / "source_accessibility_report.md")
    logger.info("Source accessibility audit complete and saved.")
    return audit_results

# Generate structured Markdown summary of source accessibility audit findings.
def generate_accessibility_report(results: list, report_path: Path) -> None:
    lines = [
        "# Source Accessibility and Reliability Assessment Report",
        "",
        f"**Audit Execution Timestamp:** {get_utc_now_iso()}",
        f"**Total Sources Audited:** {len(results)}",
        "",
        "## Summary of Findings",
        "",
        "| Source ID | Source Name | Accessible | HTTP Status | Response Time (s) | Relevant Data | Reliability | Access Restrictions | Next Action |",
        "|-----------|-------------|------------|-------------|-------------------|---------------|-------------|---------------------|-------------|"
    ]
    for r in results:
        lines.append(
            f"| `{r['source_id']}` | {r['source_name']} | **{r['is_accessible']}** | {r['http_status']} | {r['response_time_sec']} | {r['has_relevant_data']} | {r['reliability_score']} | {r['access_restrictions']} | {r['next_action']} |"
        )
    lines.extend([
        "",
        "## Detailed Source Breakdown and Audit Observations",
        ""
    ])
    for r in results:
        lines.extend([
            f"### {r['source_name']} (`{r['source_id']}`)",
            f"- **URL:** {r['source_url']}",
            f"- **Accessibility Status:** {'ACCESSIBLE' if r['is_accessible'] == 'Yes' else 'INACCESSIBLE'}",
            f"- **HTTP Status Code:** {r['http_status']}",
            f"- **Response Latency:** {r['response_time_sec']} seconds",
            f"- **Relevant Data Detected:** {r['has_relevant_data']}",
            f"- **Observed Restrictions:** {r['access_restrictions']}",
            f"- **Documented Limitations:** {r['limitations']}",
            f"- **Planned Extraction Action:** {r['next_action']}",
            ""
        ])
    save_text("\n".join(lines), report_path)

if __name__ == "__main__":
    run_source_audit()
