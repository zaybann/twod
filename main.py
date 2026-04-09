from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Lucky Boss 556 API is running! Go to /api/history to see data."

@app.route('/api/history')
def get_history():
    try:
        url = "https://livechannelmm.com/1883/2dhistory.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        history_list = []
        
        # သင့်ရဲ့ မူရင်း Logic ကို ဒီမှာ သုံးထားပါတယ်
        for date_tag in soup.find_all('h4'):
            date = date_tag.get_text(strip=True)
            tile = date_tag.find_next_sibling('div', class_='tile')
            
            if tile:
                rows = tile.find_all('div', class_='row')
                
                # ဒေတာရှိတဲ့ row တွေ ရှိမရှိ စစ်မယ်
                if len(rows) >= 4:
                    twod_row = rows[1].find_all('div')
                    modern_row = rows[2].find_all('div')
                    internet_row = rows[3].find_all('div')

                    # ယူချင်တဲ့ ဒေတာတွေကို Dictionary ထဲ ထည့်မယ်
                    day_data = {
                        "date": date,
                        "morning": {
                            "twod": twod_row[1].get_text(strip=True),
                            "three_digit": twod_row[2].get_text(strip=True),
                            "modern": modern_row[1].get_text(strip=True),
                            "internet": internet_row[1].get_text(strip=True)
                        },
                        "evening": {
                            "twod": twod_row[3].get_text(strip=True),
                            "three_digit": twod_row[4].get_text(strip=True),
                            "modern": modern_row[3].get_text(strip=True),
                            "internet": internet_row[3].get_text(strip=True)
                        }
                    }
                    history_list.append(day_data)

        # နောက်ဆုံးမှာ JSON format နဲ့ return ပြန်ပေးရပါတယ်
        return jsonify({
            "success": True,
            "data": history_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()

