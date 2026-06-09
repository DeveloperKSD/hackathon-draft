# 🚀 Xianyu AutoAgent - Intelligent E-commerce Chatbot System

An AI-driven auto-reply and negotiation solution designed for e-commerce platforms. It utilizes a **Hierarchical Router & Expert Agents** architecture to classify buyer intentions, answer technical questions, and negotiate prices dynamically. 

This repository has been fully optimized to support running locally with a standalone Web Simulator using only a **Google Gemini API Key** (or any OpenAI-compatible API), requiring no Chinese accounts, phone numbers, or cookies.

---

## 🌟 Core Features

### 1. Multi-Agent Expert System
Instead of using a single generic chatbot prompt, this system splits tasks among specialized expert agents:
*   **Intent Router**: Evaluates incoming queries using rules/regex, falling back to a lightweight LLM classifier to assign the conversation to the most relevant expert.
*   **Bargaining Agent (`PriceAgent`)**: Employs a **dynamic negotiation temperature** strategy. As bargaining rounds increase, the model's temperature increases, allowing for more creative and flexible counter-offers.
*   **Technical Advisor Agent (`TechAgent`)**: Explains complex product specifications in clear, everyday terms.
*   **Customer Service Agent (`DefaultAgent`)**: Guides users through standard checks, shipping info, and final checkout.

### 2. Standalone Web Simulator Dashboard
*   **No Platform Setup Needed**: Play and test with the chatbot logic entirely locally.
*   **Product Context Editor**: Instantly define simulated items (Title, Price, Stock, Description) or load presets (Mechanical Keyboard, iPhone 13, Studio Mic).
*   **Interactive Conversation Log**: View real-time buyer messages, agent replies, activated sub-agent statuses, and bargaining round indicators.
*   **Platform Safety Filter**: Overrides and blocks attempts to direct users to offline channels (e.g., QQ, WeChat, direct cards) to prevent fraud.

---

## 🚴 Quick Start

### Requirements
*   Python 3.8+
*   Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/))

### Installation
1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your environment variables inside the `.env` file:
   ```env
   API_KEY=YOUR_GEMINI_API_KEY
   MODEL_BASE_URL=https://generativelanguage.googleapis.com/v1beta/
   MODEL_NAME=gemini-1.5-flash
   ```

3. Launch the Simulator Server:
   ```bash
   python server.py
   ```

4. Open your browser and navigate to:
   ```text
   http://localhost:8000
   ```

---

## 🛠 Project Structure

*   `server.py`: Lightweight Python HTTP backend serving the simulator API.
*   `index.html`: Modern, responsive dark-themed dashboard frontend.
*   `XianyuAgent.py`: Core logic containing agent classes (`BaseAgent`, `PriceAgent`, `TechAgent`, `ClassifyAgent`) and the `IntentRouter`.
*   `context_manager.py`: SQLite-based message context database layer.
*   `main.py`: Original live WebSocket client for Goofish/Xianyu platforms.
*   `prompts/`: Editable text files containing the system prompts for each agent.

---

## 🚀 Future Scope

Since the core AI reasoning and negotiation components are generic, the system can be expanded to support non-Chinese platforms and global secondhand markets:

### 1. Global Platform Adaptability
*   **Multi-Platform Connectors**: Adapt the WebSocket/webhook logic to integrate with global platforms like **Facebook Marketplace**, **eBay**, **OLX (India)**, or **Shopify**.
*   **Multi-language Prompt Bundles**: Expand the files in the `prompts/` directory to natively support English, Hindi, Spanish, etc., translating Chinese platform slangs (e.g., "可小刀", "包邮") to their regional equivalents (e.g., "Negotiable", "Free shipping").

### 2. Advanced AI Capabilities
*   **RAG Knowledge Base**: Connect the `TechAgent` to custom database tables or text manuals (e.g., electronics spec sheets, user manuals) so it can pull precise answer contexts automatically.
*   **Rule-based Price Caps**: Introduce physical minimum price thresholds (e.g., a setting where the AI is strictly forbidden from offering less than 85% of the original product price).
*   **Voice Messages support**: Use Speech-to-Text and Text-to-Speech models to allow buyers to send voice notes and receive vocal audio responses.

### 3. Simulator & UI Enhancements
*   **Prompt Editor Dashboard**: Allow editing and saving custom prompts directly from the web browser instead of opening text files in an editor.
*   **Database Viewer**: A dashboard tab showing saved items, overall successful negotiations, average concession rates, and historical logs.
