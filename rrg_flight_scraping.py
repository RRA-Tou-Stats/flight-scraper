import os
import re
import urllib.request
import urllib.error
from datetime import datetime

def scrape_rodrigues_robust():
    base_url = "https://mauritius-airport.atol.aero/passengers/flights/flight-departure-search"
    print("Connecting to ATOL Departure portal...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    cwd = os.getcwd()
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"flights_{today_str}.txt"
    filepath = os.path.join(cwd, filename)
    
    rodrigues_flights = set()
    max_pages = 3  # Scan pages 0 to 2
    
    try:
        for page in range(max_pages):
            page_url = f"{base_url}?page={page}"
            print(f" -> Scanning page {page}: {page_url}")
            
            req = urllib.request.Request(page_url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    html_content = response.read().decode("utf-8")
                    
                    if "Just a moment" in html_content or "Cloudflare" in html_content:
                        print(f"    [BLOCKED] Cloudflare challenge encountered on page {page}.")
                        continue

                    # Clean up HTML tags into a flat readable string/block structure
                    # Split chunks by table row indicators or table divisions
                    rows = re.split(r'</tr>|<tr[^>]*>', html_content, flags=re.IGNORECASE)
                    
                    for row in rows:
                        # Check if this specific row block mentions Rodrigues
                        if "Rodrigues" in row:
                            # Extract all flight designators within this specific flight entry row
                            tokens = re.findall(r'\b([A-Z]{2}\d{3,4})\b', row)
                            
                            if tokens:
                                # Check if an MK flight code exists in this row
                                has_mk = any(t.startswith("MK") for t in tokens)
                                
                                for token in tokens:
                                    if token.startswith("MK"):
                                        rodrigues_flights.add(token)
                                    elif not has_mk:
                                        # Keep non-MK codes only if no MK partner code is present
                                        rodrigues_flights.add(token)
                                        
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"    [INFO] Reached end of pagination at page {page}.")
                    break
                else:
                    print(f"    [HTTP ERROR {e.code}] Skipping page {page}.")

        # Sort the results cleanly
        sorted_flights = sorted(list(rodrigues_flights))
        
        # Write to disk for CSPro
        with open(filepath, "w", encoding="utf-8") as f:
            # f.write(f"Rodrigues Exclusive Departures - Date: {today_str}\n")
            # f.write("=" * 50 + "\n")
            if sorted_flights:
                for flight in sorted_flights:
                    f.write(f"{flight}\n")
                print(f"\n[SUCCESS] Extracted {len(sorted_flights)} Rodrigues flight(s): {sorted_flights}")
            else:
                f.write("No matching Rodrigues flights found.\n")
                print("\n[NOTICE] No Rodrigues flights matched.")
                
        print(f"[SAVED] File successfully written to disk at:\n -> {filepath}")

    except Exception as err:
        print(f"\n[CRITICAL ERROR] {err}")

if __name__ == "__main__":
    scrape_rodrigues_robust()