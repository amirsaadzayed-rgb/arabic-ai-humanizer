from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# المفاتيح مباشرة لمنع أي خطأ على سيرفرات الاستضافة
GROG_API_KEY = "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"

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>أداة تحويل النصوص إلى أسلوب بشري</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 700px;
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 25px;
                font-size: 24px;
            }
            label {
                font-weight: bold;
                color: #34495e;
                display: block;
                margin-bottom: 8px;
            }
            textarea {
                width: 100%;
                height: 150px;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
                resize: vertical;
                box-sizing: border-box;
                margin-bottom: 15px;
            }
            textarea:focus {
                border-color: #3498db;
                outline: none;
            }
            button {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                transition: background 0.3s;
            }
            button:hover {
                background-color: #2980b9;
            }
            .result-box {
                margin-top: 25px;
                background: #ecf0f1;
                padding: 15px;
                border-radius: 8px;
                border-right: 5px solid #2ecc71;
                display: none;
            }
            .result-box h3 {
                margin-top: 0;
                color: #27ae60;
            }
            .loading {
                text-align: center;
                color: #e67e22;
                font-weight: bold;
                display: none;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✍️ أداة إعادة صياغة النصوص العربية بأسلوب بشري</h1>
            <form id="humanizeForm">
                <label for="text">الصق النص المكتوب بالذكاء الاصطناعي هنا:</label>
                <textarea id="text" name="text" placeholder="اكتب أو الصق النص هنا..." required></textarea>
                <button type="submit">إعادة صياغة النص (جعلها بشرية)</button>
            </form>
            
            <div id="loading" class="loading">⏳ جارٍ معالجة النص وإعادة صياغته بذكاء...</div>

            <div id="resultBox" class="result-box">
                <h3>النص بعد التعديل (أسلوب طبيعي):</h3>
                <p id="resultText" style="white-space: pre-wrap; line-height: 1.6;"></p>
            </div>
        </div>

        <script>
            document.getElementById('humanizeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const text = document.getElementById('text').value;
                const loading = document.getElementById('loading');
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');

                loading.style.display = 'block';
                resultBox.style.display = 'none';

                try {
                    const response = await fetch('/humanize', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: 'text=' + encodeURIComponent(text)
                    });

                    const data = await response.json();
                    loading.style.display = 'none';

                    if (response.ok) {
                        resultText.innerText = data.result;
                        resultBox.style.display = 'block';
                    } else {
                        alert('حدث خطأ: ' + (data.detail || 'يرجى المحاولة لاحقاً'));
                    }
                } catch (err) {
                    loading.style.display = 'none';
                    alert('خطأ في الاتصال بالخادم');
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/humanize")
async def humanize_text(text: str = Form(...)):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROG_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""قم بإعادة صياغة النص العربي التالي ليبدو كأنه مكتوب بواسطة كاتب بشري محترف وطبيعي تماماً، وتجنب تماماً التعبير الروبوتي أو المكرر الخاص بالذكاء الاصطناعي، واجعله سلساً ومترابطاً:

النص الأصلي:
{text}"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "أنت محرر وصحفي محترف متخصص في صياغة المقالات العربية بأسلوب بشري طبيعي وجذاب."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        if "choices" in res_data:
            output_text = res_data["choices"][0]["message"]["content"]
            return {"result": output_text}
        else:
            raise HTTPException(status_code=500, detail=str(res_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
