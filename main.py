from flask import Flask, jsonify
from flask_cors import CORS  # Website ချိတ်ဆက်ဖို့အတွက်
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # CORS ခွင့်ပြုချက်ပေးခြင်း

@app.route('/')
def home():
    return "Lucky Boss 556 - 2D History API is running! Use /api/history"

@app.route('/api/history')
def get_history():
    try:
        url = "https://livechannelmm.com/1883/2dhistory.html"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        history_list = []
        
        # h4 တဂ် (ရက်စွဲ) တွေကို လိုက်ရှာမယ်
        for date_tag in soup.find_all('h4'):
            date = date_tag.get_text(strip=True)
            tile = date_tag.find_next_sibling('div', class_='tile')
            
            if tile:
                rows = tile.find_all('div', class_='row')
                
                # အနည်းဆုံး row ၄ ခု ရှိမရှိ စစ်မယ် (Header, 2D, Modern, Internet)
                if len(rows) >= 4:
                    twod_cols = rows[1].find_all('div')
                    modern_cols = rows[2].find_all('div')
                    internet_cols = rows[3].find_all('div')

                    # Column အရေအတွက် ပြည့်စုံမှ ဒေတာယူမယ် (Error ကာကွယ်ရန်)
                    day_data = {
                        "date": date,
                        "morning": {
                            "twod": twod_cols[1].get_text(strip=True) if len(twod_cols) > 1 else "--",
                            "three_digit": twod_cols[2].get_text(strip=True) if len(twod_cols) > 2 else "--",
                            "modern": modern_cols[1].get_text(strip=True) if len(modern_cols) > 1 else "--",
                            "internet": internet_cols[1].get_text(strip=True) if len(internet_cols) > 1 else "--"
                        },
                        "evening": {
                            "twod": twod_cols[3].get_text(strip=True) if len(twod_cols) > 3 else "--",
                            "three_digit": twod_cols[4].get_text(strip=True) if len(twod_cols) > 4 else "--",
                            "modern": modern_cols[3].get_text(strip=True) if len(modern_cols) > 3 else "--",
                            "internet": internet_cols[3].get_text(strip=True) if len(internet_cols) > 3 else "--"
                        }
                    }
                    history_list.append(day_data)

        return jsonify({
            "success": True,
            "data": history_list
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
    
