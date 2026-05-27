document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('results');
    const jdInput = document.getElementById('jobDescription');
    const jobRoleSelect = document.getElementById('jobRole');
    const customRoleInput = document.getElementById('customRoleInput');

    let selectedFile = null;

    // Toggle custom role input
    jobRoleSelect.addEventListener('change', (e) => {
        if (e.target.value === 'other') {
            customRoleInput.classList.remove('hidden');
        } else {
            customRoleInput.classList.add('hidden');
        }
    });

    // Drag and Drop Logic
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file.name.match(/\.(pdf|docx)$/)) {
            alert('Please select a PDF or DOCX file.');
            return;
        }
        selectedFile = file;
        const dropZoneText = dropZone.querySelector('p');
        dropZoneText.textContent = `Selected: ${file.name}`;
        dropZoneText.style.color = '#8b5cf6';
    }

    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) {
            alert('Please upload a resume first.');
            return;
        }

        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const selectedRole = jobRoleSelect.value;
        formData.append('job_role', selectedRole);
        
        if (selectedRole === 'other' && customRoleInput.value.trim() !== '') {
            formData.append('custom_role', customRoleInput.value.trim());
        }

        if (jdInput.value.trim() !== '') {
            formData.append('job_description', jdInput.value.trim());
        }

        try {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error(error);
            alert('Error analyzing resume.');
        } finally {
            loader.classList.add('hidden');
        }
    });

    let currentAnalysisContext = null;

    function displayResults(data) {
        currentAnalysisContext = data;
        
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Update Score
        const scoreElement = document.getElementById('totalScore');
        animateValue(scoreElement, 0, data.overall_score, 1500);

        // Update Language Badge
        const langBadge = document.getElementById('langBadge');
        langBadge.textContent = data.language || 'English';

        // Update Progress Ring
        const circle = document.querySelector('.progress');
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (data.overall_score / 100) * circumference;
        circle.style.strokeDashoffset = offset;
        circle.style.stroke = data.overall_score > 70 ? '#10b981' : '#8b5cf6';

        // Save to History
        saveToHistory(data.overall_score, data.role_context);

        // Populate Lists
        populateList('strengthsList', data.feedback.strengths);
        populateList('weaknessesList', data.feedback.weaknesses);
        populateList('suggestionsList', data.feedback.suggestions);

        // Analytics: Missing Keywords
        const gapsContainer = document.getElementById('missingKeywords');
        gapsContainer.innerHTML = data.missing_keywords.map(kw => `<span class="tag">${kw}</span>`).join('');

        // Analytics: Formatting
        const formatContainer = document.getElementById('formattingReport');
        if (data.formatting_report.issues.length === 0) {
            formatContainer.innerHTML = '<p class="formatting-pass">✓ No formatting issues detected.</p>';
        } else {
            formatContainer.innerHTML = data.formatting_report.issues.map(issue => `<p class="formatting-issue">! ${issue}</p>`).join('');
        }

        renderScoreChart(data.section_scores);

        // Show chat button
        document.getElementById('chatToggleBtn').classList.remove('hidden');
    }

    // --- Chat Widget Logic ---
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    const chatWindow = document.getElementById('chatWindow');
    const chatCloseBtn = document.getElementById('chatCloseBtn');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');

    chatToggleBtn.addEventListener('click', () => {
        chatWindow.classList.toggle('hidden');
        chatToggleBtn.classList.toggle('hidden');
    });

    chatCloseBtn.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
        chatToggleBtn.classList.remove('hidden');
    });

    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });

    async function sendChatMessage() {
        const text = chatInput.value.trim();
        if (!text || !currentAnalysisContext) return;

        // Add user message
        addMessage(text, 'user');
        chatInput.value = '';

        // Show loading indicator in chat
        const loadingId = addMessage('...', 'ai');

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    context: currentAnalysisContext
                })
            });

            if (!response.ok) throw new Error('Chat failed');

            const data = await response.json();
            
            // Replace loading message with actual response
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.innerHTML = data.reply;
            } else {
                addMessage(data.reply, 'ai');
            }
        } catch (error) {
            console.error(error);
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) loadingMsg.innerHTML = "Sorry, I'm having trouble connecting right now.";
        }
    }

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message ${sender}`;
        msgDiv.innerHTML = text; // allow basic HTML like line breaks
        const id = 'msg-' + Date.now();
        msgDiv.id = id;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function saveToHistory(score, role) {
        const history = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
        history.unshift({ score, role, date: new Date().toLocaleDateString() });
        localStorage.setItem('resumeHistory', JSON.stringify(history.slice(0, 5)));
        renderHistory();
    }

    function renderHistory() {
        const historyList = document.getElementById('historyList');
        const history = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
        historyList.innerHTML = history.map(item => `
            <div class="history-item">
                <div>
                    <strong>${item.role.replace('_', ' ')}</strong>
                    <div style="font-size: 0.8rem; color: var(--text-muted)">${item.date}</div>
                </div>
                <div class="score-val">${item.score}%</div>
            </div>
        `).join('');
    }

    // Initial load
    renderHistory();

    function populateList(id, items) {
        const list = document.getElementById(id);
        list.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            list.appendChild(li);
        });
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    let myChart = null;
    function renderScoreChart(breakdown) {
        const ctx = document.getElementById('scoreChart').getContext('2d');
        
        if (myChart) myChart.destroy();

        myChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Skills', 'Experience', 'Projects', 'Education', 'Keywords'],
                datasets: [{
                    label: 'Resume Score Distribution',
                    data: [
                        breakdown.skills,
                        breakdown.experience,
                        breakdown.projects,
                        breakdown.education,
                        30 // Keywords/ATS Placeholder
                    ],
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    borderColor: '#8b5cf6',
                    pointBackgroundColor: '#8b5cf6',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 30,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { display: false }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
