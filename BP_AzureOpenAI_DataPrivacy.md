# Azure Open AI Data Privacy

If you choose to submit client data "as is" without scrubbing or anonymizing, Azure OpenAI Service provides specific protections to maintain data privacy, but there are important considerations and limitations regarding data access, usage, and retention.

### 1. **Data Access and Use for Model Training**
   - **Data Usage for Training**: **Azure OpenAI Service does not use your data to train or improve the public GPT models** (such as GPT-4, GPT-3.5) provided by OpenAI or Microsoft. Your data is only used to generate responses during the session, and Microsoft explicitly states that customer data is not used for training or fine-tuning models.
   - **Isolation of Data**: The data you submit to the Azure OpenAI instance is processed in a **tenant-isolated environment**, which means your data is not shared across clients. This isolation ensures that the data you submit is only accessible within your Azure subscription and instance.

### 2. **Data Privacy and Availability to Other Users**
   - **Response Isolation**: Data you provide to Azure OpenAI is processed for your requests only. **It will not appear in responses to other users’ prompts** and is not accessible by other Azure OpenAI clients or users.
   - **No Data Retention for Future Sessions**: Azure OpenAI processes data on a request-by-request basis. Once a request is processed, **Azure does not retain the data for future requests** and does not use it to influence responses to other clients.

### 3. **Data Handling and Retention Policies**
   - **Data Retention**: Microsoft has implemented policies that ensure customer input data is retained only temporarily for processing each request and is then discarded. For enterprise customers, data retention is minimal and designed to satisfy enterprise data privacy and compliance standards.
   - **Log and Monitoring Data**: Microsoft may collect some metadata (like usage logs) for operational purposes, but this does not include customer-specific data submitted in prompts. The metadata is stored in compliance with Microsoft’s data handling policies and relevant compliance standards.

### 4. **Potential Internal Access by Microsoft**
   - **Limited Access for Operations and Support**: Microsoft’s operations and support personnel may have access to service-level metadata (e.g., logs for monitoring service health) but not to your prompt data content. For troubleshooting, Microsoft has strict access control policies and auditing in place to ensure data access is restricted and monitored.
   - **Compliance with Regulatory Standards**: Microsoft’s Azure OpenAI Service is designed to comply with major regulatory standards (such as GDPR, CCPA, SOC, HIPAA). These regulations enforce strict data privacy, requiring Microsoft to secure and limit access to customer data and follow detailed protocols around data handling and retention.

### 5. **Implications of Sending Raw Client Data Without Scrubbing**
   - **Sensitive Data Risks**: Submitting raw, un-scrubbed client data does introduce potential risks, especially if the data contains sensitive information. Even though Microsoft does not use this data for model training or share it, sending sensitive data (PII, financial information, etc.) without scrubbing could still be exposed to risks if there’s a breach, misconfiguration, or human error.
   - **Data Protection Best Practices**: While Microsoft provides strong safeguards, it’s best practice to scrub sensitive data before sending it to any third-party service, including Azure OpenAI. Anonymizing or minimizing data reduces exposure risk in case of any unforeseen access.

### 6. **Control of Data Within Your Azure Environment**
   - By using Azure OpenAI Service, you have **full control over the data pipeline and architecture within your Azure environment**. This means that data processing, storage, and handling (prior to sending to OpenAI) can be controlled through Azure’s robust security and data governance features, ensuring that even if un-scrubbed data is used, it’s managed according to your organization’s security policies.

### Conclusion

In summary:
- **Your data is not used to train the public GPT models** and is not retained for use in responses to other clients.
- Microsoft ensures **tenant isolation** and controls to keep customer data private within your Azure instance, and data is not accessible to other users or clients.
- **Operational metadata** is collected for monitoring, but prompt content is discarded after processing.

If un-scrubbed data must be submitted, consider implementing additional internal access controls and data governance measures within Azure, such as using **Azure Key Vault** or **Azure Private Link** to enhance data security and protect sensitive data during processing. However, anonymizing or aggregating sensitive data remains a best practice for added privacy.