# AI Study and Career Assistant

A polished study and career assistant chat app with a simple Node.js backend connected to the OpenAI API.

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
