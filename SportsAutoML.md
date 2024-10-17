# Azure AutoML for Predicting NFL Wins and Losses Demo Instructions

## Objective
The goal of this demo is to use **Azure AutoML** to create a predictive model using **historical NFL data** from the **Sports DB API**. We will use Azure Machine Learning Studio to develop a model that predicts NFL team wins and losses. The dataset will include historical game statistics and performance metrics, which will be used for training the model.

### Prerequisites
- **Azure Account**: Ensure you have an active Azure subscription.
- **Azure Machine Learning Workspace**: Create a Machine Learning workspace in Azure before starting this demo.
- **Sports DB API Key**: You need an API key to access the **Sports DB API**. Sign up at [TheSportsDB](https://www.thesportsdb.com/) to obtain an API key.
- **Development Environment**: Python (for downloading the data using the API) or a similar tool to extract and preprocess data.

---

## Step-by-Step Instructions

### Step 1: Extract Historical NFL Data from Sports DB API
1. **Get API Key**: Ensure you have your API key from **TheSportsDB**.
2. **Use Python to Extract Data**:
   - Write a script in Python to access the **Sports DB API** and extract historical NFL data. Here is a sample Python script to get you started:

   ```python
   import requests
   import pandas as pd

   API_KEY = 'YOUR_SPORTS_DB_API_KEY'
   SEASON = '2022'  # Example season
   URL = f'https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventspastleague.php?id=4391'

   response = requests.get(URL)
   data = response.json()

   # Extract relevant data
   games = data['events']
   rows = []
   for game in games:
       rows.append({
           'Date': game['dateEvent'],
           'HomeTeam': game['strHomeTeam'],
           'AwayTeam': game['strAwayTeam'],
           'HomeScore': game['intHomeScore'],
           'AwayScore': game['intAwayScore']
       })

   # Convert to DataFrame
   df = pd.DataFrame(rows)
   df.to_csv('nfl_historical_data.csv', index=False)
   ```
3. **Save the Data**: Save the extracted data as a **CSV file** (e.g., `nfl_historical_data.csv`) to be uploaded to Azure Machine Learning Studio.

### Step 2: Set Up Azure Machine Learning Studio
1. **Navigate to Azure Portal**: Go to [Azure Portal](https://portal.azure.com/) and sign in using your Azure credentials.
2. **Create a Machine Learning Workspace**:
   - Search for **Machine Learning** in the search bar and select **Machine Learning** from the results.
   - Click **Create** to start setting up your workspace.
   - Fill in the details:
     - **Subscription**: Select your subscription.
     - **Resource Group**: Choose an existing resource group or create a new one.
     - **Workspace Name**: Provide a unique name for your workspace.
     - **Region**: Choose a location closest to you.
   - Click **Review + Create** and then **Create** to finalize the workspace creation.
3. **Access Azure Machine Learning Studio**:
   - Once the workspace is created, click **Go to Resource**.
   - Click on **Launch Studio** to open Azure Machine Learning Studio.

### Step 3: Upload the Dataset
1. **Navigate to Datasets**:
   - In Azure Machine Learning Studio, click on **Datasets** in the left-hand menu.
2. **Create a New Dataset**:
   - Click **+ Create Dataset** and select **From Local Files**.
   - Upload the **nfl_historical_data.csv** file you created.
3. **Configure Dataset Details**:
   - Enter a **name** for your dataset (e.g., "NFL_Historical_Data").
   - Select **Tabular** as the dataset type and ensure **CSV** is chosen as the file format.
   - Click **Next** to configure data format settings, verify that the data is correctly parsed, and then click **Create**.

### Step 4: Create an AutoML Experiment
1. **Start a New AutoML Run**:
   - In the Azure ML Studio, click **Automated ML** from the left-hand menu.
   - Click **+ New Automated ML Run**.
2. **Select Dataset**:
   - Select the **NFL_Historical_Data** dataset you uploaded in the previous step.
   - Click **Next**.
3. **Set Up Experiment**:
   - **Experiment Name**: Provide a name for the experiment, such as "NFL_Win_Prediction".
   - **Target Column**: Set the target column as **Winner** (this column should be computed based on HomeScore and AwayScore to determine which team won).
4. **Select Compute Cluster**:
   - **Compute Type**: Choose **Compute Cluster** and select an existing cluster or create a new one.
   - To create a new cluster:
     - Click **Create New** and specify the **Virtual Machine size** and **Minimum/Maximum nodes**.
     - Click **Create** to finalize the cluster.
5. **Configure Task Type**:
   - Select **Classification** as the task type since we are predicting whether a team will win or lose.
   - Click **Next** to proceed.

### Step 5: Configure Experiment Settings and Run
1. **Experiment Settings**:
   - **Primary Metric**: Select **Accuracy** as the primary metric to evaluate the models.
   - **Training Duration**: Set the training duration based on your available time (e.g., 1.5 hours).
2. **Run the Experiment**:
   - Click **Finish** to start the AutoML experiment.
   - The system will start training multiple models and evaluate their performance.

### Step 6: Review the Results
1. **Access the Model Leaderboard**:
   - Once the experiment is complete, navigate to the **Models** tab to view the leaderboard of models.
   - Models are ranked based on the **primary metric** (Accuracy).
2. **Select the Best Model**:
   - Click on the best-performing model to view more details.
   - Review the **Precision, Recall, F1 Score**, and other metrics to evaluate model performance.
3. **Explore Feature Importance**:
   - In the model details, go to the **Explanations** tab to see the **feature importance**. This helps you understand which features had the most impact on the predictions.

### Step 7: Deploy the Best Model
1. **Deploy the Model**:
   - Click **Deploy** on the best-performing model's page.
   - Provide a **name** for the deployment (e.g., "NFLWinPredictorAPI").
   - **Compute Type**: Select **Azure Container Instance** for a quick deployment.
2. **Authentication**:
   - Enable authentication to secure your model endpoint.
   - Click **Deploy** to start the deployment process.

### Step 8: Test the Deployed Model
1. **Access the Endpoint**:
   - Once the deployment is complete, navigate to the **Endpoints** section in Azure Machine Learning Studio.
2. **Test the Web Service**:
   - Click on the deployed model and select **Test**.
   - Use the **sample data** provided or enter your own data to test the predictions.
   - The model will return a prediction indicating which team is likely to win.

### Step 9: Consume the Model via API
1. **Get API Details**:
   - In the **Endpoints** section, click on your deployed model.
   - Copy the **REST API endpoint** and the **API key**.
2. **Use the API**:
   - Use tools like **Postman** or integrate the API into your application to send data and receive predictions.

---

## Summary
In this demo, we used **Azure AutoML** to create a predictive model for NFL team wins and losses. The steps included extracting data from the Sports DB API, setting up a Machine Learning workspace, running an AutoML experiment, and deploying the best model. This demo demonstrates how sports data can be leveraged to make informed predictions using Azure's powerful machine learning tools.

