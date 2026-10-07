document.addEventListener('DOMContentLoaded', () => {
    // Views
    const viewInitial = document.getElementById('view-initial');
    const viewResponse = document.getElementById('view-response');
    const viewChat = document.getElementById('view-chat');

    // View 1 Elements
    const initialInput = document.getElementById('initial-input');
    const initialSubmitBtn = document.getElementById('initial-submit-btn');

    // View 2 Elements
    const responseUserQuery = document.getElementById('response-user-query');
    const responseAiAnswer = document.querySelector('#response-ai-answer .text-content');
    const initialTyping = document.getElementById('initial-typing');
    const resolutionActionArea = document.getElementById('resolution-action-area');
    const followupBtn = document.getElementById('followup-btn');

    // View 3 Elements
    const chatHistory = document.getElementById('chat-history');
    const chatInput = document.getElementById('chat-input');
    const chatSubmitBtn = document.getElementById('chat-submit-btn');

    let currentQuery = '';

    // Switch Views
    function switchView(hideView, showView) {
        hideView.classList.remove('active');
        setTimeout(() => {
            hideView.classList.add('hidden');
            showView.classList.remove('hidden');
            // Small timeout to allow display:block to render before opacity transition
            setTimeout(() => {
                showView.classList.add('active');
            }, 50);
        }, 400); // Matches CSS transition speed
    }

    // Handle Initial Submit
    function handleInitialSubmit() {
        const query = initialInput.value.trim();
        if (!query) return;

        currentQuery = query;
        responseUserQuery.textContent = query;
        
        switchView(viewInitial, viewResponse);
        
        // Simulate AI Processing
        initialTyping.classList.remove('hidden');
        responseAiAnswer.innerHTML = '';
        
        setTimeout(() => {
            initialTyping.classList.add('hidden');
            
            // Dummy response text
            const responseHtml = `
                <p style="margin-bottom: 12px;">Based on your query regarding <strong>"${query}"</strong>, here is an initial analysis:</p>
                <ul style="margin-left: 20px; margin-bottom: 16px;">
                    <li style="margin-bottom: 8px;">The issue appears to be related to the recent configuration changes.</li>
                    <li style="margin-bottom: 8px;">Log analysis indicates a potential bottleneck in the database connection pool.</li>
                </ul>
                <p>I recommend checking the connection pool metrics or investigating the recent commits to the configuration repository.</p>
            `;
            
            responseAiAnswer.innerHTML = responseHtml;
            
            // Show action area after response finishes "typing"
            setTimeout(() => {
                resolutionActionArea.classList.remove('hidden');
            }, 800);
            
        }, 2000);
    }

    initialSubmitBtn.addEventListener('click', handleInitialSubmit);
    initialInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleInitialSubmit();
    });

    // Handle Followup Button Click
    followupBtn.addEventListener('click', () => {
        // Move the initial conversation to the chat history
        chatHistory.innerHTML = '';
        
        // Add User Message
        appendMessage('user', currentQuery);
        // Add AI Message
        appendMessage('ai', responseAiAnswer.innerHTML, false);
        
        // Switch to Chat View
        switchView(viewResponse, viewChat);
        
        setTimeout(() => {
            chatInput.focus();
        }, 500);
    });

    // Handle Continuous Chat
    function appendMessage(sender, text, isText = true) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        
        if (sender === 'ai') {
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.innerHTML = '<i class="ri-robot-2-line"></i>';
            
            const content = document.createElement('div');
            content.className = 'content';
            if (isText) {
                content.textContent = text;
            } else {
                content.innerHTML = text; // Handle HTML from the initial response
            }
            
            msgDiv.appendChild(avatar);
            msgDiv.appendChild(content);
        } else {
            msgDiv.textContent = text;
        }
        
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function handleChatSubmit() {
        const text = chatInput.value.trim();
        if (!text) return;
        
        appendMessage('user', text);
        chatInput.value = '';
        
        // Simulate AI thinking and responding
        setTimeout(() => {
            appendMessage('ai', "I'm looking into that for you. Let me query the system logs based on your new context...");
        }, 1000);
    }

    chatSubmitBtn.addEventListener('click', handleChatSubmit);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleChatSubmit();
    });
});
