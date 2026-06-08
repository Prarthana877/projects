const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const suggestionButtons = document.querySelectorAll('.suggestion-button');

const API_ENDPOINT = 'http://localhost:3000/api/chat';

suggestionButtons.forEach(button => {
    button.addEventListener('click', () => {
        userInput.value = button.textContent;
        if (typeof chatForm.requestSubmit === 'function') {
            chatForm.requestSubmit();
        } else {
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
    });
});

chatForm.addEventListener('submit', async event => {
    event.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user-message');
    userInput.value = '';
    userInput.disabled = true;
    appendLoadingMessage();

    try {
        const responseText = await sendMessageToApi(message);
        replaceLoadingMessage(responseText);
    } catch (error) {
        replaceLoadingMessage(getBotResponse(message));
        console.error('API chat error:', error);
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
});

async function sendMessageToApi(message) {
    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    });

    if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    return data.reply || data.message || 'Sorry, no answer was returned.';
}

function appendMessage(text, className) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.textContent = text;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendLoadingMessage() {
    const loadingElement = document.createElement('div');
    loadingElement.className = 'message bot-message loading-message';
    loadingElement.textContent = 'Thinking...';
    loadingElement.dataset.loading = 'true';
    chatBox.appendChild(loadingElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function replaceLoadingMessage(text) {
    const loadingMessage = chatBox.querySelector('[data-loading="true"]');
    if (loadingMessage) {
        loadingMessage.textContent = text;
        loadingMessage.removeAttribute('data-loading');
    } else {
        appendMessage(text, 'bot-message');
    }
}

function getBotResponse(message) {
    const normalized = message.toLowerCase();

    if (normalized.includes('hello') || normalized.includes('hi')) {
        return 'Hello! I am your AI study and career assistant. I can help with study plans, resume advice, internships, projects, and more.';
    }

    if (normalized.includes('study') || normalized.includes('learning')) {
        return 'Start with clear goals: pick one topic, follow a structured course, practice consistently, and review regularly. Break work into short daily sessions with focused tasks.';
    }

    if (normalized.includes('career') || normalized.includes('job') || normalized.includes('path')) {
        return 'Identify your strengths, explore roles that match your interests, build relevant skills, and connect with mentors. Use internships and small projects to test different career paths.';
    }

    if (normalized.includes('project') || normalized.includes('portfolio')) {
        return 'Choose projects that solve real problems and show your skills clearly: a portfolio site, task manager, study planner, or small web app. Host them on GitHub and add descriptions.';
    }

    if (normalized.includes('resume') || normalized.includes('cv') || normalized.includes('improve')) {
        return 'Keep your resume concise, emphasize achievements with measurable results, list relevant skills, and include project links. Tailor it for each role and keep the design clean.';
    }

    if (normalized.includes('how do i prepare for an internship') || normalized.includes('prepare for an internship')) {
        return 'To prepare for an internship, start with a strong plan: choose roles that match your interests, build one or two relevant projects, and keep your GitHub or portfolio up to date. Tailor your resume and cover letter for each application, practice common technical and behavioral questions, and be ready to explain your projects clearly. Show enthusiasm, highlight what you learned, and follow up politely after interviews.';
    }

    if (normalized.includes('internship')) {
        return 'For internships, focus on practical projects, keep your resume targeted, and prepare to explain your learnings clearly during interviews.';
    }

    if (normalized.includes('interview') || normalized.includes('technical') || normalized.includes('questions')) {
        return 'Practice common interview questions, explain your thinking clearly, and build confidence with mock interviews. Review algorithms, systems, and your own projects so you can talk about them easily.';
    }

    if (normalized.includes('web development') || normalized.includes('html') || normalized.includes('css') || normalized.includes('javascript')) {
        return 'For web development, learn HTML, CSS, and JavaScript first. Then add a frontend framework like React and a backend tool like Node.js or Express for full-stack skills.';
    }

    if (normalized.includes('skills') || normalized.includes('learn')) {
        return 'Focus first on core skills for your chosen area, then strengthen them with real practice projects. Soft skills like communication and time management are also important for career success.';
    }

    return 'I can help with study plans, career advice, internships, projects, resumes, and interview prep. Can you share more details so I can give a better answer?';
}
