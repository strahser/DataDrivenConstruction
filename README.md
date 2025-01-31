

# Data Analysis Streamlit App

This Streamlit application allows you to upload data, perform basic analysis, and visualize your data. It provides flexibility in how data can be loaded (from Excel files or converted from Revit files), and offers multi-page functionality for different types of analysis.

## Key Features

*   **Data Upload:**
    *   Supports uploading data from Excel (.xlsx) files.
    *   Provides an option to convert data from Revit files (.rvt) using a DDC converter.
        *   The user must provide the path to the DDC converter folder and the path to the Revit file.
*   **Multi-Page Functionality:** The app uses a multi-page structure for better navigation and organization.
    *   **Upload Page:** Handles uploading data from Excel files or conversion from Revit files. This is the initial page to load any data.
    *   **Complex Analysis Page:** Performs and displays a more detailed analysis of the uploaded data. Only visible if data has been uploaded.
    *   **Dynamic Analysis Page:** Allows user to perform dynamic (interactive) analysis of uploaded data.  Only visible if data has been uploaded.
*   **Data Visualization:** Displays:
    *   A preview of the uploaded data
    *   A detailed summary of column characteristics (Total values, missing values, top values, etc.)
    *   Structure of columns and their categories.
    *   Interactive histograms for numeric columns.
    *   Interactive bar charts for categorical columns.
*   **Language Support:** The interface language can be switched between English and Russian.
*   **Session State:** The app uses Streamlit session state to preserve data and selected options between page changes, as well as track language, data, selected columns etc.

## How to Run the App

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_folder>
    ```
    Replace `<repository_url>` and `<project_folder>` with your repository details.
2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    or pip install streamlit seaborn multipage-streamlit matplotlib openpyxl
    ```
    This will install all necessary Python packages (including `streamlit`, `seaborn`, and `matplotlib`). Make sure you have `requirements.txt`, if not, you can generate it using `pip freeze > requirements.txt`.
3.  **Run the Streamlit app:**

    ```bash
    streamlit run main.py
    ```
    Replace `main.py` if your main app script has another name.

4.  **Access the app:** Open the URL provided in the terminal in your web browser. Typically something like `http://localhost:8501`.

## Code Structure

*   **`main.py`:** Contains the main application logic, handles session state, multi-page setup, and language selection.
*   **`UploadPage.py`** (or equivalent file): Contains the logic for the data upload, data conversion, and visualisation functions.
*   **`ProfilingScript.py`** (or equivalent file): Contains the logic for the complex and dynamic data analysis pages.

## Session State Variables:

*   `df`: Stores the pandas DataFrame loaded from Excel or converted from Revit file.
*   `selected_columns`: Stores selected column names (used for analysis).
*   `LANGUAGE`: Stores the selected language for the UI ("EN" for English, "RU" for Russian).
*   `complex_analysis_selected_columns_widget`: stores selected columns from complex analysis page

## Data Loading

The app provides two main ways to load data:

1.  **Excel Files:** You can directly upload `.xlsx` Excel files using the file uploader on the "Upload" page.
2.  **Revit Conversion:** To load data from a Revit file, you need to:
    *   Select the "Revit Converter" option.
    *   Provide the path to the folder that contains the `RvtExporter.exe` file.
    *   Provide the path to your Revit file (`.rvt`).
    *   Click the "Convert Revit File" button to perform the conversion.

## Libraries Used

*   **Streamlit:** For creating the interactive web application.
*   **pandas:** For data manipulation and analysis.
*   **seaborn:** For statistical data visualization.
*   **matplotlib:** For creating basic plots.
*   **multipage_streamlit (or equivalent)**: A library to implement multi-page navigation, replace this with the correct library name if required.

## Further Information

This app provides a foundational framework for working with data. You can expand its capabilities by adding:
*   more complex data analysis functions.
*   more visualizations.
*   advanced filtering and sorting functionality.
*   file export functions.
*   custom data analysis tools.

---

This README should give new users a good understanding of how to use your app and how it is structured. Remember to adjust it based on the specific details of your project, such as the name of the multi-page library.