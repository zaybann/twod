import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# ဒေတာယူမယ့် မူရင်း Link
HISTORY_URL = "https://livechannelmm.com/1883/2dhistory.html"

@app.route('/api/history')
def get_history():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        response = requests.get(HISTORY_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        history_data = []
        
        # <h4> (ရက်စွဲ) တစ်ခုချင်းစီကို အခြေခံပြီး ဒေတာဆွဲမယ်
        dates = soup.find_all('h4')
        
        for date_tag in dates:
            # ရက်စွဲကို ယူမယ်
            date_str = date_tag.get_text(strip=True)
            
            # ရက်စွဲရဲ့ အောက်က tile div ကို ယူမယ်
            tile = date_tag.find_next_sibling('div', class_='tile')
            
            if tile:
                rows = tile.find_all('div', class_='row')
                
                # ဒေတာတွေကို Index အလိုက် သေချာခွဲထုတ်မယ်
                # Row 1: Header (Skip)
                # Row 2: 2D & 3D
                twod_cols = rows[1].find_all('div')
                # Row 3: Modern
                modern_cols = rows[2].find_all('div')
                # Row 4: Internet
                internet_cols = rows[3].find_all('div')

                # JSON အတွက် Dictionary ပုံစံ စီမယ်
                day_entry = {
                    "date": date_str,
                    "morning": {
                        "twod": twod_cols[1].get_text(strip=True),
                        "three_digit": twod_cols[2].get_text(strip=True),
                        "modern": modern_cols[1].get_text(strip=True),
                        "internet": internet_cols[1].get_text(strip=True)
                    },
                    "evening": {
                        "twod": twod_cols[3].get_text(strip=True),
                        "three_digit": twod_cols[4].get_text(strip=True),
                        "modern": modern_cols[3].get_text(strip=True),
                        "internet": internet_cols[3].get_text(strip=True)
                    }
                }
                history_data.append(day_entry)

        # နောက်ဆုံးမှာ JSON အဖြစ် Output ထုတ်ပေးမယ်
        return jsonify({
            "status": "success",
            "count": len(history_data),
            "results": history_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
  
