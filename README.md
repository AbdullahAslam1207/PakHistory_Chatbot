# Pakistan History Chatbot

## Overview
The **Pakistan History Chatbot** is an AI-powered chatbot designed to provide accurate and insightful responses to queries related to Pakistan’s historical events and news. The system integrates document-based retrieval, internet search capabilities, and real-time news fetching to ensure comprehensive responses.

## Features
✅ **Document Integration** – Supports PDF, TXT, and DOCX files for historical data extraction.
✅ **Retrieval-Augmented Generation (RAG)** – Uses RAG to fetch relevant information from documents before generating responses.
✅ **Internet Search** – Employs Google Custom Search API to retrieve information when documents lack relevant data.
✅ **Real-Time News Retrieval** – Fetches the latest news updates based on user queries.
✅ **Sensitive Query Handling** – Triggers an email notification for restricted topics and informs users of the limitation.
✅ **Source Attribution** – Differentiates between document-based and internet-sourced information in responses.
✅ **User-Friendly Interface** – Designed for seamless interaction and query handling.
✅ **Scalability** – Allows the addition of more documents over time.

## Tech Stack
- **LangGraph Agents** – Used for structured AI agent orchestration.
- **Retrieval-Augmented Generation (RAG)** – Implements retrieval-based responses from stored documents.
- **Google Custom Search API** – Enables precise online searches for real-time data.
- **Flask** – Backend framework for handling requests.
- **Twilio SendGrid (Optional)** – Used for email alerts on sensitive queries.

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/pakistan-history-chatbot.git
   cd pakistan-history-chatbot
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file and add the required API keys and configurations.
   ```env
   GOOGLE_CUSTOM_SEARCH_API_KEY=your_api_key
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
   EMAIL_ALERT_RECEIVER=your_email@example.com
   ```
5. Run the chatbot:
   ```bash
   python application.py
   ```

## Usage
- Upload historical documents (PDF, TXT, DOCX) for enhanced query responses.
- Ask questions related to Pakistan’s history and news.
- If the answer is unavailable in the documents, the chatbot will fetch relevant data from the internet.
- For sensitive queries, the chatbot will restrict access and trigger an email alert.

## Limitations
- Only responds to queries related to **Pakistan’s history and news**.
- Does not provide information about other countries.
- Sensitive topics (e.g., army or special forces events) trigger an email alert instead of a direct response.

## Future Enhancements
- Expand document database for broader historical coverage.
- Improve NLP capabilities for better contextual understanding.
- Optimize real-time news retrieval with additional sources.

## Contributing
Feel free to submit issues or pull requests to improve the chatbot. Contributions are always welcome!

## Contact
For any inquiries, reach out to am0055461@gmail.com or open an issue in the repository.

