# 🚀 Vortex Watch

>  A security extension that scans terms, privacy policies, and HTML to warn users so of scams and suspicious websites in real time.

## 📖 Overview  
**Protect Your Privacy, One Click at a Time**  

In today’s digital world, hidden dangers lurk within the fine print of websites. Our Chrome extension empowers users by analyzing Terms & Conditions, Privacy Policies, and web content to detect potential security risks. Using OpenAI, Cohere AI, and Gemini, we scan for malicious clauses and suspicious content that might compromise your privacy or data security.

With real-time pop-up notifications, our extension keeps you informed whenever you visit a site, ensuring you browse safely. Designed for a community that values transparency and security, this tool puts the power back in your hands—because protecting your data shouldn’t be a guessing game.

**Core Safety Analysis:**

* Automated Privacy Policy Analysis (AI-powered)
* Highlighting Problematic Policy Sentences
* Privacy Concern Summaries
* Website Structure & Behavior Analysis (HTML, JavaScript)
* Phishing & Malware Detection
* Suspicious Design Pattern Identification
* Safety Scoring (1-10)
* Website Safety Categorization (Safe, Suspicious, Unsafe)
* Safe Alternative Website Recommendations

**User Interface & Experience:**

* Seamless Browser Integration
* Simplified Safety Reporting
* History Log of Website Checks
* Customizable Alert System (Future)

**Technical & Performance:**

* AI-Driven Analysis (Cohere, OpenAI, Gemini)
* Efficient Web Scraping (Beautiful Soup, Selenium)
* Scalable Cloud Infrastructure (Google Servers)
* API Driven architecture.
* Cross-Platform Compatibility (Mobile - Future)

## 🛠 Tech Stack  
- **Frontend:** / HTML / CSS / JavaScript /   
- **Backend:** Python  / Flask /   
- **AI:** Cohere AI / OpenAI / Gemini AI

## 🚀 Setup Instructions

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/VortexWatch.git](https://github.com/yourusername/VortexWatch.git)
    cd VortexWatch
    ```

2.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

4.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Environment Variables:**
    * Create a `.env` file in the `backend` directory.
    * Add your API keys and other sensitive information to the `.env` file. For example:
        ```
        OPENAI_API_KEY=your_openai_api_key
        GOOGLE_API_KEY=your_google_api_key
        COHERE_API_KEY=your_cohere_api_key
        ```
    * Ensure the python backend can read these variables.
    * If you are using selenium, you will need to download the chrome driver that matches your chrome version. You can download it from here: https://chromedriver.chromium.org/downloads. Place the driver in a location that is accessible by your operating system's PATH variable, or place it in the same directory as the python script.

6.  **Navigate to the Frontend Directory:**
    ```bash
    cd ../frontend
    ```

7.  **Install Node.js Dependencies:**
    ```bash
    npm install
    ```

8.  **Run the Backend Server:**
    * Go back to the `backend` directory.
    ```bash
    cd ../backend
    python main.py
    ```

9.  **Run the Frontend Development Server:**
    * Go to the `frontend` directory.
    ```bash
    cd ../frontend
    npm start
    ```

10. **Install the Chrome Extension**

    * Navigate to `chrome-extension` directory
    * Open chrome and go to `chrome://extensions/`
    * Enable developer mode (toggle switch at the top right)
    * Click on "Load unpacked" and select the `chrome-extension` directory.

**Important Notes:**

* Replace `yourusername` with your actual GitHub username.
* Ensure you have Python 3 and Node.js installed on your system.
* Make sure you have valid API keys for OpenAI, Google Generative AI, and Cohere.
* Selenium requires a compatible ChromeDriver.
* The frontend will typically run on `http://localhost:3000`, and the backend on `http://localhost:5000`.
* The chrome extension will add the functionality to your browser.



** 🙌 Acknowledgments **
We would like to express our sincere gratitude to everyone who contributed to the development of VortexWatch. This project wouldn't have been possible without the support and guidance we received throughout the Genesis GenAI Hackathon.

We also want to extend our appreciation to the organizers of the Genesis GenAI Hackathon for creating an inspiring and supportive environment. Your dedication to fostering innovation and collaboration made this experience truly remarkable.

Finally, we are grateful to our mentors for their invaluable feedback and guidance. Your insights helped us refine our project and overcome the challenges we faced.
