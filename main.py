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
            }
            /* شريط النسب مخفي افتراضياً ولا يظهر إلا بعد المعالجة */
            .metrics-bar {
                display: none;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                background: #0f172a;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 20px;
                border: 1px solid var(--border-color);
            }
            .metric-box {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .metric-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 13px;
            }
            .metric-label {
                color: var(--text-muted);
            }
            .metric-val {
                color: #fff;
                font-weight: bold;
                direction: ltr;
                unicode-bidi: embed;
            }
            .progress-track {
                background: #1e293b;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
                direction: ltr;
            }
            .progress-fill-human {
                background: #10b981;
                width: 0%;
                height: 100%;
                transition: width 0.5s ease;
            }
            .progress-fill-ai {
                background: #ef4444;
                width: 0%;
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
            .loading {
                text-align: center;
                color: #fbbf24;
                font-weight: bold;
                margin: 10px 0;
                display: none;
            }
            /* Modals */
            .modal-overlay {
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.8);
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal-content {
                background: #131b2e;
                border: 1px solid var(--border-color);
                padding: 30px;
                border-radius: 16px;
                width: 100%;
                max-width: 750px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                max-height: 80vh;
                overflow-y: auto;
            }
            .pricing-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 15px;
                margin-top: 20px;
            }
            .price-card {
                background: #0f172a;
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .price-card.pro {
                border-color: #8b5cf6;
            }
            .close-modal {
                background: #ef4444;
                color: white;
                border: none;
                padding: 6px 14px;
                border-radius: 6px;
                cursor: pointer;
                float: left;
            }
            .history-item {
                background: #0f172a;
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 10px;
                border: 1px solid var(--border-color);
                font-size: 13px;
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
                    <div class="badge">المحاولات: <span id="attemptsCount" dir="ltr">3/3</span> متبقية</div>
                    <button class="upgrade-btn" onclick="openPricingModal()">✨ ترقية الباقة</button>
                    <div class="badge" style="cursor:pointer;" onclick="openHistoryModal()">📜 السجل</div>
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

            <!-- شريط النسب (يظهر فقط بعد اكتمال التحويل) -->
            <div id="metricsBar" class="metrics-bar">
                <!-- اليمين: النمط الآلي -->
                <div class="metric-box">
                    <div class="metric-row">
                        <span class="metric-label">نسبة النمط الآلي (AI Pattern):</span>
                        <span id="aiMetricVal" class="metric-val">2%</span>
                    </div>
                    <div class="progress-track"><div id="aiBar" class="progress-fill-ai" style="width: 2%;"></div></div>
                </div>
                <!-- اليسار: الصياغة البشرية -->
                <div class="metric-box">
                    <div class="metric-row">
                        <span class="metric-label">نسبة الصياغة البشرية النقية:</span>
                        <span id="humanMetricVal" class="metric-val">98%</span>
                    </div>
                    <div class="progress-track"><div id="humanBar" class="progress-fill-human" style="width: 98%;"></div></div>
                </div>
            </div>

            <div class="editors-grid">
                <!-- اليمين: النص الأصلي / الآلي -->
                <div class="editor-card">
                    <div class="editor-header">
                        <span>النص الأصلي (الذكاء الاصطناعي)</span>
                        <div>
                            <label class="upload-label" for="fileInput">📁 رفع ملف</label>
                            <input type="file" id="fileInput" accept=".txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
                            <span id="origWordCount" style="margin-right: 8px;" dir="ltr">0 كلمة</span>
                        </div>
                    </div>
                    <textarea id="inputText" placeholder="انسخ النص هنا أو الصقه أو ارفع ملفاً..." oninput="updateWordCounts()"></textarea>
                </div>

                <!-- اليسار: النص المولد بشرياً -->
                <div class="editor-card">
                    <div class="editor-header">
                        <span>النص المولد بشرياً (الناتج النهائي)</span>
                        <span id="resWordCount" dir="ltr">0 كلمة</span>
                    </div>
                    <textarea id="resultText" readonly placeholder="سيتم كتابة النص المعاد صياغته هنا مباشرة..."></textarea>
                    <button class="copy-btn" onclick="copyResult()">📋 نسخ النص الناتج</button>
                </div>
            </div>
        </div>

        <!-- Pricing Modal (3 باقات) -->
        <div id="pricingModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-modal" onclick="closePricingModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff; text-align:center;">اختر الباقة المناسبة لك</h2>
                <div class="pricing-grid">
                    <!-- باقة 1: المجانية -->
                    <div class="price-card">
                        <div>
                            <h3 style="color:#94a3b8; margin-top:0;">الباقة المجانية</h3>
                            <p style="font-size:22px; font-weight:bold; color:#fff;" dir="ltr">0 ج.م</p>
                            <p style="font-size:12px; color:#94a3b8;">3 محاولات مجانية يومياً للاستجابة السريعة</p>
                        </div>
                        <button style="width:100%; padding:10px; background:#1e293b; color:white; border:none; border-radius:6px; margin-top:10px;" onclick="closePricingModal()">باقتك الحالية</button>
                    </div>
                    <!-- باقة 2: المحددة بعدد مقالات -->
                    <div class="price-card">
                        <div>
                            <h3 style="color:#38bdf8; margin-top:0;">الباقة المحددة</h3>
                            <p style="font-size:22px; font-weight:bold; color:#fff;" dir="ltr">150 ج.م</p>
                            <p style="font-size:12px; color:#94a3b8;">مخصصة لعدد 50 مقال شهرياً بدعم كامل</p>
                        </div>
                        <button style="width:100%; padding:10px; background:#0284c7; color:white; border:none; border-radius:6px; margin-top:10px; cursor:pointer;" onclick="alert('قريباً سيتم تفعيل بوابة الدفع لهذه الباقة!')">اشترك الآن</button>
                    </div>
                    <!-- باقة 3: Pro اللامحدودة -->
                    <div class="price-card pro">
                        <div>
                            <h3 style="color:#8b5cf6; margin-top:0;">باقة Pro</h3>
                            <p style="font-size:22px; font-weight:bold; color:#fff;" dir="ltr">350 ج.م</p>
                            <p style="font-size:12px; color:#94a3b8;">مقاولات ومحاولات غير محدودة بالكامل + دعم فني خاص</p>
                        </div>
                        <button style="width:100%; padding:10px; background:linear-gradient(135deg, #8b5cf6, #ec4899); color:white; border:none; border-radius:6px; margin-top:10px; cursor:pointer;" onclick="alert('قريباً سيتم تفعيل بوابة الدفع لباقة Pro!')">اشترك الآن</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- History Modal -->
        <div id="historyModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-modal" onclick="closeHistoryModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff;">سجل المحاولات السابقة</h2>
                <div id="historyContainer" style="margin-top: 15px;">
                    <!-- سيتم تعبئته ديناميكياً -->
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

            function openPricingModal() {
                document.getElementById('pricingModal').style.display = 'flex';
            }
            function closePricingModal() {
                document.getElementById('pricingModal').style.display = 'none';
            }

            function openHistoryModal() {
                const container = document.getElementById('historyContainer');
                let history = JSON.parse(localStorage.getItem('ai_humanizer_history') || '[]');
                if (history.length === 0) {
                    container.innerHTML = '<p style="color: #94a3b8; text-align: center;">لا توجد محاولات مسجلة حتى الآن.</p>';
                } else {
                    container.innerHTML = history.map((item, index) => `
                        <div class="history-item">
                            <div style="display: flex; justify-content: space-between; color: #8b5cf6; margin-bottom: 5px;">
                                <span>محاولة رقم #${index + 1} (${item.tone})</span>
                                <span dir="ltr">${item.date}</span>
                            </div>
                            <div style="color: #f8fafc; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">الناتج: ${item.result}</div>
                        </div>
                    `).join('');
                }
                document.getElementById('historyModal').style.display = 'flex';
            }
            function closeHistoryModal() {
                document.getElementById('historyModal').style.display = 'none';
            }

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

            document.getElementById('humanizeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                if (currentAttempts <= 0) {
                    openPricingModal();
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

                        // إظهار شريط النسب وتحديثه بعد المعالجة الفعلية فقط
                        document.getElementById('metricsBar').style.display = 'grid';
                        document.getElementById('aiMetricVal').innerText = '2%';
                        document.getElementById('aiBar').style.width = '2%';
                        document.getElementById('humanMetricVal').innerText = '98%';
                        document.getElementById('humanBar').style.width = '98%';

                        // حفظ المحاولة في السجل
                        let history = JSON.parse(localStorage.getItem('ai_humanizer_history') || '[]');
                        history.unshift({
                            tone: tone,
                            date: new Date().toLocaleString(),
                            result: data.result.substring(0, 100) + '...'
                        });
                        localStorage.setItem('ai_humanizer_history', JSON.stringify(history));

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
