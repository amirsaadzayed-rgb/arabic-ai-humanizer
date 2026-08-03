from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# مفتاح الاتصال المباشر لضمان استقرار العمل على السيرفر
GROG_API_KEY = "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"

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>أداة إعادة صياغة النصوص العربية بأسلوب بشري</title>
        <style>
            :root {
                --primary: #4f46e5;
                --primary-hover: #4338ca;
                --bg-color: #f8fafc;
                --card-bg: #ffffff;
                --text-main: #1e293b;
                --border-color: #cbd5e1;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-main);
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: var(--card-bg);
                padding: 35px;
                border-radius: 16px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
                width: 100%;
                max-width: 750px;
            }
            h1 {
                color: var(--primary);
                text-align: center;
                margin-bottom: 25px;
                font-size: 26px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                font-weight: 600;
                display: block;
                margin-bottom: 8px;
            }
            textarea {
                width: 100%;
                height: 160px;
                padding: 14px;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
                box-sizing: border-box;
                transition: border-color 0.2s;
            }
            textarea:focus {
                border-color: var(--primary);
                outline: none;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            .stats {
                display: flex;
                justify-content: space-between;
                font-size: 13px;
                color: #64748b;
                margin-top: 5px;
                margin-bottom: 15px;
            }
            .btn-container {
                display: flex;
                gap: 10px;
            }
            button {
                background-color: var(--primary);
                color: white;
                border: none;
                padding: 14px 20px;
                font-size: 16px;
                font-weight: 600;
                border-radius: 10px;
                cursor: pointer;
                width: 100%;
                transition: background 0.2s, transform 0.1s;
            }
            button:hover {
                background-color: var(--primary-hover);
            }
            button:active {
                transform: scale(0.99);
            }
            .result-box {
                margin-top: 25px;
                background: #f1f5f9;
                padding: 20px;
                border-radius: 10px;
                border-right: 5px solid #10b981;
                display: none;
                position: relative;
            }
            .result-box h3 {
                margin-top: 0;
                color: #059669;
                font-size: 18px;
            }
            .copy-btn {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 13px;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 12px;
                width: auto;
                display: inline-block;
            }
            .copy-btn:hover {
                background-color: #059669;
            }
            .loading {
                text-align: center;
                color: #d97706;
                font-weight: 600;
                display: none;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✍️ أداة إعادة صياغة النصوص بأسلوب بشري</h1>
            <form id="humanizeForm">
                <div class="form-group">
                    <label for="text">الصق النص المكتوب بالذكاء الاصطناعي هنا:</label>
                    <textarea id="text" name="text" placeholder="اكتب أو الصق النص هنا..." oninput="updateStats()" required></textarea>
                    <div class="stats">
                        <span id="charCount">عدد الحروف: 0</span>
                        <span id="wordCount">عدد الكلمات: 0</span>
                    </div>
                </div>
                <div class="btn-container">
                    <button type="submit" id="submitBtn">إحداث صياغة بشرية طبيعية</button>
                </div>
            </form>
            
            <div id="loading" class="loading">⏳ جارٍ تحليل النص وإعادة صياغته ببراعة...</div>

            <div id="resultBox" class="result-box">
                <h3>النص المُعدّل (أسلوب طبيعي):</h3>
                <p id="resultText" style="white-space: pre-wrap; line-height: 1.7; margin-bottom: 10px;"></p>
                <button class="copy-btn" onclick="copyResult()">📋 نسخ النص الناتج</button>
            </div>
        </div>

        <script>
            function updateStats() {
                const text = document.getElementById('text').value;
                document.getElementById('charCount').innerText = 'عدد الحروف: ' + text.length;
                const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
                document.getElementById('wordCount').innerText = 'عدد الكلمات: ' + words;
            }

            document.getElementById('humanizeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const text = document.getElementById('text').value;
                const loading = document.getElementById('loading');
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');
                const submitBtn = document.getElementById('submitBtn');

                loading.style.display = 'block';
                resultBox.style.display = 'none';
                submitBtn.disabled = true;

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
                    submitBtn.disabled = false;

                    if (response.ok) {
                        resultText.innerText = data.result;
                        resultBox.style.display = 'block';
                    } else {
                        alert('حدث خطأ: ' + (data.detail || 'يرجى المحاولة لاحقاً'));
                    }
                } catch (err) {
                    loading.style.display = 'none';
                    submitBtn.disabled = false;
                    alert('خطأ في الاتصال بالخادم');
                }
            });

            function copyResult() {
                const textToCopy = document.getElementById('resultText').innerText;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    alert('تم نسخ النص بنجاح!');
                });
            }
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
    
    prompt = f"""قم بإعادة صياغة النص العربي التالي ليبدو تماماً كأنه مكتوب بواسطة كاتب بشري محترف وطبيعي، وتجنب تماماً التعبيرات النمطية أو الآلية، واجعله سلساً، جذاباً، ومترابطاً:

النص الأصلي:
{text}"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "أنت محرر وصحفي محترف خبير في صياغة المحتوى العربي بأسلوب بشري طبيعي وجذاب."},
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
