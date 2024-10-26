# Azure Vision AI Demo
---

## **Analyze Images with Azure AI Vision**

Azure AI Vision is an artificial intelligence capability that enables software systems to interpret visual input by analyzing images. In Microsoft Azure, the Vision Azure AI service provides pre-built models for common computer vision tasks, including analysis of images to suggest captions and tags, detection of common objects and people. You can also use the Azure AI Vision service to remove the background or create a foreground matting of images.

---

## **Clone the Repository for This Course**

1. **Start Visual Studio Code**.
2. Open the palette (`SHIFT+CTRL+P`) and run a **Git: Clone** command to clone the following repository to a local folder:  
   `https://github.com/MicrosoftLearning/mslearn-ai-vision`
3. When the repository has been cloned, open the folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.
    - **Note**: If prompted to add required assets to build and debug, select **Not Now**.
    - If prompted with the message "Detected an Azure Function Project in folder," close that message.

---

## **Provision an Azure AI Services Resource**

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select **Create a resource**.
3. In the search bar, search for **Azure AI services**. Select **Azure AI Services**, and create an Azure AI services multi-service account resource with the following settings:
    - **Subscription**: Your Azure subscription.
    - **Resource group**: Choose or create a resource group (if using a restricted subscription, you may not have permission to create a new resource group - use the one provided).
    - **Region**: Choose from East US, West US, France Central, Korea Central, North Europe, Southeast Asia, West Europe, or East Asia.
    - **Name**: Enter a unique name.
    - **Pricing tier**: Standard S0.
4. Select the required checkboxes and create the resource.
5. Wait for deployment to complete, and then view the deployment details.
6. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page in the next procedure.

---

## **Prepare to Use the Azure AI Vision SDK**

In this exercise, you'll complete a partially implemented client application that uses the Azure AI Vision SDK to analyze images.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the `Labfiles/01-analyze-images` folder and expand the **C-Sharp** or **Python** folder, depending on your language preference.
2. Right-click the `image-analysis` folder and open an integrated terminal.
3. Install the Azure AI Vision SDK package by running the appropriate command for your language preference:

   **C#**:
   ```bash
   dotnet add package Azure.AI.Vision.ImageAnalysis -v 1.0.0-beta.3
   ```

   **Python**:
   ```bash
   pip install azure-ai-vision-imageanalysis==1.0.0b3
   ```

   - **Tip**: If you are doing this lab on your own machine, you'll also need to install `matplotlib` and `pillow` and `python-dotenv`.

4. View the contents of the `image-analysis` folder and note the configuration settings file:
    - **C#**: `appsettings.json`
    - **Python**: `.env`
5. Open the configuration file and update the configuration values to reflect the **endpoint** and an **authentication key** for your Azure AI services resource. Save your changes.

---

## **Import Required Namespaces**

1. Open the client application code file:
    - **C#**: `Program.cs`
    - **Python**: `image-analysis.py`
2. Under the **Import namespaces** comment, add the following language-specific code to import the namespaces required to use the Azure AI Vision SDK:

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

## **View the Images to Analyze**

1. In **Visual Studio Code**, expand the `image-analysis` folder and the **images** folder it contains.
2. Select each image file in turn to view it in Visual Studio Code.

---

## **Analyze an Image to Suggest a Caption**

1. In the code file for your client application (`Program.cs` for C# or `image-analysis.py` for Python), in the **Main function**, note that the code to load the configuration settings has been provided. Then find the comment **Authenticate Azure AI Vision client**. Under this comment, add the following code to create and authenticate an Azure AI Vision client object:

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

2. In the `AnalyzeImage` function, under the comment **Get result with specified features to be retrieved**, add the following code to specify the analysis features you want to retrieve:

   **C#**:
   ```csharp
   // Get result with specified features to be retrieved
   ImageAnalysisResult result = client.Analyze(
       BinaryData.FromStream(stream),
       VisualFeatures.Caption | VisualFeatures.DenseCaptions | VisualFeatures.Objects | VisualFeatures.Tags | VisualFeatures.People);
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

3. In the `AnalyzeImage` function, under the comment **Display analysis results**, add the following code (including the comments indicating where you will add more code later):

   **C#**:
   ```csharp
   // Display analysis results
   // Get image captions
   if (result.Caption.Text != null)
   {
       Console.WriteLine(" Caption:");
       Console.WriteLine($"   \"{result.Caption.Text}\", Confidence {result.Caption.Confidence:0.00}\n");
   }

   // Get image dense captions
   Console.WriteLine(" Dense Captions:");
   foreach (DenseCaption denseCaption in result.DenseCaptions.Values)
   {
       Console.WriteLine($"   Caption: '{denseCaption.Text}', Confidence: {denseCaption.Confidence:0.00}");
   }

   // Get image tags

   // Get objects in the image

   // Get people in the image
   ```

   **Python**:
   ```python
   # Display analysis results
   # Get image captions
   if result.caption is not None:
       print("\nCaption:")
       print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))

   # Get image dense captions
   if result.dense_captions is not None:
       print("\nDense Captions:")
       for caption in result.dense_captions.list:
           print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))

   # Get image tags

   # Get objects in the image

   # Get people in the image
   ```

4. Save your changes and return to the integrated terminal for the image-analysis folder, and enter the following command to run the program with the argument images/street.jpg:

   **C#**:
   ```csharp

   dotnet run images/street.jpg

   ```

   **Python**:
   ```python

   python image-analysis.py images/street.jpg

   ```
Observe the output, which should include a suggested caption for the street.jpg image.
Run the program again, this time with the argument images/building.jpg to see the caption that gets generated for the building.jpg image.
Repeat the previous step to generate a caption for the images/person.jpg file.
Get suggested tags for an image
It can sometimes be useful to identify relevant tags that provide clues about the contents of an image.
## **Get Suggested Tags for an Image**

1. In the `AnalyzeImage` function, under the comment **Get image tags**, add the following code:

   **C#**:
   ```csharp
   // Get image tags
   if (result.Tags.Values.Count > 0)
   {
       Console.WriteLine("\n Tags:");
       foreach (DetectedTag tag in result.Tags.Values)
       {
           Console.WriteLine($"   '{tag.Name}', Confidence: {tag.Confidence:F2}");
       }
   }
   ```

   **Python**:
   ```python
   # Get image tags
   if result.tags is not None:
       print("\nTags:")
       for tag in result.tags.list:
           print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))
   ```

2. Save your changes and run the program for each image file in the `images` folder, observing that a list of suggested tags is displayed along with the image caption.

---

## **Detect and Locate Objects in an Image**

Object detection identifies specific objects within an image and their location indicated by a bounding box.

1. In the `AnalyzeImage` function, under the comment **Get objects in the image**, add the following code:

   **C#**:
   ```csharp
   // Get objects in the image
   if (result.Objects.Values.Count > 0)
   {
       Console.WriteLine(" Objects:");

       // Prepare image for drawing
       stream.Close();
       System.Drawing.Image image = System.Drawing.Image.FromFile(imageFile);
       Graphics graphics = Graphics.FromImage(image);
       Pen pen = new Pen(Color.Cyan, 3);
       Font font = new Font("Arial", 16);
       SolidBrush brush = new SolidBrush(Color.WhiteSmoke);

       foreach (DetectedObject detectedObject in result.Objects.Values)
       {
           Console.WriteLine($"   \"{detectedObject.Tags[0].Name}\"");

           // Draw object bounding box
           var r = detectedObject.BoundingBox;
           Rectangle rect = new Rectangle(r.X, r.Y, r.Width, r.Height);
           graphics.DrawRectangle(pen, rect);
           graphics.DrawString(detectedObject.Tags[0].Name, font, brush, (float)r.X, (float)r.Y);
       }

       // Save annotated image
       String output_file = "objects.jpg";
       image.Save(output_file);
       Console.WriteLine("  Results saved in " + output_file + "\n");
   }
   ```

   **Python**:
   ```python
   # Get objects in the image
   if result.objects is not None:
       print("\nObjects in image:")

       # Prepare image for drawing
       image = Image.open(image_filename)
       fig = plt.figure(figsize=(image.width/100, image.height/100))
       plt.axis('off')
       draw = ImageDraw.Draw(image)
       color = 'cyan'

       for detected_object in result.objects.list:
           # Print object name
           print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))

           # Draw object bounding box
           r = detected_object.bounding_box
           bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
           draw.rectangle(bounding_box, outline=color, width=3)
           plt.annotate(detected_object.tags[0].name, (r.x, r.y), backgroundcolor=color)

       # Save annotated image
       plt.imshow(image)
       plt.tight_layout(pad=0)
       outputfile = 'objects.jpg'
       fig.savefig(outputfile)
       print('  Results saved in', outputfile)
   ```

2. Save your changes and run the program once for each image file, observing detected objects in the output. View the `objects.jpg` file generated to see the annotated objects.

---

## **Detect and Locate People in an Image**

People detection identifies individuals within an image and their location using bounding boxes.

1. In the `AnalyzeImage` function, under the comment **Get people in the image**, add the following code:

   **C#**:
   ```csharp
   // Get people in the image
   if (result.People.Values.Count > 0)
   {
       Console.WriteLine($" People:");

       // Prepare image for drawing
       System.Drawing.Image image = System.Drawing.Image.FromFile(imageFile);
       Graphics graphics = Graphics.FromImage(image);
       Pen pen = new Pen(Color.Cyan, 3);
       Font font = new Font("Arial", 16);
       SolidBrush brush = new SolidBrush(Color.WhiteSmoke);

       foreach (DetectedPerson person in result.People.Values)
       {
           // Draw object bounding box
           var r = person.BoundingBox;
           Rectangle rect = new Rectangle(r.X, r.Y, r.Width, r.Height);
           graphics.DrawRectangle(pen, rect);
       }

       // Save annotated image
       String output_file = "persons.jpg";
       image.Save(output_file);
       Console.WriteLine("  Results saved in " + output_file + "\n");
   }
   ```

   **Python**:
   ```python
   # Get people in the image
   if result.people is not None:
       print("\nPeople in image:")

       # Prepare image for drawing
       image = Image.open(image_filename)
       fig = plt.figure(figsize=(image.width/100, image.height/100))
       plt.axis('off')
       draw = ImageDraw.Draw(image)
       color = 'cyan'

       for detected_people in result.people.list:
           # Draw object bounding box
           r = detected_people.bounding_box
           bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
           draw.rectangle(bounding_box, outline=color, width=3)

       # Save annotated image
       plt.imshow(image)
       plt.tight_layout(pad=0)
       outputfile = 'people.jpg'
       fig.savefig(outputfile)
       print('  Results saved in', outputfile)
   ```

2. Save your changes and run the program for each image in the folder, viewing the `people.jpg` file generated to see detected individuals.

---

## **Remove the Background or Generate a Foreground Matte of an Image**

1. In your code file, find the `BackgroundForeground` function; under the comment **Remove the background from the image or generate a foreground matte**, add the following code:

   **C#**:
   ```csharp
   // Remove the background from the image or generate a foreground matte
   Console.WriteLine($" Background removal:");
   string apiVersion = "2023-02-01-preview";
   string mode = "backgroundRemoval"; // Can be "foregroundMatting" or "backgroundRemoval"

   string url = $"computervision/imageanalysis:segment?api-version={apiVersion}&mode={mode}";

   using (var client = new HttpClient())
   {
       var contentType = new MediaTypeWithQualityHeaderValue("application/json");
       client.BaseAddress = new Uri(endpoint);
       client.DefaultRequestHeaders.Accept.Add(contentType);
       client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);

       var data = new
       {
           url = $"https://github.com/MicrosoftLearning/mslearn-ai-vision/blob/main/Labfiles/01-analyze-images/Python/image-analysis/{imageFile}?raw=true"
       };

       var jsonData = JsonSerializer.Serialize(data);
       var contentData = new StringContent(jsonData, Encoding.UTF8, contentType);
       var response = await client.PostAsync(url, contentData);

       if (response.IsSuccessStatusCode) {
           File.WriteAllBytes("background.png", response.Content.ReadAsByteArrayAsync().Result);
           Console.WriteLine("  Results saved in background.png\n");
       }
       else
       {
           Console.WriteLine($"API error: {response.ReasonPhrase} - Check your body url, key, and endpoint.");
       }
   }
   ```

   **Python**:
   ```python
   # Remove the background from the image or generate a foreground matte
   print('\nRemoving background from image...')

   url = "{}computervision/imageanalysis:segment?api-version={}&mode={}".format(endpoint, api_version, mode)

   headers= {
       "Ocp-Apim-Subscription-Key": key, 
       "Content-Type": "application/json" 
   }

   image_url="https://github.com/MicrosoftLearning/mslearn-ai-vision/blob/main/Labfiles/01-analyze-images/Python/image-analysis/{}?raw=true".format(image_file)  

   body = {
       "url": image_url,
   }

   response = requests.post(url, headers=headers, json=body)

   image=response.content
   with open("background.png", "wb") as file:
       file.write(image)
   print('  Results saved in background.png \n')
   ```

2. Save your changes and run the program for each image in the `images` folder, observing the background removal results in `background.png`.

3. To generate a foreground matte, change the `mode` variable to **foregroundMatting** in the `BackgroundForeground` function.

4. Save your changes and run the program for each image, viewing `background.png` generated with the new settings.

---

## **Clean Up Resources**

If you're not using the Azure resources created in this lab for other training modules, delete them to avoid incurring further charges:

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in.
2. Search for

 **Azure AI services multi-service account**, select the resource created in this lab, and follow the steps to delete it.

For more information on using Azure AI Vision, refer to the [Azure AI Vision documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/).

---
