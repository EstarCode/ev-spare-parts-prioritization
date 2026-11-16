# Rate-Limited, Resilient HTTP Client Module.
import time
import requests
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse
from src.utils.logger import get_logger

logger = get_logger("http_client")

# Robust, respectful HTTP client for academic and market research data collection.
class HttpClient:
    
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 (Research Bot/Academic Internship Data Collector; Ethiopia EV Parts Study)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,am;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    def __init__(self, delay_seconds: float = 1.0, timeout: int = 25, max_retries: int = 3):
        self.delay_seconds = delay_seconds
        self.timeout = timeout
        self.max_retries = max_retries
        self.last_request_time: Dict[str, float] = {}
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    # Enforce polite inter-request delay per target domain.
    def _rate_limit(self, domain: str) -> None:
        now = time.time()
        last_time = self.last_request_time.get(domain, 0.0)
        elapsed = now - last_time
        if elapsed < self.delay_seconds:
            sleep_needed = self.delay_seconds - elapsed
            time.sleep(sleep_needed)
        self.last_request_time[domain] = time.time()

    # Execute GET request with retries and rate limiting. Returns (status_code, text_content, json_dict_or_none, error_message_or_none).
    def get(self, url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, verify_ssl: bool = True) -> Tuple[int, str, Optional[Dict[str, Any]], Optional[str]]:
        domain = urlparse(url).netloc
        self._rate_limit(domain)

        merged_headers = dict(self.DEFAULT_HEADERS)
        if headers:
            merged_headers.update(headers)

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(
                    url,
                    headers=merged_headers,
                    params=params,
                    timeout=self.timeout,
                    verify=verify_ssl,
                    allow_redirects=True
                )
                
                status_code = response.status_code
                text_content = response.text
                json_data = None
                
                if "application/json" in response.headers.get("Content-Type", "").lower():
                    try:
                        json_data = response.json()
                    except Exception:
                        pass
                else:
                    stripped = text_content.strip()
                    if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
                        try:
                            json_data = response.json()
                        except Exception:
                            pass

                return status_code, text_content, json_data, None

            except requests.exceptions.SSLError as ssl_err:
                logger.warning(f"SSL error connecting to {url} (attempt {attempt}/{self.max_retries}): {ssl_err}")
                if verify_ssl:
                    logger.info(f"Retrying {url} with SSL verification disabled...")
                    try:
                        return self.get(url, headers=headers, params=params, verify_ssl=False)
                    except Exception as retry_err:
                        last_error = str(retry_err)
                else:
                    last_error = str(ssl_err)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as conn_err:
                logger.warning(f"Connection/Timeout error connecting to {url} (attempt {attempt}/{self.max_retries}): {conn_err}")
                last_error = str(conn_err)
                time.sleep(attempt * 1.5)
            except Exception as e:
                logger.error(f"Unexpected error requesting {url}: {e}")
                last_error = str(e)
                break

        return 0, "", None, last_error
