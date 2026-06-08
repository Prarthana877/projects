# AI Study and Career Assistant

A polished study and career assistant chat app with a simple Node.js backend connected to the OpenAI API.

## Description

This chatbot is designed to help students and early career professionals explore study plans, career guidance, portfolio projects, resume advice, and technical interview preparation. The app combines a clean, mobile-friendly front end with a lightweight backend service that securely forwards chat requests to OpenAI. The conversational experience is built using standard web technologies so it remains easy to understand, extend, and deploy.

The front end is built with HTML, CSS, and JavaScript. `index.html` provides the chat interface structure and the suggested question buttons, `styles.css` creates a polished and responsive layout, and `script.js` manages user interactions, updates the message stream, and handles API requests. Thoughtful UX details like loading states, accessible form controls, and suggestion buttons make it easier for users to ask questions and receive instant answers.

The backend is implemented in Node.js using the Express framework. It exposes a single route, `/api/chat`, that accepts POST requests containing the user’s message. `server.js` loads environment variables using `dotenv` and uses the official OpenAI client library to forward the message to the OpenAI API model. The backend returns the assistant’s response as JSON, keeping the API key hidden from the browser and enabling secure server-side calls.

This architecture separates concerns clearly: the browser handles UI rendering and interaction, while the server handles API communication and security. The project also includes `cors` for safe cross-origin requests during local development and static file serving so the entire app can run from a single Node.js process.

The bot’s behavior can be customized by modifying the prompt logic in `server.js` or the local fallback responses in `script.js`. The current implementation includes clear guidance on study strategies, career path selection, project ideas, resume improvement, and interview preparation. This makes the chatbot useful for users who want practical advice on improving their learning habits and preparing for future technology roles.

## Project structure

- `index.html` — front-end chat UI
- `styles.css` — polished styling for the chat experience
- `script.js` — client-side chat logic and API integration
- `server.js` — Express backend that forwards chat messages to OpenAI
- `package.json` — Node.js package manifest
- `.env.example` — example environment file for storing secrets

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

3. Add your OpenAI API key to `.env`:
   ```text
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Run locally

Start the server:
```bash
npm start
```

Then open the chat app in your browser at:

```text
http://localhost:3000/index.html
```

## How it works

- The browser sends user messages to `/api/chat`.
- The Express backend forwards those messages to OpenAI.
- The backend returns the AI reply to the chat client.

## Notes

- Change the `API_ENDPOINT` in `script.js` if you run the backend on a different host or port.
- Use a valid OpenAI API key with access to the selected model.

## Customize

- Update `server.js` to use a different OpenAI model or prompt behavior.
- Style the app further in `styles.css`.
- Add richer chat message rendering in `script.js`.
