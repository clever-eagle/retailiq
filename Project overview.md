#### Project Title:
# RetailIQ: AI-Driven Sales Forecasting and Market Basket Analysis System

# **1. Project Description / Purpose / Target Users**

RetailIQ is a data-driven retail analytics web application designed to help retail businesses make smarter, faster, and more informed decisions using their existing sales and transaction data. The platform is built for retail managers, business analysts, and small-to-medium-sized retailers who want to gain insights without needing advanced data science skills. By offering easy-to-use tools and powerful AI modules, **RetailIQ** transforms raw data into practical business strategies.
## Its core functionalities are:

1. **Sales Forecasting:**
   Predicts future sales for individual products or categories based on historical data. This assists businesses in planning inventory, managing supply chains, optimizing staffing, and setting realistic financial goals.

2. **Market Basket Analysis (MBA):**
   Detects patterns in customer purchasing behavior by identifying frequently bought-together items. This insight is useful for creating bundles, improving cross-selling strategies, and optimizing shelf layouts or online product recommendations.

In essence, RetailIQ serves as an AI-powered assistant for retailers, converting everyday sales data into actionable intelligence that drives better decision-making across inventory, marketing operations, and sales strategy.

---
# **2. Overall Application Workflow for RetailIQ**

The core idea of RetailIQ is to empower retail businesses with AI-driven insights for sales forecasting and market basket analysis, all accessible through a web-based dashboard built with a **React frontend and a Node.js backend, which communicates with a Python AI/ML service.**

---
## 1. User Access & Initial Setup (Frontend & Backend)

*   **User Interaction (Frontend - React App):**
    *   The user (e.g., retail manager) navigates to the RetailIQ web application URL, served by the **React frontend**.
    *   If authentication is implemented (optional), the user logs in (handled by **Node.js backend**).
*   **Backend Preparation:**
    *   The primary backend (**Node.js with Express.js**) is running, ready to receive requests from the React frontend.
    *   The **Python AI/ML backend (Flask/FastAPI)** is also running as a separate service, ready to receive requests from the Node.js backend.
    *   Database (**MongoDB** connected to Node.js; optionally SQLite for Python if needed for temporary local storage) is accessible.

---

## 2. Data Ingestion & Preparation (Detailed Workflow)

This section details the crucial first steps where the user provides their data and the system prepares it for the AI/ML engines. This is a common prerequisite for all core features of RetailIQ (Sales Forecasting and Market Basket Analysis).

---
### A. User Interaction (Frontend - React App)

The goal here is to provide a simple and intuitive way for the user to get their retail data into the RetailIQ system.

1.  **Navigate to Data Upload:**
    *   The user, typically a retail manager, accesses a clearly marked section in the **React web application's** user interface.
    *   **UI Element:** This is often a "Data Upload," "Import Data," or "Manage Dataset" option in a persistent sidebar menu or a prominent button on a welcome/dashboard page, built using **React components**.

2.  **File Selection & Upload Mechanism:**
    *   **UI Element:** A standard file uploader widget (e.g., a custom React component using `<input type="file">` or a library like `react-dropzone`).
    *   **Supported Formats:** The system is designed to accept common structured data formats:
        *   **CSV (Comma Separated Values):** A plain text file where data is separated by commas.
        *   **Excel (``.xlsx`` or ``.xls``):** Microsoft Excel spreadsheet files. The system might need to allow users to specify which sheet to use if multiple sheets exist.
    *   **Data Structure Expectation:** The uploaded file should ideally contain historical sales and transaction data. A typical structure, as per the blueprint's example, would be a table with columns like:
        *   `Product`: Name or ID of the product. (Categorical/Text)
        *   `Date`: Date of the sale/transaction. (Datetime)
        *   `Units Sold`: Quantity of the product sold in that transaction/day. (Numeric)
        *   `Price`: Unit price of the product at the time of sale. (Numeric)
        *   `Category`: Product category (e.g., Fruit, Electronics). (Categorical/Text)
        *   *Required for MBA:* `TransactionID` or `OrderID`: An identifier to group items bought together in a single purchase.
    *   **User Guidance:** The UI should ideally provide clear instructions on the expected file format, required columns, and an example snippet or template.

3.  **Initiate and Confirm Upload:**
    *   **UI Element:** An "Upload" or "Submit" button in the **React UI**.
    *   **Feedback:** Once the user selects a file and clicks upload, the **React UI** should provide feedback handled by **React state updates**:
        *   A loading spinner or progress bar during the file transfer.
        *   A success message upon completion or an error message if the upload fails (e.g., wrong file type, file too large if limits are set).
    *   The file is sent from the **React frontend to the Node.js backend API**.
    *   **Single vs. Multiple Files:** The blueprint mentions "CSV or Excel," implying one primary dataset at a time. For simplicity, a single comprehensive file is the starting point.

---

### B. Data Processing (Backend - Node.js orchestrating Python, pandas)

Once the file is received by the **Node.js backend API endpoint**, it's typically forwarded to the Python AI/ML service for heavy lifting.

1.  **File Reception (Node.js & Python):**
    *   The **Node.js backend API endpoint** receives the file from the React frontend (e.g., using `multer` for Express.js).
    *   The Node.js backend then **forwards this file** (or its content) to a specific endpoint on the **Python (Flask/FastAPI) AI/ML backend**.
    *   The **Python backend API endpoint** receives the raw file bytes.
    *   **Libraries (Python):** `pandas` is the primary tool here.
        *   `pd.read_csv()` for CSV files.
        *   `pd.read_excel()` for Excel files (may need to specify sheet name).
    *   The raw data is loaded into a pandas DataFrame in the Python service.

2.  **Data Validation (Initial Check - Python):**
    *   Performed by the Python service.
    *   **Essential Columns:** Check if critical columns (e.g., 'Date', 'Product', 'Units Sold', 'TransactionID' for MBA) are present. If not, an error is returned (via Node.js) to the user.
    *   **Data Types (Basic):** Attempt to infer data types. Log warnings if, for instance, 'Units Sold' cannot be converted to a numeric type or 'Date' to datetime.
    *   **File Integrity:** Basic checks like ensuring the file is not empty.

3.  **Data Cleaning & Preprocessing (Python):**
    *   This is often an iterative process. Handled by functions likely in `utils.py` or specific preprocessing sections within the Python service's modules (`forecast.py`, `basket.py`).
    *   **Handling Missing Values (NaNs):**
        *   **Strategy:** Depending on the column and context (e.g., fill with 0, mean/median, 'Unknown', or drop rows).
    *   **Data Type Conversion (Robust):**
        *   `Date`: Ensure conversion to `datetime` objects (e.g., `pd.to_datetime()`).
        *   `Units Sold`, `Price`: Convert to numeric types.
        *   `Product`, `Category`: Ensure string/object types.
    *   **Removing Duplicates:** Check for and remove entire duplicate rows.
    *   **Outlier Handling (Optional but Recommended):**
        *   For `Units Sold` or `Price`, using methods like capping or statistical removal.
    *   **Text Normalization (for `Product`, `Category`):**
        *   Convert to consistent case, remove whitespace, standardize variations.

4.  **Feature Engineering & Transformation (Python - Tailored for specific modules):**
    *   The cleaned DataFrame in the Python service is transformed.
    *   **For Sales Forecasting (e.g., using Prophet):**
        *   **Column Renaming:** 'Date' to 'ds', 'Units Sold' to 'y'.
        *   **Aggregation:** Aggregate to consistent frequency (e.g., daily).
        *   **Filtering:** Based on user selection.
    *   **For Market Basket Analysis (e.g., using Apriori):**
        *   **Transactional Format:** Transform the DataFrame into a list of transactions, where each transaction is a list of items (products) grouped by `TransactionID`.
        *   **One-Hot Encoding:** If needed by `mlxtend`.

5.  **Data Storage/Access for Analysis Modules (Python Service & Node.js):**
    *   **In-Memory (Python Service):** The processed pandas DataFrames (original cleaned data, forecast-ready data, MBA-ready transactional data) are typically held in memory within the Python backend process for the duration of the analysis task.
    *   **Temporary Storage (Python Service - Optional):** For very large datasets that exceed memory capacity for a single request or if intermediate results need to be cached within the Python service, SQLite could be used.
    *   **Data for Node.js/React:** The Python service doesn't directly use frontend session state. Once an analysis is complete, the *results* (e.g., forecast data, association rules, typically as JSON) are sent back to the Node.js backend. The Node.js backend then forwards these results to the React frontend. The React frontend manages its own state (e.g., using Context API, Redux, or Zustand) to store these results for display.
    *   **Module Access:**
        *   When a user triggers an analysis from the **React UI**, the request goes to the **Node.js backend**.
        *   The Node.js backend calls the appropriate **Python AI/ML service API endpoint** (e.g., `/forecast`, `/associations`), passing necessary parameters. The Python service will use the data that was uploaded and processed in a prior step (it might maintain a short-lived reference to this data, possibly keyed by a temporary ID or session context managed by the Node.js layer if needed for complex multi-step operations, though often the data is re-retrieved or assumed to be available for the current request flow).
        *   The Python service uses the relevant preprocessed DataFrame and passes it to the respective AI engine function.

By the end of this phase, the raw data provided by the user has been cleaned, validated, transformed by the Python service, and is ready to be fed into the specialized AI/ML models for generating insights.

---

## 3. Feature-Specific Workflows

### A. Sales Forecasting Workflow

*   **User Interaction (Frontend - React):**
    1.  **Select Analysis:** User selects "Sales Forecasting" from the analysis options in the **React UI**.
    2.  **Set Parameters:** User chooses the timeframe for the forecast and potentially selects specific products/categories in the **React UI**.
    3.  **Initiate Forecast:** User clicks a "Generate Forecast" button in **React**.
    4.  **Feedback:** The **React UI** shows a loading indicator or progress message.
*   **Backend Processing (Node.js orchestrating Python Sales Forecast Engine):**
    1.  **API Request:** **React frontend** sends a request to the **Node.js backend API's** forecasting endpoint (e.g., `/api/forecast`), including the parameters.
    2.  **Orchestration & Engine Invocation:** The **Node.js backend** validates the request and then forwards it to the **Python AI/ML backend's** forecasting endpoint (e.g., `/forecast` in `forecast.py`).
    3.  **Model Application (Python):**
        *   The Python engine retrieves the preprocessed historical sales data (likely the time-series aggregated data).
        *   It applies the chosen forecasting algorithm (Prophet).
        *   It generates future sales predictions.
    4.  **Result Aggregation (Python):** The Python engine prepares the forecast results (e.g., JSON data for graphs, summary statistics).
*   **Output Display (Frontend - React):**
    1.  **Receive Results:** The **React frontend** receives the forecast data (as JSON) from the **Node.js backend API**.
    2.  **Display Forecast:** "Sales forecasts appear." **React components** render this using:
        *   Visualizations (e.g., graphs via Plotly.js showing historical trend and future forecast).
        *   Data tables with predicted values.
    3.  **Download Option:** User can download the forecast results (e.g., as CSV/Excel), facilitated by the backend.

### B. Market Basket Analysis (MBA) Workflow

*   **User Interaction (Frontend - React):**
    1.  **Select Analysis:** User selects "Market Basket Analysis" in the **React UI**.
    2.  **Set Parameters (Optional):** User might set thresholds like minimum support or confidence via **React UI**.
    3.  **Initiate Analysis:** User clicks a "Find Item Associations" button in **React**.
    4.  **Feedback:** **React UI** shows a loading indicator.
*   **Backend Processing (Node.js orchestrating Python Market Basket Module):**
    1.  **API Request:** **React frontend** sends a request to the **Node.js backend API's** MBA endpoint (e.g., `/api/mba`).
    2.  **Orchestration & Engine Invocation:** The **Node.js backend** routes the request to the **Python AI/ML backend's** Market Basket Module (e.g., `/associations` in `basket.py`).
    3.  **Data Preparation (Python):** The Python module uses the preprocessed *transactional data* (list of transactions/items).
    4.  **Algorithm Application (Python):** It applies the Apriori algorithm to:
        *   Identify frequent itemsets.
        *   Generate association rules.
    5.  **Result Aggregation (Python):** The Python engine prepares the discovered rules and itemsets (JSON).
*   **Output Display (Frontend - React):**
    1.  **Receive Results:** **React frontend** receives the MBA results from the **Node.js backend**.
    2.  **Display Associations:** "Bundles or rules are generated." **React components** display:
        *   A table or list of association rules with metrics (support, confidence, lift).
        *   Suggestions for product bundles or cross-selling based on the rules.
        *   Potentially a network graph visualizing item associations (advanced).
    3.  **Download Option:** User can download rules/itemsets.

# **3. Tech Stack (MERN + Python Hybrid Approach)**

This section outlines the technologies, libraries, and models for building RetailIQ using a hybrid architecture: a MERN stack for the primary web application and user interface, and a Python stack for the specialized AI/Machine Learning computations.

---

**I. Web Application Layer (MERN Stack)**

*   **Frontend Technologies (Client-Side):**
    *   **Core Framework:** React.js
        *   A JavaScript library for building user interfaces, enabling dynamic and responsive components.
    *   **Key React Ecosystem Libraries:**
        *   **State Management:** Zustand or React Context API (for managing application state; Redux is powerful but potentially overkill for this scope).
        *   **Routing:** React Router (for client-side navigation).
        *   **HTTP Client:** Axios or Fetch API (for making requests to the Node.js backend).
        *   **UI Component Libraries (Recommended):** Material-UI (MUI), Ant Design, Chakra UI (for pre-built components, saving significant development time).
    *   **Visualization Libraries (JavaScript-based):**
        *   Plotly.js, Recharts, Chart.js, Nivo, or Victory (Plotly.js is good for time series and can render complex charts).

*   **Backend Technologies - Web API (Server-Side):**
    *   **Core Framework:** Node.js with Express.js
        *   **Node.js:** A JavaScript runtime environment for building server-side applications.
        *   **Express.js:** A minimal and flexible Node.js web application framework, used to build the primary API that the React frontend interacts with. This API will handle user authentication, data validation, and orchestrating calls to the Python AI/ML backend.
    *   **Core Language:** JavaScript (or TypeScript for enhanced type safety).

*   **Databases (Primarily for MERN Stack):**
    *   **Primary Application Database:** MongoDB
        *   A NoSQL, document-oriented database. Well-suited for flexibility and often used with the MERN stack. Will store user accounts, application settings, references to uploaded data files, and job statuses.
        *   **ODM (Object Data Mapper):** Mongoose (for modeling application data for MongoDB in Node.js).

*   **Authentication (Handled by Node.js/Express.js):**
    *   **Libraries/Strategies:** Passport.js (for authentication middleware) with a local strategy, JSON Web Tokens (JWT) for sessionless authentication.

---

**II. AI/Machine Learning Processing Layer (Python Stack)**

*   **Backend Technologies - AI/ML Services (Server-Side):**
    *   **API Framework:** Flask or FastAPI (Python)
        *   This will be a *separate* backend service dedicated to AI/ML tasks. It will expose its own API endpoints (e.g., `/forecast`, `/associations`) that the Node.js/Express.js backend will call.
        *   **Flask:** Lightweight and simple for creating ML model APIs.
        *   **FastAPI:** Modern, high-performance, with automatic data validation and API docs, ideal for robust ML service deployment. (Recommended for robustness).
    *   **Core Language:** Python

*   **Key Data Science Libraries & Tools (Python AI/ML Backend):**
    *   **General Data Handling & Numerics:**
        *   `pandas`: For data manipulation and analysis (DataFrames) of the retail data.
        *   `NumPy`: For numerical operations.
    *   **Sales Forecasting Module:**
        *   `prophet` (by Meta): Primary library for forecasting time series data.
        *   `scikit-learn` (Optional, for simple baseline models or feature engineering).
    *   **Market Basket Analysis Module:**
        *   `mlxtend.frequent_patterns`: For Apriori algorithm and association rule mining.

*   **Databases (Primarily for Python AI/ML Backend, if needed beyond in-memory processing):**
    *   **Local/Development/Caching:** SQLite (for temporary storage or simple persistence if Python services need to retain data between requests).
    *   *Note: The Python services will primarily receive data via API calls from the Node.js backend and process it in memory. Direct access to the MongoDB instance by Python is possible but less common in this decoupled architecture; data sharing usually happens via the Node.js intermediary.*

---

**III. General Tools & Cross-Cutting Concerns**

*   **API Testing (Development Tool):**
    *   Postman or Insomnia: For testing REST APIs of both the Node.js/Express.js backend and the Python AI/ML backend.
*   **Communication Protocol:**
    *   HTTP/REST: For communication between React Frontend <-> Node.js Backend, and Node.js Backend <-> Python AI/ML Backend.

---

**IV. ML/AI Models Involved (Executed in the Python AI/ML Backend)**

*   **Sales Forecasting:**
    *   **Prophet:** A robust time-series forecasting model.
*   **Market Basket Analysis:**
    *   **Apriori Algorithm:** For association rule learning.

# **4. Platform & Usage**

This section details the platforms RetailIQ will operate on, how users will interact with it, the necessary runtime environments, and the resources required for its development, deployment, and ongoing usage.

*   **Platforms Supported:**
    *   **Primary Platform:** Web Application (built with React).
    *   RetailIQ will be accessible through modern web browsers (e.g., Google Chrome, Mozilla Firefox, Microsoft Edge, Safari) on desktop and laptop computers. While it might be viewable on mobile browsers, the interface will be optimized for desktop use, which is more suitable for data analysis tasks.

*   **How the App is Used Once Completed:**
    1.  **Access:** Users (retail managers, analysts) will navigate to the deployed web application URL (serving the **React application**).
    2.  **(Optional) Authentication:** If implemented, users will log in with their credentials (handled by the **Node.js backend**).
    3.  **Data Upload:** Users will upload their historical sales and transaction data (including TransactionID for MBA), typically in CSV or Excel format, through a designated upload interface in the **React UI**. The data is sent to the **Node.js backend**, which then forwards it to the **Python AI/ML service** for processing.
    4.  **Module Selection:** Users will choose one of the core analysis modules (Sales Forecasting or Market Basket Analysis) in the **React UI**.
    5.  **Parameter Configuration:** Depending on the module, users may adjust parameters (e.g., forecast period, product selection, MBA thresholds) in the **React UI**.
    6.  **Analysis Execution:** Users will initiate the analysis. The request is sent from the **React frontend to the Node.js backend**, which then calls the appropriate **Python AI/ML service**. Results are generated by Python and returned via Node.js.
    7.  **Results Visualization & Interpretation:** The **React frontend** will display the results through interactive charts (using JavaScript libraries), data tables, and textual summaries.
    8.  **Download (Optional):** Users may have the option to download generated reports, forecast data, or association rules, facilitated by the backend systems.

*   **Runtime Requirements:**
    *   **User-Side (Client):**
        *   A modern web browser with JavaScript enabled.
        *   A stable internet connection.
    *   **Server-Side (Hosting Environment for Deployment):**
        *   **Node.js Application Server (MERN Backend):**
            *   Node.js runtime environment (e.g., v18.x or later recommended).
            *   Access to a MongoDB instance.
        *   **Python AI/ML Service (Python Backend):**
            *   Python runtime environment (e.g., Python 3.8 - 3.11).
            *   Installed Python libraries as specified in the Tech Stack.
            *   Sufficient CPU and RAM to handle data processing and model inference. CPU-only instances are expected for free-tier deployment.

*   **Resources Required for:**

    *   **Development:**
        *   **Software & Tools:**
            *   **IDE:** VS Code (recommended).
            *   **Version Control:** Git and a GitHub repository.
            *   **Node.js & npm/yarn:** For MERN stack development.
            *   **React Developer Tools (browser extension).**
            *   **Python & pip/conda:** For AI/ML backend development.
            *   **MongoDB:** Local installation or a free tier cloud instance (e.g., MongoDB Atlas M0).
            *   **API Testing Tool:** Postman or Insomnia.
            *   **Web Browsers.**
            *   **Communication Tools:** Slack, Discord, or WhatsApp.
            *   **Documentation Tools:** Google Docs, Markdown editor.
        *   **Hardware:**
            *   **Individual Laptops/PCs.**
            *   **GPU Access (Helpful for Initial Model Experimentation):**
                *   **Lab GPUs:** NVIDIA 1060, 1660, or 2060 (useful for quickly testing model performance characteristics, though Prophet is mostly CPU-bound).
                *   **Cloud GPU (Free Tiers - Backup/Supplementary):** Google Colab, Kaggle Kernels, AWS SageMaker Studio Lab.

    *   **Deployment (Aiming for Free/Student Tiers):**
        *   **Frontend (React App):**
            *   **Platforms:** Netlify, Vercel, GitHub Pages (static hosting).
        *   **Backend - Node.js API (Express.js):**
            *   **Platforms:** Render.com, Fly.io, Railway.app, Heroku (if student program available).
        *   **Backend - Python AI/ML API (Flask/FastAPI):**
            *   **Platforms:** Similar to Node.js backend: Render.com, Fly.io, Railway.app, Heroku.
            *   **Important Note for Python Backend:** Free tiers typically provide CPU-only instances with limited RAM. Efficient data processing (`pandas` practices) and CPU-friendly models (Prophet, Apriori) are crucial.
        *   **Database (MongoDB):**
            *   **Platform:** MongoDB Atlas (M0 "Shared" cluster).
        *   **Domain Name (Optional):** Use free subdomains provided by hosting platforms.

    *   **Usage (by End-Users & System Load):**
        *   **End-User Side:** Standard desktop/laptop, internet.
        *   **Application Server Side (Impact on Deployed Resources):**
            *   **CPU Load:**
                *   Node.js backend: Low to moderate (mostly routing and data forwarding).
                *   Python AI/ML backend: Can be significant during data loading, preprocessing, and model execution.
            *   **Memory (RAM):**
                *   Python backend will be most memory-intensive due to holding DataFrames in memory. Dataset size limitations imposed by free-tier RAM are the main constraint.
            *   **Storage:**
                *   Application code: Minimal.
                *   User-uploaded data: Processed in-memory/temporarily in Python service; not stored long-term in MongoDB.
                *   MongoDB: User accounts, metadata about analysis runs (optional). Modest needs for M0 tier.
            *   **Network Bandwidth:** Dependent on data size and analysis result size. Free tiers usually sufficient for moderate data.

# **5. Data Flow**

This section outlines the path data takes through the RetailIQ system, from initial input by the user to the final output of analytical insights.

*   **Expected Input:**
    *   **Primary Input:** User-uploaded data files.
        *   **Format:** CSV or Excel (``.xlsx``, ``.xls``).
        *   **Content:** Historical sales and transaction data.
        *   **Key Expected Columns:** `Product`, `Date`, `Units Sold`, `Price`, `Category`, `TransactionID` (Required for MBA).
    *   **User Parameters (via UI):**
        *   For Sales Forecasting: Forecast period, specific products/categories.
        *   For Market Basket Analysis: Minimum support, confidence, lift thresholds.

*   **Expected Output:**
    The system will generate insights and visualizations tailored to each core module:
    *   **Sales Forecasting:**
        *   **Visualizations:** Interactive line charts (e.g., via Plotly.js in React).
        *   **Data Tables:** Predicted sales figures.
        *   **Downloadable Reports:** CSV/Excel of forecast.
    *   **Market Basket Analysis:**
        *   **Data Tables:** Association rules with metrics.
        *   **Textual Insights:** Suggestions for bundles, cross-selling based on rules.
        *   **Visualizations (Optional):** Network graphs of item relationships.
        *   **Downloadable Reports:** CSV/Excel of rules/itemsets.

*   **Data Storage and Retrieval Process:**
    1.  **Data Upload:**
        *   The user uploads a CSV/Excel file via the **React frontend**.
        *   The file is sent to the **Node.js/Express.js backend**.
        *   The Node.js backend may perform initial validation and then **forwards the file to the Python (Flask/FastAPI) AI/ML backend**.
    2.  **Data Processing (Python Backend):**
        *   The Python backend receives the raw file.
        *   `pandas` is used to parse, clean, preprocess, and transform the data into forms suitable for Forecasting and MBA.
    3.  **In-Session Data Management (Python Backend):**
        *   The processed and module-specific DataFrames are primarily held in memory (RAM) within the Python backend process for the duration of the analysis task or related sequence of requests. For larger data or complex flows, temporary storage (like SQLite) might be used within the Python service.
    4.  **AI/ML Model Application (Python Backend):**
        *   The relevant AI/ML model (Prophet or Apriori) is applied to the appropriate preprocessed DataFrame in the Python service's memory.
    5.  **Results Generation & Transfer:**
        *   The Python backend generates results (predictions, rules) typically in JSON format.
        *   These results are sent back to the **Node.js backend**.
        *   The Node.js backend relays these results to the **React frontend**.
    6.  **Frontend Display:**
        *   The **React frontend** receives the JSON data and uses it to populate charts (using JavaScript libraries like Plotly.js), tables, and other UI elements within **React components**.
    7.  **Application Data Storage (MongoDB):**
        *   MongoDB, connected to the **Node.js backend**, will primarily store:
            *   User accounts and authentication details (if implemented).
            *   Application settings or user preferences.
            *   Potentially metadata about uploaded files or saved analysis configurations. The raw voluminous sales data itself is transient for processing within the Python service, or stored temporarily in the Python service's environment (e.g., SQLite).
    8.  **Downloads:**
        *   If the user requests a download from the **React UI**, the Python backend can generate a CSV/Excel file from the results, which is then streamed through the Node.js backend to the user's browser.

---

# **6. Development Plan**

This plan outlines the project's development in distinct phases, with estimated time allocations considering a 4-5 month timeline, approximately 2 hours of coding on regular days, and one dedicated project day per week (assuming ~15 effective team hours per week for the core team).

*   **Phased Development Outline & Estimated Time Allocation:**

    *   **Phase 1: Planning and Design (Weeks 1-3; Approx. 45 team hours)**
        *   **Activities:**
            *   Detailed requirements gathering and finalization of the two core features (Sales Forecasting, MBA).
            *   Creation of user stories for these features.
            *   Finalize UI/UX wireframes and mockups for key screens (Data Upload, Forecasting, MBA results) using React components.
            *   Define API contracts (endpoints, request/response formats) between:
                *   React Frontend <-> Node.js Backend
                *   Node.js Backend <-> Python AI/ML Backend
            *   Design MongoDB schema for application data (user accounts, settings).
            *   Set up Git repository, development environments (Node.js, Python, MongoDB).
            *   Initial PoC for core ML models (Prophet, Apriori) with sample data.
        *   **Team Focus:** All team members involved. MERN-focused members lead UI/API design. ML-inclined members focus on PoCs. Beginners can assist with initial documentation or environment setup.

    *   **Phase 2: Core Frontend & Backend Structure (Weeks 4-8; Approx. 75 team hours)**
        *   **Frontend (React):**
            *   Develop main application layout, navigation (React Router), basic styling.
            *   Implement user authentication components (if included), connecting to Node.js.
            *   Build the data upload component in React and logic to send files to Node.js.
            *   Create reusable React UI components for displaying data tables and basic charts.
            *   Set up React state management (e.g., Zustand).
            *   Develop placeholder components for Forecasting and MBA screens.
        *   **Backend (Node.js/Express.js):**
            *   Set up Express server, API structure, basic middleware (body-parser, cors).
            *   Implement API endpoints for user authentication.
            *   Implement API endpoint for receiving file uploads from React (using `multer`).
            *   Basic MongoDB integration (Mongoose schemas, connection, user models).
            *   Define initial API endpoints that will call the Python service (e.g., `/api/forecast`, `/api/mba`) with placeholder logic.
        *   **Team Focus:** MERN members lead. Beginners assist with basic React components, styling, or simple Node.js routes/middleware.

    *   **Phase 3: AI/ML Module Development & Backend Integration (Weeks 9-15; Approx. 80 team hours)**
        *   **Python AI/ML Backend (Flask/FastAPI):**
            *   Develop the robust data ingestion and preprocessing pipeline for uploaded sales data (parsing CSV/Excel, cleaning, validation, transformation for both Forecasting and MBA).
            *   Implement the Sales Forecasting module using Prophet.
            *   Implement the Market Basket Analysis module using Apriori from `mlxtend`.
            *   Develop API endpoints for each AI function (e.g., `/forecast`, `/associations`) within the Python service.
            *   Utilize lab GPU access for initial model experimentation/tuning if needed, but Prophet is largely CPU-bound. Focus on ensuring CPU-efficient inference.
        *   **Node.js Backend Integration:**
            *   Implement logic in Node.js/Express.js endpoints (`/api/forecast`, `/api/mba`) to make HTTP requests (using Axios or Node-fetch) to the corresponding Python AI/ML API endpoints (`/forecast`, `/associations`).
            *   Handle sending preprocessed data (or a reference to it) to Python and receiving results (JSON) back from Python.
            *   Implement error handling for communication between Node.js and Python.
        *   **Frontend Integration (React):**
            *   Connect React components for the Forecasting and MBA screens to trigger calls to the respective **Node.js backend APIs**.
            *   Handle asynchronous responses and display loading states.
            *   Integrate JavaScript visualization libraries (e.js., Plotly.js) in React components to dynamically render graphs (forecast plots, MBA relationship graphs if attempted) based on data received from the backend.
            *   Display data tables with results (predicted values, association rules).
        *   **Team Focus:** ML-inclined members spearhead Python development. MERN devs focus on Node.js orchestration (calling Python APIs) and connecting React frontend to these Node.js APIs, as well as integrating visualization libraries. Beginners can help with testing specific API endpoints or preparing diverse test data.

    *   **Phase 4: Testing, Refinement, and Debugging (Weeks 16-17; Approx. 30 team hours)**
        *   **Activities:**
            *   Unit testing for critical functions in Node.js and Python backends, and React components.
            *   Integration testing of the entire workflows (React -> Node.js -> Python -> Node.js -> React) for both Forecasting and MBA.
            *   User Acceptance Testing (UAT) with sample datasets.
            *   Address bugs, performance bottlenecks, particularly in the Python data processing and model inference stages.
            *   Refine UI/UX based on testing feedback.
            *   Implement download functionality for results.
        *   **Team Focus:** All team members participate. Beginners can focus heavily on manual testing and reporting bugs.

    *   **Phase 5: Deployment and Documentation (Week 18; Approx. 15 team hours)**
        *   **Activities:**
            *   Prepare frontend (React) and backend applications (Node.js, Python) for deployment.
            *   Configure environment variables, deployment scripts for free-tier PaaS.
            *   Deploy all components (React to Netlify/Vercel; Node.js & Python to Render/Fly.io; MongoDB to Atlas) and perform final testing on deployed versions.
            *   Finalize project documentation (user manual, technical docs, API documentation, project report).
            *   Prepare project presentation/demo.
        *   **Team Focus:** MERN members likely lead deployment configuration and execution. All contribute to documentation/presentation.

*Note: This timeline is an estimate. The total estimated hours for the core development team are approximately 245 (45 + 75 + 80 + 30 + 15). Regular weekly reviews and flexible task assignment are essential.*