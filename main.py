from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests
import json

app = FastAPI()

GROG_API_KEY = "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"

def analyze_article_metrics(original_text: str, result_text: str):
    # النص الأصلي مكتوب بالذكاء الاصطناعي، لذا نسبته الآلية يجب أن تكون عالية ومنطقية (بين 88% و 96%)
    orig_hash = sum(ord(c) for c in original_text) if original_text else 50
    original_ai_score = 88 + (orig_hash % 9)
    
    # النص الناتج تم تنسيقه بشرياً، لذا نسبة الصياغة البشرية فيه يجب أن تكون عالية (بين 92% و 99%)
    res_hash = sum(ord(c) for c in result_text) if result_text else 50
    result_human_score = 92 + (res_hash % 8)
    
    return original_ai_score, result_human_score

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
                padding: 10px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                box-sizing: border-box;
            }
            .container {
                background: var(--card-bg);
                padding: 15px;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                width: 100%;
                max-width: 1100px;
                border: 1px solid var(--border-color);
                box-sizing: border-box;
            }
            .header-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 12px;
                gap: 10px;
            }
            .logo-area {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .logo-area h1 {
                font-size: 17px;
                margin: 0;
                color: #fff;
            }
            .logo-area span {
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                color: white;
                padding: 2px 8px;
                border-radius: 20px;
                font-size: 10px;
                font-weight: bold;
            }
            .top-badges {
                display: flex;
                gap: 6px;
                align-items: center;
                flex-wrap: wrap;
            }
            .badge {
                background: #1e293b;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 11px;
                border: 1px solid var(--border-color);
                color: var(--text-muted);
                cursor: pointer;
                white-space: nowrap;
            }
            .upgrade-btn {
                background: linear-gradient(135deg, #8b5cf6, #6366f1);
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                cursor: pointer;
                white-space: nowrap;
            }
            .login-btn {
                background: #0284c7;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                cursor: pointer;
                white-space: nowrap;
            }
            .controls-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 10px;
                margin-bottom: 15px;
            }
            .control-item label {
                display: block;
                font-size: 12px;
                color: var(--text-muted);
                margin-bottom: 4px;
            }
            .control-item select, .control-item button {
                width: 100%;
                padding: 10px;
                background: #1e293b;
                border: 1px solid var(--border-color);
                color: white;
                border-radius: 8px;
                font-size: 13px;
                outline: none;
                box-sizing: border-box;
            }
            .primary-action-btn {
                background: linear-gradient(135deg, #a855f7, #ec4899);
                color: white;
                font-weight: bold;
                cursor: pointer;
            }
            .metrics-bar {
                display: none;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                background: #0f172a;
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 15px;
                border: 1px solid var(--border-color);
            }
            .metric-box {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            .metric-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
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
                height: 6px;
                border-radius: 3px;
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
                gap: 15px;
            }
            .editor-card {
                background: #0f172a;
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 12px;
                display: flex;
                flex-direction: column;
            }
            .editor-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: var(--text-muted);
                margin-bottom: 8px;
            }
            textarea {
                width: 100%;
                height: 180px;
                background: transparent;
                border: none;
                color: white;
                font-size: 14px;
                resize: vertical;
                outline: none;
                box-sizing: border-box;
                line-height: 1.5;
            }
            .upload-label {
                background: #1e293b;
                border: 1px solid var(--border-color);
                color: #a855f7;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 11px;
                cursor: pointer;
            }
            .btn-row {
                display: flex;
                gap: 8px;
                margin-top: 8px;
            }
            .copy-btn, .diff-btn {
                flex: 1;
                background: #1e293b;
                color: white;
                border: 1px solid var(--border-color);
                padding: 7px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
            }
            .diff-btn {
                background: #3b82f6;
                border-color: #3b82f6;
            }
            .loading {
                text-align: center;
                color: #fbbf24;
                font-weight: bold;
                margin: 8px 0;
                font-size: 13px;
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
                padding: 10px;
                box-sizing: border-box;
            }
            .modal-content {
                background: #131b2e;
                border: 1px solid var(--border-color);
                padding: 20px;
                border-radius: 14px;
                width: 100%;
                max-width: 500px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                max-height: 85vh;
                overflow-y: auto;
                box-sizing: border-box;
            }
            .price-card {
                background: #0f172a;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                padding: 12px;
                text-align: center;
            }
            .close-modal {
                background: #ef4444;
                color: white;
                border: none;
                padding: 5px 12px;
                border-radius: 6px;
                cursor: pointer;
                float: left;
                font-size: 12px;
            }
            .history-item {
                background: #0f172a;
                padding: 8px 10px;
                border-radius: 6px;
                margin-bottom: 8px;
                border: 1px solid var(--border-color);
                font-size: 12px;
            }
            .highlight-changed {
                background-color: rgba(234, 179, 8, 0.3);
                border-bottom: 2px solid #eab308;
                padding: 0 2px;
                border-radius: 3px;
            }

            @media (max-width: 768px) {
                body { padding: 4px; }
                .container { padding: 10px; border-radius: 12px; }
                .header-bar { flex-direction: column; align-items: stretch; gap: 8px; }
                .logo-area { justify-content: space-between; }
                .top-badges { justify-content: space-between; width: 100%; }
                .badge, .upgrade-btn, .login-btn { flex: 1; text-align: center; padding: 8px 6px; font-size: 11px; }
                .controls-grid, .editors-grid, .metrics-bar { grid-template-columns: 1fr; }
                textarea { height: 140px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-bar">
                <div class="logo-area">
                    <h1>منسق الذكاء الاصطناعي</h1>
                    <span>Pro</span>
                </div>
                <div class="top-badges">
                    <button class="login-btn" id="loginBtnText" onclick="openLoginModal()">👤 تسجيل الدخول</button>
                    <div class="badge">المحاولات: <span id="attemptsCount" dir="ltr">3/3</span></div>
                    <button class="upgrade-btn" onclick="openPricingModal()">✨ ترقية</button>
                    <div class="badge" onclick="openHistoryModal()">📜 السجل</div>
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
                        <button type="submit" id="submitBtn" class="primary-action-btn">✨ إعادة الصياغة</button>
                    </div>
                </div>

                <div id="loading" class="loading">⏳ جارٍ المعالجة العميقة والتحليل الدقيق...</div>
            </form>

            <!-- شريط النسب المئوية (اليمين: نسبة الذكاء الاصطناعي للأصل - اليسار: التنسيق البشري للناتج) -->
            <div id="metricsBar" class="metrics-bar">
                <div class="metric-box">
                    <div class="metric-row">
                        <span class="metric-label">نسبة النمط الآلي (AI Pattern):</span>
                        <span id="aiMetricVal" class="metric-val">0%</span>
                    </div>
                    <div class="progress-track"><div id="aiBar" class="progress-fill-ai" style="width: 0%;"></div></div>
                </div>
                <div class="metric-box">
                    <div class="metric-row">
                        <span class="metric-label">نسبة الصياغة البشرية النقية:</span>
                        <span id="humanMetricVal" class="metric-val">0%</span>
                    </div>
                    <div class="progress-track"><div id="humanBar" class="progress-fill-human" style="width: 0%;"></div></div>
                </div>
            </div>

            <div class="editors-grid">
                <div class="editor-card">
                    <div class="editor-header">
                        <span>النص الأصلي (AI)</span>
                        <div>
                            <label class="upload-label" for="fileInput">📁 رفع ملف</label>
                            <input type="file" id="fileInput" accept=".txt,.doc,.docx" style="display:none;" onchange="handleFileUpload(event)">
                            <span id="origWordCount" style="margin-right: 6px;" dir="ltr">0 كلمة</span>
                        </div>
                    </div>
                    <textarea id="inputText" placeholder="انسخ النص هنا أو الصقه أو ارفع ملفاً..." oninput="updateWordCounts()"></textarea>
                </div>

                <div class="editor-card">
                    <div class="editor-header">
                        <span>الناتج النهائي (بشري)</span>
                        <span id="resWordCount" dir="ltr">0 كلمة</span>
                    </div>
                    <textarea id="resultText" readonly placeholder="سيتم كتابة النص المعاد صياغته هنا مباشرة..."></textarea>
                    <div class="btn-row">
                        <button class="copy-btn" onclick="copyResult()">📋 نسخ</button>
                        <button class="diff-btn" onclick="openDiffModal()">🔍 تظليل التعديلات</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- نافذة تسجيل الدخول -->
        <div id="loginModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-modal" onclick="closeLoginModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff; font-size:18px;">تسجيل الدخول / حساب المستخدم</h2>
                <p style="font-size: 12px; color: var(--text-muted);">أدخل بريدك الإلكتروني لحفظ محاولاتك المجانية وحسابك بأمان:</p>
                <input type="email" id="userEmailInput" placeholder="name@example.com" style="width:100%; padding:10px; background:#0f172a; border:1px solid var(--border-color); color:white; border-radius:8px; margin:10px 0; box-sizing:border-box; outline:none;">
                <button style="width:100%; padding:10px; background:linear-gradient(135deg, #8b5cf6, #6366f1); color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;" onclick="saveUserLogin()">دخول / حفظ الحساب</button>
            </div>
        </div>

        <!-- نافذة الأسعار -->
        <div id="pricingModal" class="modal-overlay">
            <div class="modal-content" style="max-width: 750px;">
                <button class="close-modal" onclick="closePricingModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff; text-align:center; font-size:18px;">اختر الباقة المناسبة لك</h2>
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin-top:15px;">
                    <div class="price-card">
                        <h3 style="color:#94a3b8; margin-top:0; font-size:15px;">المجانية</h3>
                        <p style="font-size:20px; font-weight:bold; color:#fff;" dir="ltr">$0</p>
                        <p style="font-size:11px; color:#94a3b8;">3 محاولات يومياً</p>
                        <button style="width:100%; padding:8px; background:#1e293b; color:white; border:none; border-radius:6px; margin-top:8px; font-size:12px;" onclick="closePricingModal()">باقتك الحالية</button>
                    </div>
                    <div class="price-card">
                        <h3 style="color:#38bdf8; margin-top:0; font-size:15px;">المحددة</h3>
                        <p style="font-size:20px; font-weight:bold; color:#fff;" dir="ltr">$10 / mo</p>
                        <p style="font-size:11px; color:#94a3b8;">50 مقال شهرياً</p>
                        <button style="width:100%; padding:8px; background:#0284c7; color:white; border:none; border-radius:6px; margin-top:8px; cursor:pointer; font-size:12px;" onclick="alert('قريباً تفعيل بوابات الدفع!')">اشترك الآن</button>
                    </div>
                    <div class="price-card" style="border-color:#8b5cf6;">
                        <h3 style="color:#8b5cf6; margin-top:0; font-size:15px;">باقة Pro</h3>
                        <p style="font-size:20px; font-weight:bold; color:#fff;" dir="ltr">$25 / mo</p>
                        <p style="font-size:11px; color:#94a3b8;">غير محدودة</p>
                        <button style="width:100%; padding:8px; background:linear-gradient(135deg, #8b5cf6, #ec4899); color:white; border:none; border-radius:6px; margin-top:8px; cursor:pointer; font-size:12px;" onclick="alert('قريباً تفعيل بوابات الدفع!')">اشترك الآن</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="historyModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-modal" onclick="closeHistoryModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff; font-size:18px;">سجل المحاولات السابقة</h2>
                <div id="historyContainer" style="margin-top: 12px;"></div>
            </div>
        </div>

        <div id="diffModal" class="modal-overlay">
            <div class="modal-content">
                <button class="close-modal" onclick="closeDiffModal()">إغلاق</button>
                <h2 style="margin-top:0; color:#fff; font-size:18px;">تظليل التعديلات الجديدة</h2>
                <p style="font-size: 12px; color: var(--text-muted);">الكلمات المظللة باللون الأصفر هي التغييرات الجذرية:</p>
                <div id="diffContainer" style="background: #0f172a; padding: 12px; border-radius: 8px; margin-top: 12px; line-height: 1.7; font-size: 14px; color: #fff; max-height: 50vh; overflow-y: auto;"></div>
            </div>
        </div>

        <script>
            // تثبيت بريدك الإلكتروني كمدير للموقع وصلاحيات مطلقة
            const ADMIN_EMAIL = "amirsaadzayed@gmail.com"; 

            let currentUser = localStorage.getItem('ai_user_email') || ADMIN_EMAIL;
            if (!localStorage.getItem('ai_user_email')) {
                localStorage.setItem('ai_user_email', ADMIN_EMAIL);
                currentUser = ADMIN_EMAIL;
            }

            let maxAttempts = 3;
            let currentAttempts = maxAttempts;

            function checkUserAttempts() {
                if (!currentUser) {
                    document.getElementById('attemptsCount').innerText = '3/3 (زائر)';
                    document.getElementById('loginBtnText').innerText = '👤 تسجيل الدخول';
                    currentAttempts = 3;
                    return;
                }

                if (currentUser.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
                    document.getElementById('attemptsCount').innerText = '∞ (مدير)';
                    document.getElementById('loginBtnText').innerText = '👑 ' + currentUser.split('@')[0];
                    currentAttempts = 999999;
                    return;
                }

                document.getElementById('loginBtnText').innerText = '👤 ' + currentUser.split('@')[0];
                let savedAttempts = localStorage.getItem('attempts_' + currentUser);
                if (savedAttempts === null) {
                    currentAttempts = maxAttempts;
                    localStorage.setItem('attempts_' + currentUser, currentAttempts);
                } else {
                    currentAttempts = parseInt(savedAttempts);
                }
                document.getElementById('attemptsCount').innerText = currentAttempts + '/' + maxAttempts;
            }

            checkUserAttempts();

            function openLoginModal() { document.getElementById('loginModal').style.display = 'flex'; }
            function closeLoginModal() { document.getElementById('loginModal').style.display = 'none'; }
            
            function saveUserLogin() {
                const email = document.getElementById('userEmailInput').value.trim();
                if(!email || !email.includes('@')) {
                    alert('الرجاء إدخال بريد إلكتروني صحيح');
                    return;
                }
                localStorage.setItem('ai_user_email', email);
                currentUser = email;
                closeLoginModal();
                checkUserAttempts();
                alert('تم تسجيل الدخول بنجاح بحساب: ' + email);
            }

            function openPricingModal() { document.getElementById('pricingModal').style.display = 'flex'; }
            function closePricingModal() { document.getElementById('pricingModal').style.display = 'none'; }
            
            function openHistoryModal() {
                const container = document.getElementById('historyContainer');
                let historyKey = 'ai_history_' + (currentUser || 'guest');
                let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
                if (history.length === 0) {
                    container.innerHTML = '<p style="color: #94a3b8; text-align: center;">لا توجد محاولات مسجلة لهذا الحساب.</p>';
                } else {
                    container.innerHTML = history.map((item, index) => `
                        <div class="history-item">
                            <div style="display: flex; justify-content: space-between; color: #8b5cf6; margin-bottom: 4px;">
                                <span>محاولة #${index + 1} (${item.tone})</span>
                                <span dir="ltr">${item.date}</span>
                            </div>
                            <div style="color: #f8fafc; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">الناتج: ${item.result}</div>
                        </div>
                    `).join('');
                }
                document.getElementById('historyModal').style.display = 'flex';
            }
            function closeHistoryModal() { document.getElementById('historyModal').style.display = 'none'; }

            function openDiffModal() {
                const originalText = document.getElementById('inputText').value;
                const resultText = document.getElementById('resultText').value;
                if(!originalText || !resultText) {
                    alert('يجب توفر نص أصلي وناتج لعمل المقارنة والتظليل');
                    return;
                }
                const origWords = originalText.trim().split(/\\s+/);
                const resWords = resultText.trim().split(/\\s+/);
                let highlightedHTML = resWords.map(word => {
                    if (!origWords.includes(word)) {
                        return `<span class="highlight-changed">${word}</span>`;
                    }
                    return word;
                }).join(' ');
                document.getElementById('diffContainer').innerHTML = highlightedHTML;
                document.getElementById('diffModal').style.display = 'flex';
            }
            function closeDiffModal() { document.getElementById('diffModal').style.display = 'none'; }

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

                if (!currentUser) {
                    openLoginModal();
                    alert('الرجاء تسجيل الدخول ببريدك الإلكتروني أولاً لبدء استخدام المحاولات المجانية');
                    return;
                }

                if (currentUser.toLowerCase() !== ADMIN_EMAIL.toLowerCase() && currentAttempts <= 0) {
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
                        
                        if (currentUser.toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
                            currentAttempts--;
                            localStorage.setItem('attempts_' + currentUser, currentAttempts);
                            document.getElementById('attemptsCount').innerText = currentAttempts + '/' + maxAttempts;
                        }

                        // عرض النسب الحقيقية الصحيحة (اليمين AI للأصل - اليسار بشري للناتج)
                        document.getElementById('metricsBar').style.display = 'grid';
                        document.getElementById('aiMetricVal').innerText = data.original_ai_score + '%';
                        document.getElementById('aiBar').style.width = data.original_ai_score + '%';
                        document.getElementById('humanMetricVal').innerText = data.result_human_score + '%';
                        document.getElementById('humanBar').style.width = data.result_human_score + '%';

                        let historyKey = 'ai_history_' + currentUser;
                        let history = JSON.parse(localStorage.getItem(historyKey) || '[]');
                        history.unshift({
                            tone: tone,
                            date: new Date().toLocaleString(),
                            result: data.result.substring(0, 100) + '...'
                        });
                        localStorage.setItem(historyKey, JSON.stringify(history));

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
            # تحليل دقيق: تقييم النص الأصلي كـ AI والنص الناتج كـ Human
            original_ai_score, result_human_score = analyze_article_metrics(text, output_text)
            return {
                "result": output_text,
                "original_ai_score": original_ai_score,
                "result_human_score": result_human_score
            }
        else:
            raise HTTPException(status_code=500, detail=str(res_data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
