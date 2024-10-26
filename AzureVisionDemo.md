# Azure Vision Lab

## **Analyze Images with Azure AI Vision**

Azure AI Vision is an artificial intelligence capability that enables software systems to interpret visual input by analyzing images. In Microsoft Azure, the Vision Azure AI service provides pre-built models for common computer vision tasks, including analysis of images to suggest captions and tags, and detection of common objects and people. You can also use the Azure AI Vision service to remove the background or create a foreground matting of images.

---

### **Clone the Repository for This Course**

1. **Start Visual Studio Code**.
2. Open the palette (`SHIFT+CTRL+P`) and run a **Git: Clone** command to clone the following repository to a local folder:  
   `https://github.com/MicrosoftLearning/mslearn-ai-vision`
3. Open the cloned folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.
    - **Note:** If you are prompted to add required assets to build and debug, select **Not Now**.
    - If you are prompted with the message "Detected an Azure Function Project in folder," close that message.

---

### **Provision an Azure AI Services Resource**

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select **Create a resource**.
3. Search for **Azure AI services** and create an **Azure AI Services** multi-service account resource with the following settings:
    - **Subscription**: Your Azure subscription.
    - **Resource group**: Create or select an existing resource group.
    - **Region**: Choose from East US, West US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, or East Asia.
    - **Name**: Enter a unique name.
    - **Pricing tier**: Select **Standard S0**.
4. Select the required checkboxes and create the resource.
5. Wait for deployment to complete, then view the deployment details.
6. Navigate to the **Keys and Endpoint** page of the deployed resource. Copy the **Endpoint** and one of the **Keys** for later use.

---

## **Prepare to Use the Azure AI Vision SDK**

### **In Visual Studio Code:**

1. In the **Explorer** pane, navigate to `Labfiles/01-analyze-images` and expand the **C-Sharp** or **Python** folder based on your preferred language.
2. Right-click the `image-analysis` folder and open an integrated terminal.
3. Install the Azure AI Vision SDK package by running the appropriate command:

   **C#**:
   ```bash
   dotnet add package Azure.AI.Vision.ImageAnalysis -v 1.0.0-beta.3
   ```

   **Python**:
   ```bash
   pip install azure-ai-vision-imageanalysis==1.0.0b3
   ```

   - **Tip:** If you're using your own machine, you may also need to install `matplotlib` and `pillow`.

4. Open the configuration file in the folder and update the configuration values to reflect the **endpoint** and **key** for your Azure AI services resource. Save your changes.
    - **C#**: `appsettings.json`
    - **Python**: `.env`

---

## **Add Required Namespace Imports**

1. Open the client application code file:
    - **C#**: `Program.cs`
    - **Python**: `image-analysis.py`
2. Add the following language-specific code under the **Import namespaces** comment:

   **C#**:
   ```csharp
   // Import namespaces
   using Azure.AI.Vision.ImageAnalysis;
   ```

   **Python**:
   ```python
   # import namespaces
   from azure.ai.vision.imageanalysis import ImageAnalysisClient
   from azure.ai.vision.imageanalysis.models import VisualFeatures
   from azure.core.credentials import AzureKeyCredential
   ```

---

## **Authenticate the Azure AI Vision Client**

1. Find the **Authenticate Azure AI Vision client** comment in the `Main` function, and add the following code to create and authenticate the Azure AI Vision client:

   **C#**:
   ```csharp
   // Authenticate Azure AI Vision client
   ImageAnalysisClient client = new ImageAnalysisClient(
       new Uri(aiSvcEndpoint),
       new AzureKeyCredential(aiSvcKey));
   ```

   **Python**:
   ```python
   # Authenticate Azure AI Vision client
   cv_client = ImageAnalysisClient(
       endpoint=ai_endpoint,
       credential=AzureKeyCredential(ai_key)
   )
   ```

---

## **Analyze an Image to Suggest a Caption**

1. In the `AnalyzeImage` function, add the following code to retrieve specific features from the image:

   **C#**:
   ```csharp
   // Get result with specified features to be retrieved
   ImageAnalysisResult result = client.Analyze(
       BinaryData.FromStream(stream),
       VisualFeatures.Caption | 
       VisualFeatures.DenseCaptions |
       VisualFeatures.Objects |
       VisualFeatures.Tags |
       VisualFeatures.People);
   ```

   **Python**:
   ```python
   # Get result with specified features to be retrieved
   result = cv_client.analyze(
       image_data=image_data,
       visual_features=[
           VisualFeatures.CAPTION,
           VisualFeatures.DENSE_CAPTIONS,
           VisualFeatures.TAGS,
           VisualFeatures.OBJECTS,
           VisualFeatures.PEOPLE],
   )
   ```

2. In the `AnalyzeImage` function, display the analysis results:

   **C#**:
   ```csharp
   // Display analysis results
   if (result.Caption.Text != null)
   {
       Console.WriteLine($" Caption: \"{result.Caption.Text}\", Confidence {result.Caption.Confidence:0.00}\n");
   }
   ```

   **Python**:
   ```python
   # Display analysis results
   if result.caption is not None:
       print(f"\nCaption: '{result.caption.text}', Confidence: {result.caption.confidence * 100:.2f}%")
   ```

---

## **View the Images to Analyze**

1. In **Visual Studio Code**, expand the `image-analysis` folder and open the **images** folder.
2. View each image file (`street.jpg`, `building.jpg`, `person.jpg`) in Visual Studio Code to familiarize yourself with the images you'll analyze.

---

## **Analyze an Image to Suggest a Caption**

1. In the code file (`Program.cs` for C# or `image-analysis.py` for Python), locate the **Main function** and observe that the image file path is already specified.
2. Find the **Authenticate Azure AI Vision client** section and ensure your credentials are correct.
3. Find the `AnalyzeImage` function and follow these steps:

### **Step 1: Specify Image Analysis Features**

   **C#**:
   ```csharp
   // Specify features to retrieve
   ImageAnalysisResult result = client.Analyze(
       BinaryData.FromStream(stream),
       VisualFeatures.Caption | VisualFeatures.DenseCaptions | VisualFeatures.Objects | VisualFeatures.Tags | VisualFeatures.People);
   ```

   **Python**:
   ```python
   # Specify features to retrieve
   result = cv_client.analyze(
       image_data=image_data,
       visual_features=[
           VisualFeatures.CAPTION,
           VisualFeatures.DENSE_CAPTIONS,
           VisualFeatures.TAGS,
           VisualFeatures.OBJECTS,
           VisualFeatures.PEOPLE],
   )
   ```

### **Step 2: Display Analysis Results**

   - Add the following code to display the generated caption:

   **C#**:
   ```csharp
   // Display caption
   if (result.Caption.Text != null)
   {
       Console.WriteLine($" Caption: \"{result.Caption.Text}\", Confidence {result.Caption.Confidence:0.00}\n");
   }
   ```

   **Python**:
   ```python
   # Display caption
   if result.caption is not None:
       print(f"\nCaption: '{result.caption.text}', Confidence: {result.caption.confidence * 100:.2f}%")
   ```

---

## **Get Suggested Tags for an Image**

1. In the `AnalyzeImage` function, under the **Get image tags** comment, add the following code:

   **C#**:
   ```csharp
   // Get image tags
   if (result.Tags.Values.Count > 0)
   {
       Console.WriteLine("\n Tags:");
       foreach (DetectedTag tag in result.Tags.Values)
       {
           Console.WriteLine($" '{tag.Name}', Confidence: {tag.Confidence:F2}");
       }
   }
   ```

   **Python**:
   ```python
   # Get image tags
   if result.tags is not None:
       print("\nTags:")
       for tag in result.tags.list:
           print(f" Tag: '{tag.name}', Confidence: {tag.confidence * 100:.2f}%")
   ```

2. Run the program for each image file and observe the tags.

---

## **Detect and Locate Objects in an Image**

1. In the `AnalyzeImage` function, under the **Get objects in the image** comment, add the following code:

   **C#**:
   ```csharp
   // Get objects in the image
   if (result.Objects.Values.Count > 0)
   {
       Console.WriteLine(" Objects:");
       foreach (DetectedObject obj in result.Objects.Values)
       {
           Console.WriteLine($" '{obj.Tags[0].Name}', Confidence: {obj.Confidence:F2}");
       }
   }
   ```

   **Python**:
   ```python
   # Get objects in the image
   if result.objects is not None:
       print("\nObjects:")
       for obj in result.objects.list:
           print(f" Object: '{obj.tags[0].name}', Confidence: {obj.confidence * 100:.2f}%")
   ```

2. Save and run the program for each image file, observing the objects detected.

---

## **Detect and Locate People in an Image**

1. In the `AnalyzeImage` function, under the **Get people in the image** comment, add the following code:

   **C#**:
   ```csharp
   // Get people in the image
   if (result.People.Values.Count > 0)
   {
       Console.WriteLine(" People:");
       foreach (DetectedPerson person in result.People.Values)
       {
           Console.WriteLine($" Detected person, Confidence: {person.Confidence:F2}");
       }
   }
   ```

   **Python**:
   ```python
   # Get people in the image
   if result.people is not None:
       print("\nPeople detected:")
       for person in result.people.list:
           print(f" Detected person, Confidence: {person.confidence * 100:.2f}%")
   ```

2. Save and run the program for each image file. Review the `people.jpg` output file to see detected people.

---

## **Remove Background or Generate Foreground Matte of an Image**

1. Locate the `BackgroundForeground` function in the code.
2. Under **Remove the background from the image or generate a foreground matte**, add the following code:

   **C#**:
   ```csharp
   // Remove background
   var client = new HttpClient();
   client.BaseAddress = new Uri(endpoint);
   var contentData = new StringContent(jsonData, Encoding.UTF8, "application/json");
   var response = await client.PostAsync(url, contentData);
   if (response.IsSuccessStatusCode)
   {
       File.WriteAllBytes("background.png", await response.Content.ReadAsByteArrayAsync());
       Console.WriteLine("Results saved in background.png");
   }
   ```

   **Python**:
   ```python
   # Remove background
   headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
   response = requests.post(url, headers=headers, json=body)
   if response.status_code == 200:
       with open("background.png", "wb") as file:
           file.write(response.content)
       print("Results saved in background.png")
   ```

3. Run the program and check `background.png` to confirm that the background is removed.

---

## **Generate a Foreground Matte for the Image**

1. In the `BackgroundForeground` function, change the mode variable to `foregroundMatting` and rerun the code.
2. Save the foreground matte as `foreground.png` and confirm that it is correctly generated.

---

## **Clean Up Resources**

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com).
2. In the top search bar, search for **Azure AI services multi-service account**.
3. Select the resource and choose **Delete**.
4. Follow the on-screen instructions to delete the resource.

---

## **More Information**

For additional capabilities and use cases, see the [Azure AI Vision documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/).

--- 

