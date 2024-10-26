## **Demo 1: Azure Cognitive Services - Text Analytics**

### **Step 1: Sign into Azure Portal**

1. Go to [Azure Portal](https://portal.azure.com/).
2. Sign in with your Azure account credentials.
3. If you don’t have an account, sign up for a free Azure account [here](https://azure.microsoft.com/en-us/free/).

---

### **Step 2: Create a New Resource for Text Analytics**

1. Once signed in, click **Create a resource** in the left-hand menu.
2. In the **Search the Marketplace** bar, type **Text Analytics**.
3. Select **Text Analytics** from the search results.
4. Click **Create**.
5. Fill in the following fields in the **Create Text Analytics** form:
    - **Subscription**: Select your active subscription.
    - **Resource Group**: Either create a new resource group (e.g., `TextAnalyticsDemo`) or use an existing one.
    - **Region**: Choose the region closest to you.
    - **Name**: Choose a unique name for the service (e.g., `TextAnalyticsDemoService`).
    - **Pricing Tier**: Select the free tier (F0) for the demo.
6. Click **Review + Create**, and then **Create**.

---

### **Step 3: Access the Text Analytics Service**

1. Once the resource is created, navigate to the **Text Analytics** resource in your **Resource Group**.
2. In the resource overview, click **Keys and Endpoint** on the left-side menu.
3. Copy the **Key1** and **Endpoint** values. These will be used to authenticate your API requests.

---

### **Step 4: Use the Text Analytics API with Postman**

1. Download and install **Postman** (if not already installed) from [here](https://www.postman.com/downloads/).
2. Open Postman, and click **New** -> **HTTP Request**.
3. Set up the request as follows:
    - **Method**: POST
    - **URL**: Paste the **Endpoint** you copied earlier, followed by `/text/analytics/v3.1-preview.5/sentiment`
    - Example: `https://<your-resource-name>.cognitiveservices.azure.com/text/analytics/v3.1-preview.5/sentiment`
4. In the **Headers** tab, add the following:
    - **Key**: `Ocp-Apim-Subscription-Key`
    - **Value**: Paste the **Key1** you copied earlier.
5. In the **Body** tab, select **raw** and **JSON** as the format. Add the following JSON payload:
```json
{
  "documents": [
    {
      "id": "1",
      "text": "The service was amazing and the team was very helpful!"
    },
    {
      "id": "2",
      "text": "I had a terrible experience. The product was faulty and customer support was unresponsive."
    }
  ]
}
```
6. Click **Send** to make the request.

---

### **Step 5: Review Sentiment Analysis Results**

1. In Postman, you'll see the response in JSON format. It should look something like this:
```json
{
  "documents": [
    {
      "id": "1",
      "sentiment": "positive",
      "confidenceScores": {
        "positive": 0.99,
        "neutral": 0.01,
        "negative": 0.00
      }
    },
    {
      "id": "2",
      "sentiment": "negative",
      "confidenceScores": {
        "positive": 0.00,
        "neutral": 0.00,
        "negative": 1.00
      }
    }
  ],
  "errors": [],
  "modelVersion": "latest"
}
```
2. Explain the **sentiment** values (positive, neutral, or negative) and the **confidence scores** that show how certain the model is in its assessment.

---

### **Step 6: Perform Key Phrase Extraction**

1. In Postman, change the URL to:
    - `https://<your-resource-name>.cognitiveservices.azure.com/text/analytics/v3.1-preview.5/keyPhrases`
2. Use the same request body as in **Step 4**.
3. Click **Send**.
4. Review the response, which will include key phrases from each document:
```json
{
  "documents": [
    {
      "id": "1",
      "keyPhrases": [
        "service",
        "team",
        "helpful"
      ]
    },
    {
      "id": "2",
      "keyPhrases": [
        "terrible experience",
        "faulty product",
        "unresponsive customer support"
      ]
    }
  ],
  "errors": [],
  "modelVersion": "latest"
}
```
5. Explain how the key phrases summarize the main themes of each document.

---

### **Step 7: Perform Language Detection**

1. Change the URL again to:
    - `https://<your-resource-name>.cognitiveservices.azure.com/text/analytics/v3.1-preview.5/languages`
2. Use the same request body as before.
3. Click **Send**.
4. Review the response, which will indicate the detected language for each text:
```json
{
  "documents": [
    {
      "id": "1",
      "detectedLanguage": {
        "name": "English",
        "iso6391Name": "en",
        "confidenceScore": 1.0
      }
    },
    {
      "id": "2",
      "detectedLanguage": {
        "name": "English",
        "iso6391Name": "en",
        "confidenceScore": 1.0
      }
    }
  ],
  "errors": []
}
```
5. Explain how the service accurately detects the language and confidence score.

---

### **Wrap-Up**

- Show attendees how Text Analytics can be used in real-world scenarios like customer feedback analysis, content moderation, or business insights.
- Remind them of the variety of Cognitive Services available in Azure for text, vision, and speech tasks.
  
---
