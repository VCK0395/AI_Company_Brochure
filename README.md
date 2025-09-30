# 🔗 **AI-Powered Website Link Analyzer**

Extract and filter relevant links from a corporate website using web scraping and the Gemini API. This tool is designed to quickly identify links useful for a company brochure, such as **About Us, Careers, and Company History** pages.

---

## 💡 What It Does 

This Python script performs a two-step process to intelligently filter a website's links:

1.  **Web Scraping:** It fetches the content of a specified URL, handles common scraping issues (like missing headers and relative links), and extracts all unique, absolute, non-duplicate links from the page.
2.  **AI Analysis (Gemini):** It passes the list of extracted links to the **Gemini 1.5 Flash** model, which is instructed to act as an analyst and identify the links most relevant for a corporate brochure. It strictly enforces a **JSON output format** for reliable, structured data extraction.

This process automates the tedious task of manually sifting through dozens of links to find the key information pages.

---

## 🛠️ How to Use It 

### Prerequisites

You'll need the following installed:

* **Python 3.8+**
* A **Google AI Studio API Key** (formerly Gemini API Key).

### Setup

1.  **Clone the Repository** (assuming you'll place the code in a file like `analyzer.py`):
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```

2.  **Install Dependencies:**
    ```bash
    pip install requests beautifulsoup4 python-dotenv google-genai
    ```

3.  **Configure API Key:**
    Create a file named **`.env`** in the root directory of the project and add your API key:
    ```
    # .env file
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

### Running the Code

The main logic resides in the `get_links(url: str)` function. To run the script, you would typically add an execution block at the end of your file:

```python
# Add this block to the end of your file (e.g., analyzer.py)
if __name__ == "__main__":
    target_url = "[https://www.example.com](https://www.example.com)" # Replace with your target website
    relevant_links = get_links(target_url)
    
    print("\n--- AI Analysis Results ---")
    if relevant_links.get("links"):
        for link_data in relevant_links["links"]:
            print(f"[{link_data['type'].title()}]: {link_data['url']}")
    else:
        print("No relevant links were identified.")
```

## 🎯 Why This Project 

Mastering the ML Pipeline
This project serves as an excellent demonstration of a complete, end-to-end Machine Learning pipeline, which is crucial for real-world data science tasks:

Handling Real-World Data Issues: The code effectively addresses the challenge of missing values, which are common in real-world datasets, by implementing appropriate imputation strategies for both numerical and categorical features.

Essential Preprocessing Steps: It highlights the necessity of One-Hot Encoding for categorical data and MinMaxScaler for feature scaling, both of which are critical steps for models like Logistic Regression.

Robust Model Optimization: The use of GridSearchCV demonstrates best practices for model optimization, ensuring the final model is not only trained but also fine-tuned for better predictive power and generalization on unseen data.

This project validates the importance of data preprocessing and hyperparameter tuning in achieving high-performing and reliable classification models.

