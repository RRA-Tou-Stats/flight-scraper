import os
import sys
from datetime import datetime
from seleniumbase import Driver

def scrape_rodrigues_robust():
    base_url = "https://mauritius-airport.atol.aero/passengers/flights/flight-departure-search"
    print("Connecting to ATOL Departure portal via SeleniumBase...")
    
    cwd = os.getcwd()
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"flights_{today_str}.txt"
    filepath = os.path.join(cwd, filename)
    
    rodrigues_flights = set()
    max_pages = 3  # Scan pages 0 to 2
    
    # Initialize SeleniumBase Driver in Undetected & Headless mode to bypass Cloudflare
    driver = Driver(uc=True, headless=True)
    
    try:
        for page in range(max_pages):
            page_url = f"{base_url}?page={page}"
            print(f" -> Scanning page {page}: {page_url}")
            
            driver.get(page_url)
            
            # Brief pause to let Cloudflare clearance/JS finish rendering
            driver.sleep(3)
            
            html_content = driver.page_source
            
            if "Just a moment" in html_content or "Cloudflare" in html_content:
                print(f"    [BLOCKED] Cloudflare challenge active on page {page}.")
                continue

            # Simple string token check for Rodrigues and flight numbers
            # (Matches your original extraction pattern safely against page source)
            import re
            rows = re.split(r'</tr>|<tr[^>]*>', html_content, flags=re.IGNORECASE)
            
            for row in rows:
                if "Rodrigues" in row:
                    tokens = re.findall(r'\b([A-Z]{2}\d{3,4})\b', row)
                    if tokens:
                        has_mk = any(t.startswith("MK") for t in tokens)
                        for token in tokens:
                            if token.startswith("MK"):
                                rodrigues_flights.add(token)
                            elif not has_mk:
                                rodrigues_flights.add(token)

        # Sort the results cleanly
        sorted_flights = sorted(list(rodrigues_flights))
        
        # Write to disk for CSPro
        with open(filepath, "w", encoding="utf-8") as f:
            if sorted_flights:
                for flight in sorted_flights:
                    f.write(f"{flight}\n")
                print(f"\n[SUCCESS] Extracted {len(sorted_flights)} Rodrigues flight(s): {sorted_flights}")
            else:
                f.write("No matching Rodrigues flights found.\n")
                print("\n[NOTICE] No Rodrigues flights matched.")
                
        print(f"[SAVED] File successfully written to disk at:\n -> {filepath}")

    except Exception as err:
        print(f"\n[CRITICAL ERROR] {err}", file=sys.stderr)
        sys.exit(1)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_rodrigues_robust()
