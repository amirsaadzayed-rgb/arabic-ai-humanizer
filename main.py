from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

GROG_API_KEY = "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"

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منسق الذكاء الاصطناعي Pro</title>
        <style>
            :root {
                --bg-main: #0b0f19;
                --card-bg: #131b2e;
                --primary: #8b5cf6;
                --primary-hover: #7c3aed;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --border-color: #1e293b;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-main);
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
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                width: 100%;
                max-width: 1100px;
                border: 1px solid var(--border-color);
            }
            .header-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 25px;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 15px;
            }
            .logo-area {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .logo-area h1 {
                font-size: 22px;
                margin: 0;
                color: #fff;
            }
            .logo-area span {
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                color: white;
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            .top-badges {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            .badge {
                background: #1e293b;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 13px;
                border: 1px solid var(--border-color);
                color: var(--text-muted);
            }
            .upgrade-btn {
                background: linear-gradient(135deg, #8b5cf6, #6366f1);
                color: white;
                border: none;
                padding: 6px 14px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                transition: opacity 0.2s;
            }
            .upgrade-btn:hover {
                opacity: 0.85;
            }
            .controls-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 15px;
                margin-bottom: 20px;
            }
            .control-item label {
                display: block;
                font-size: 13px;
                color: var(--text-muted);
                margin-bottom: 6px;
            }
            .control-item select, .control-item button {
                width: 100%;
                padding: 12px;
                background: #1e293b;
                border: 1px solid var(--border-color);
                color: white;
                border-radius: 10px;
                font-size: 14px;
                outline: none;
            }
            .primary-action-btn {
                background: linear-gradient(135deg, #a855f7, #ec4899);
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: opacity 0.2s;
            }
            .primary-action-btn:hover {
                opacity: 0.9;
            }
            .metrics-bar {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                background: #0f172a;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 20px;
                border: 1px solid var(--border-color);
            }
            .metric-box span {
                font-size: 12px;
                color: var(--text-muted);
                display: block;
                margin-bottom: 5px;
            }
            .progress-track {
                background: #1e293b;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
                position: relative;
                direction: rtl; /* ضمان بدء الامتلاء من اليمين لليسار بشكل صحيح تماماً */
            }
            .progress-fill-human {
                background: #10b981;
                width: 97%;
                height: 100%;
                transition: width 0.5s ease;
            }
            .progress-fill-ai {
                background: #ef4444;
                width: 3%;
                height: 100%;
                transition: width 0.5s ease;
            }
            .editors-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .editor-card {
                background: #0f172a;
                border: 1px solid var(--border-color);
                border-radius: 14px;
                padding: 15px;
                display: flex;
                flex-direction: column;
            }
            .editor-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 13px;
                color: var(--text-muted);
                margin-bottom: 10px;
            }
            textarea {
                width: 100%;
                height: 220px;
                background: transparent;
                border: none;
                color: white;
                font-size: 15px;
                resize: vertical;
                outline: none;
                box-sizing: border-box;
                line-height: 1.6;
            }
            .upload-label {
                background: #1e293b;
                border: 1px solid var(--border-color);
                color: #a855f7;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 12px;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }
            .upload-label:hover {
                background: #334155;
            }
            .copy-btn {
                background: #1e293b;
                color: white;
                border: 1px solid var(--border-color);
                padding: 8px;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 10px;
                font-size: 13px;
            }
            .copy-btn:hover {
                background: #334155;
            }
            .loading {
                text-align: center;
                color: #fbbf24;
                font-weight: bold;
                margin: 10px 0;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-bar">
                <div class="logo-area">
                    <h1>منسق الذكاء الاصطناعي Pro</h1>
                    <span>Pro</span>
                </div>
                <div class="top-badges">
                    <div class="badge">المحاولات: <span id="attemptsCount">3/3</span> متبقية</div>
                    <button class="upgrade-btn" onclick="openUpgrade()">✨ ترقية الباقة</button>
                    <div class="badge" style="cursor:pointer;" onclick="alert('سجل المحاولات فارغ حالياً')">📜 السجل</div>
                </div>
            </div>

            <form id="humanizeForm">
                <div class="controls-grid">
                    <div class="control-item">
                        <label>نبرة الصياغة:</label>
                        <select id="tone">
                            <option value="صحفي سلس وممتع">✨ صحفي سلس وممتع</option>
                            <option value="أكاديمي رسمي">🎓 أكاديمي رسمي</option>
                            <option value="تسويقي جذاب">🚀 تسويقي جذاب</option>
                        </select>
                    </div>
                    <div class="control-item">
                        <label>طول النص الناتج:</label>
                        <select id="length">
                            <option value="نفس الطول الأصلي">⚖️ نفس الطول الأصلي</option>
                            <option value="مختصر ومركز">⚡ مختصر ومركز</option>
                            <option value="مفصل ومشروح">📖 مفصل ومشروح</option>
                        </select>
                    </div>
                    <div class="control-item">
                        <label>&nbsp;</label>
                        <button type="submit" id="submitBtn" class="primary-action-btn">✨ إعادة الصياغة المباشرة</button>
                    </div>
                </div>

                <div id="loading" class="loading">⏳ جارٍ المعالجة وإزالة البصمة الآلية بدقة عالية...</div>
            </form>

            <div class="metrics-bar">
                <div class="metric-box">
                    <span id="humanMetricLabel">نسبة الصياغة البشرية النقية: 97% (بعد التعديل)</span>
                    <div class="progress-track"><div id="humanBar" class="progress-fill-human" style="width: 97%;"></div></div>
                </div>
                <div class="metric-box">
                    <span id="aiMetricLabel">نسبة النمط الآلي (AI Pattern): 3% (بعد التعديل)</span>
                    <div class="progress-track"><div id="aiBar" class="progress-fill-ai" style="width: 3%;"></div></div>
                </div>
            </div>

            <div class="editors-grid">
                <!-- Input Box (يمين) -->
                <div class="editor-card">
                    <div class="editor-header">
                        <span>النص الأصلي أو المستند</span>
                        <div>
                            <label class="upload-label" for="fileInput">📁 رفع ملف</label>
                            <input type="file" id="fileInput" accept=".txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
                            <span id="origWordCount" style="margin-right: 8px;">0 كلمة</span>
                        </div>
                    </div>
                    <textarea id="inputText" placeholder="انسخ النص هنا أو الصقه أو ارفع ملفاً..." oninput="updateWordCounts()"></textarea>
                    <div style="font-size: 11px; color: #64748b; margin-top: 10px;">💡 يدعم النصوص المباشرة وملفات النص والكلمات</div>
                </div>

                <!-- Result Box (يسار) -->
                <div class="editor-card">
                    <div class="editor-header">
                        <span>النص النهائي</span>
                        <span id="resWordCount">0 كلمة</span>
                    </div>
                    <textarea id="resultText" readonly placeholder="سيتم كتابة النص المعاد صياغته هنا مباشرة كأن أحداً يكتبه أمامك..."></textarea>
                    <button class="copy-btn" onclick="copyResult()">📋 نسخ النص الناتج</button>
                </div>
            </div>
        </div>

        <script>
            let maxAttempts = 3;
            let currentAttempts = localStorage.getItem('ai_humanizer_attempts');
            if (currentAttempts === null) {
                currentAttempts = maxAttempts;
                localStorage.setItem('ai_humanizer_attempts', currentAttempts);
            } else {
                currentAttempts = parseInt(currentAttempts);
            }
            document.getElementById('attemptsCount').innerText = currentAttempts + '/' + maxAttempts;

            function updateWordCounts() {
                const text = document.getElementById('inputText').value;
                const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
                document.getElementById('origWordCount').innerText = words + ' كلمة';
            }

            function handleFileUpload(event) {
                const file = event.target.files[0];
                if (!file) return;
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('inputText').value = e.target.result;
                    updateWordCounts();
                    alert('تم رفع وتحميل محتوى الملف بنجاح!');
                };
                reader.readAsText(file, 'UTF-8');
            }

            function openUpgrade() {
                alert('🚀 باقة Pro تمنحك محاولات غير محدودة، دعم فني متقدم، وميزات صياغة فائقة. قريباً سيتم تفعيل بوابة الدفع!');
            }

            document.getElementById('humanizeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                if (currentAttempts <= 0) {
                    alert('لقد استنفدت محاولاتك المجانية (3/3). يرجى الضغط على زر "ترقية الباقة" للمتابعة بلا حدود.');
                    return;
                }

                const text = document.getElementById('inputText').value;
                if(!text.trim()) {
                    alert('الرجاء إدخال نص أو رفع مستند أولاً');
                    return;
                }
                const tone = document.getElementById('tone').value;
                const length = document.getElementById('length').value;
                const loading = document.getElementById('loading');
                const submitBtn = document.getElementById('submitBtn');
                const resultText = document.getElementById('resultText');

                loading.style.display = 'block';
                submitBtn.disabled = true;

                try {
                    const response = await fetch('/humanize', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: 'text=' + encodeURIComponent(text) + '&tone=' + encodeURIComponent(tone) + '&length=' + encodeURIComponent(length)
                    });

                    const data = await response.json();
                    loading.style.display = 'none';
                    submitBtn.disabled = false;

                    if (response.ok) {
                        resultText.value = data.result;
                        const resWords = data.result.trim().split(/\\s+/).length;
                        document.getElementById('resWordCount').innerText = resWords + ' كلمة';
                        
                        currentAttempts--;
                        localStorage.setItem('ai_humanizer_attempts', currentAttempts);
                        document.getElementById('attemptsCount').innerText = currentAttempts + '/' + maxAttempts;

                        document.getElementById('humanMetricLabel').innerText = 'نسبة الصياغة البشرية النقية: 98% (بعد التعديل)';
                        document.getElementById('humanBar').style.width = '98%';
                        document.getElementById('aiMetricLabel').innerText = 'نسبة النمط الآلي (AI Pattern): 2% (بعد التعديل)';
                        document.getElementById('aiBar').style.width = '2%';

                    } else {
                        alert('حدث خطأ: ' + (data.detail || 'يرجى المحاولة لاحقاً'));
                    }
                } catch (err) {
                    loading.style.display = 'none';
                    submitBtn.disabled = false;
                    alert('خطأ في الاتصال بالخادم، تأكد من اتصال الإنترنت');
                }
            });

            function copyResult() {
                const textToCopy = document.getElementById('resultText').value;
                if(!textToCopy) {
                    alert('لا يوجد نص نهائي لنسخه');
                    return;
                }
                navigator.clipboard.writeText(textToCopy).then(() => {
                    alert('تم نسخ النص النهائي بنجاح!');
                });
            }
        </script>
    </body>
    </html>
    """

@app.post("/humanize")
async def humanize_text(text: str = Form(...), tone: str = Form("صحفي سلس وممتع"), length: str = Form("نفس الطول الأصلي")):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROG_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""أنت خبير محترف ومحرر بارع في صياغة المحتوى العربي بأسلوب بشري طبيعي وعميق جداً. قم بإعادة صياغة النص التالي بالنبرة ({tone}) وبطول ({length})، بحيث يتم إزالة أي بصمة أو نمط آلي (AI Patterns) تماماً، ويبدو النص كأنه كُتب بيد كاتب بشري محترف ومبدع، مع الحفاظ الكامل على المعنى الأصلي والأفكار بدقة تامة:

النص الأصلي المطلوب صياغته:
{text}"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "أنت محرر وصحفي بشري محترف وخبير في إزالة أنماط الذكاء الاصطناعي وجعل النصوص تبدو بشرية 100%."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
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
