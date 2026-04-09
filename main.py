from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "2D History API is running! Go to /api/history to see data."

@app.route('/api/history')
def get_history():
    try:
        url = "https://livechannelmm.com/1883/2dhistory.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        history_list = []
        
        # h4 (ရက်စွဲ) တွေကို လိုက်ရှာမယ်
        for date_tag in soup.find_all('h4'):
            date_text = date_tag.get_text(strip=True)
            tile = date_tag.find_next_sibling('div', class_='tile')
            
            if tile:
                rows = tile.find_all('div', class_='row')
                
                # ဒေတာရှိတဲ့ Row တွေကို စစ်ဆေးမယ် (အနည်းဆုံး row ၃ ခုရှိမှ ယူမယ်)
                if len(rows) >= 4:
                    twod_cols = rows[1].find_all('div')
                    modern_cols = rows[2].find_all('div')
                    internet_cols = rows[3].find_all('div')

                    # Python Dictionary ထဲ အစီအစဉ်တကျ ထည့်မယ်
                    day_data = {
                        "date": date_text,
                        "morning": {
                            "twod": twod_cols[1].get_text(strip=True) if len(twod_cols) > 1 else "",
                            "three_digit": twod_cols[2].get_text(strip=True) if len(twod_cols) > 2 else "",
                            "modern": modern_cols[1].get_text(strip=True) if len(modern_cols) > 1 else "",
                            "internet": internet_cols[1].get_text(strip=True) if len(internet_cols) > 1 else ""
                        },
                        "evening": {
                            "twod": twod_cols[3].get_text(strip=True) if len(twod_cols) > 3 else "",
                            "three_digit": twod_cols[4].get_text(strip=True) if len(twod_cols) > 4 else "",
                            "modern": modern_cols[3].get_text(strip=True) if len(modern_cols) > 3 else "",
                            "internet": internet_cols[3].get_text(strip=True) if len(internet_cols) > 3 else ""
                        }
                    }
                    history_list.append(day_data)

        # JSON အဖြစ် ပြန်ထုတ်ပေးမယ်
        return jsonify({
            "success": True,
            "data": history_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

