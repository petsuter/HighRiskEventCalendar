import requests
from icalendar import Calendar

FEEDS = [
  "https://ics.fixtur.es/v2/home/fc-zurich.ics",
  "https://ics.fixtur.es/v2/home/grasshoppers.ics",
]

HIGH_RISK_KEYWORDS = [
  "Zurich",
  "Grasshoppers",
  "Basel",
  "St. Gallen",
  "Luzern",
  "BSC",
  "Sion",
]

def build_filtered_ics():
    out_cal = Calendar()
    out_cal.add('prodid', '-//High Risk Events//EN')
    out_cal.add('version', '2.0')
    out_cal.add('x-wr-calname', 'High Risk Events')
    seen_events = set()
    for url in FEEDS:
        try:
            res = requests.get(url, timeout=10)
            in_cal = Calendar.from_ical(res.text)
            for event in in_cal.walk('VEVENT'):
                uid = str(event.get('uid', ''))
                if uid in seen_events: continue
                summary = str(event.get('summary', ''))
                risk = sum((kw in summary) for kw in HIGH_RISK_KEYWORDS)
                if risk >= 2:
                    event['summary'] = 'Hooligan Risk'
                    event['description'] = summary
                    out_cal.add_component(event)
                    seen_events.add(uid)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    with open("high_risk_events.ics", "wb") as f:
        f.write(out_cal.to_ical())

if __name__ == "__main__":
    build_filtered_ics()
