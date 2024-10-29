This walkthrough focuses on demonstrating the core setup and deployment of an AVD environment in a business context, emphasizing key decisions and configurations for enterprise needs.

---

## **Azure Virtual Desktop Demo: Step-by-Step Setup**

### Step 1: Sign in to Azure Portal
1. Open a web browser and navigate to [https://portal.azure.com](https://portal.azure.com).
2. Sign in with your Azure account credentials that have permissions to create resources and manage Azure Active Directory (AD).

### Step 2: Create a Resource Group
1. In the Azure portal, go to **Resource Groups** and click on **Create**.
2. Configure the following settings:
   - **Subscription**: Choose the appropriate subscription.
   - **Resource Group**: Enter a unique name for your resource group (e.g., `AVD-Demo-RG`).
   - **Region**: Choose a region that is closest to your users or organization data center (e.g., **East US**).
3. Click **Review + Create** and then **Create**.

### Step 3: Set Up Azure Active Directory (AD) and Virtual Network
1. **Azure AD Tenant Connection**:
   - Ensure you have an **Azure AD Tenant** linked to your Azure subscription.
   - Confirm that your users are synced to Azure AD (via **AD Connect** or another synchronization tool).
2. **Create Virtual Network**:
   - Go to **Virtual networks** and click on **Create**.
   - Configure the network settings:
     - **Name**: Enter a name (e.g., `AVD-Demo-VNet`).
     - **Address range**: Define an address range (e.g., `10.0.0.0/16`).
     - **Subnet**: Add a subnet for AVD (e.g., `10.0.1.0/24`).
     - **Region**: Match the region of your resource group.
   - Click **Review + Create** and then **Create**.

### Step 4: Deploy Azure Virtual Desktop Host Pool
1. In the search bar, type **Azure Virtual Desktop** and select **Host pools** under Services.
2. Click on **Create** and configure the following:
   - **Resource Group**: Select the resource group you created earlier.
   - **Host Pool Name**: Enter a unique name (e.g., `AVD-Demo-HostPool`).
   - **Location**: Select the same region as your resource group.
   - **Host Pool Type**: Select **Pooled** (for shared desktops) or **Personal** (for dedicated desktops).
   - **Max session limit**: Define the maximum number of concurrent users (e.g., `5`).
3. Click **Next: Virtual Machines**.

### Step 5: Configure Session Hosts (Virtual Machines)
1. Choose **Add virtual machines** and configure the following:
   - **Virtual machine size**: Choose a VM size based on user needs (e.g., `Standard D2s_v3` for a balanced configuration).
   - **Number of VMs**: Enter the number of VMs you need (e.g., `2` for a small-scale demo).
   - **Image**: Choose the **Windows 10 Enterprise multi-session** image.
   - **Network**: Select the virtual network created in Step 3.
2. **Domain to Join**: Join the VMs to an **Active Directory** domain:
   - **Domain Name**: Enter your AD domain (e.g., `corp.contoso.com`).
   - **OU Path**: Optional - specify an organizational unit if required.
   - **Domain Admin Account**: Enter credentials to join the domain.
3. Configure **User Profile** using FSLogix:
   - **Enable FSLogix Profile Container** and provide a storage account or SMB file path for storing user profiles.
4. Click **Next: Workspace**.

### Step 6: Register with Azure Virtual Desktop Workspace
1. In the **Workspace** section, choose **Yes** to register the host pool with a workspace.
2. Select an existing workspace or create a new one:
   - **Workspace Name**: Enter a name for the workspace (e.g., `AVD-Demo-Workspace`).
3. Click **Review + Create**, review the settings, and then click **Create**.

### Step 7: Configure User Access
1. Go to the **Azure Virtual Desktop** page and select the **Applications** section under the workspace.
2. **Assign Application Groups**:
   - Choose the application group associated with your host pool.
   - Under **Assignments**, select **Add** and assign the necessary users or groups (e.g., add `BankofAmericaUserGroup`).
3. **Multi-Factor Authentication (Optional)**:
   - For additional security, configure MFA for users accessing AVD.

### Step 8: Test and Access Azure Virtual Desktop
1. Go to the **Azure Virtual Desktop** client at [https://rdweb.wvd.microsoft.com/webclient](https://rdweb.wvd.microsoft.com/webclient).
2. Sign in with a user account assigned to the host pool.
3. Launch the desktop or applications to verify access.

---

This demonstration setup will provide Bank of America technology leaders with a practical view of the steps and configuration options involved in deploying Azure Virtual Desktop. The demo covers essentials like network setup, VM configuration, and user access management, providing insight into how AVD supports secure, scalable, and flexible remote desktop solutions for large organizations.