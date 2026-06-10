// Load server dependencies and environment variables.
const express = require('express');
const cors = require('cors');
const path = require('path');
const { Configuration, OpenAIApi } = require('openai');
require('dotenv').config();

// Create the Express app and read runtime configuration.
const app = express();
const port = process.env.PORT || 3000;
const apiKey = process.env.OPENAI_API_KEY;

// Stop early if the OpenAI API key has not been configured.
if (!apiKey) {
console.error('Missing OPENAI_API_KEY in environment. Create a .env file and set OPENAI_API_KEY=your_key');
process.exit(1);
}

// Configure the OpenAI client.
const configuration = new Configuration({ apiKey });
const openai = new OpenAIApi(configuration);

// Enable JSON requests, CORS, and static file hosting for the front end.
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Chat endpoint used by script.js to get an AI response.
app.post('/api/chat', async (req, res) => {
const { message } = req.body;
if (!message || typeof message !== 'string') {
    return res.status(400).json({ error: 'message is required' });
}

try {
    // Send the user's message with a focused assistant role prompt.
    const completion = await openai.createChatCompletion({
        model: 'gpt-4o-mini',
        messages: [
        {
            role: 'system',
            content: 'You are an AI assistant that helps users with study plans, career advice, internship guidance, and project ideas.'
        },
        {
            role: 'user',
            content: message
        }
        ],
        max_tokens: 250,
        temperature: 0.8
    });

    // Return the generated reply to the browser.
    const reply = completion.data.choices?.[0]?.message?.content?.trim() || 'Sorry, I was unable to generate an answer.';
    res.json({ reply });
    } catch (error) {
        console.error('OpenAI request failed:', error);
        res.status(500).json({ error: 'Failed to get a response from the API.' });
    }
});

// Start the local development server.
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
    console.log('Open http://localhost:3000/index.html in your browser to use the chat app.');
});
