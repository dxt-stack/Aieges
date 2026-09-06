"""
AEGIS Real Market & Competitor Research Engine
Performs live web audits, pricing extraction, SEO keyword density analysis, and competitor scans.
"""

import urllib.request
import urllib.parse
import json
import re
import socket
import ipaddress
from typing import Dict, Any, List
from bs4 import BeautifulSoup


class LiveResearchEngine:
    """
    Real web intelligence scanner for competitor analysis and market validation.
    """

    @staticmethod
    def audit_url(target_url: str) -> Dict[str, Any]:
        """
        Fetches live web page, extracts metadata, headings, pricing signals, and technical footprint.
        """
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url
        parsed = urllib.parse.urlparse(target_url)
        if parsed.username or parsed.password or not parsed.hostname:
            raise ValueError("Research targets must be public HTTP(S) URLs without embedded credentials")
        try:
            addresses = socket.getaddrinfo(parsed.hostname, parsed.port or 443, type=socket.SOCK_STREAM)
            if any(ipaddress.ip_address(item[4][0]).is_private or ipaddress.ip_address(item[4][0]).is_loopback or ipaddress.ip_address(item[4][0]).is_link_local for item in addresses):
                raise ValueError("Private, loopback, and link-local research targets are not allowed")
        except socket.gaierror as exc:
            raise ValueError(f"Unable to resolve research target: {exc}") from exc

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AEGIS-Market-Intelligence/1.0"
        }

        try:
            req = urllib.request.Request(target_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                html_content = response.read(2_000_000).decode('utf-8', errors='ignore')
                status_code = response.getcode()
        except Exception as e:
            return {
                "target_url": target_url,
                "status": "UNREACHABLE",
                "error": str(e),
                "insights": {
                    "vulnerability": "Target domain unreachable or blocking scrapers.",
                    "opportunity": "Opportunity to offer high-reliability, zero-downtime API alternative."
                }
            }

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. Title & Meta
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': re.compile(r'description', re.I)}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta_tag and meta_tag.get('content'):
            meta_desc = meta_tag['content'].strip()

        # 2. Extract Headings
        h1s = [h.get_text(strip=True) for h in soup.find_all('h1')[:3]]
        h2s = [h.get_text(strip=True) for h in soup.find_all('h2')[:5]]

        # 3. Detect Pricing Clues
        text = soup.get_text()
        pricing_matches = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?(?:/mo|/month|/yr|/year)?', text)
        unique_pricing = list(set(pricing_matches))[:6]

        # 4. Keyword Frequency
        words = re.findall(r'\b[a-zA-Z]{4,15}\b', text.lower())
        stopwords = {'this', 'that', 'with', 'from', 'your', 'have', 'more', 'about', 'will', 'their', 'what', 'which', 'there', 'when'}
        freq = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:8]

        return {
            "target_url": target_url,
            "status": "LIVE",
            "http_status": status_code,
            "title": title,
            "meta_description": meta_desc,
            "primary_headings": h1s,
            "subheadings": h2s,
            "detected_pricing_points": unique_pricing,
            "top_keyword_signals": [f"{k} ({v})" for k, v in top_keywords],
            "vulnerability_analysis": {
                "pricing_transparency": "High" if len(unique_pricing) > 0 else "Low (Hidden behind sales form)",
                "recommended_exploit": "Deploy self-serve transparent pricing tiers ($49/$149) to capture fast-moving SMB buyers." if not unique_pricing else "Compete on automated throughput and superior API latency."
            }
        }
