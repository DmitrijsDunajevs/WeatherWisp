# WeatherWisp

WeatherWisp is a Python-based weather application built with CustomTkinter. It allows users to fetch weather and air quality data for a specified city and country, featuring dark mode, favorite countries, and a clean interface.


## Installation Steps

### 1. Install Python
1. Check if Python 3.8 or higher is installed:
   ```
   python --version
   ```
   If not installed, download and install Python from [python.org](https://www.python.org/downloads/).

2. Ensure `pip` is installed:
   ```
   pip --version
   ```
   If not, follow the instructions at [pip.pypa.io](https://pip.pypa.io/en/stable/installation/).

### 2. Download WeatherWisp
1. Clone or download this repository to your system:
   ```
   git clone https://github.com/DmitrijsDunajevs/WeatherWisp.git
   ```
   Or download the ZIP file and extract it.

2. Navigate to the project directory:
   ```
   cd weatherwisp
   ```

   The repository should include:
   - `main.py`: Main application script
   - `countries.py`: Dictionary mapping country names to codes
   - `icons/` folder: Contains icon files (`logo.ico`, `logo.png`, `about.png`, `settings.png`, `search.png`)

### 3. Install Required Libraries
Install the necessary Python libraries using `pip`:
```
pip install -r requirements.txt
```
- `customtkinter`: GUI framework
- `requests`: API calls to OpenWeatherMap
- `pillow`: Icon image handling
- `CTkToolTip`: Tooltip add-on

### 4. Obtain and Configure an OpenWeatherMap API Key
WeatherWisp uses the OpenWeatherMap API, requiring a valid API key.

1. **Sign Up**:
   - Visit [openweathermap.org](https://openweathermap.org/) and create a free account.
   - Verify your email address.

2. **Generate an API Key**:
   - Log in, go to "API keys" in your account dashboard.
   - Create a key (e.g., name it "WeatherWisp") and copy it (e.g., `abcd1234efgh5678`).

3. **Update the API Key in `main.py`**:
   - Open `main.py` in a text editor.
   - Find the line:
     ```
     self.api_key = "API_KEY"
     ```
   - Replace it with your API key:
     ```
     self.api_key = "abcd1234efgh5678"
     ```
   - Save the file.

### 5. Launch the Application
Run the app:
```
python main.py
```
The WeatherWisp window should open, showing the main interface.

## Troubleshooting
- **Error: "ModuleNotFoundError: No module named 'customtkinter'"**
  - Ensure you installed the libraries in Step 3. Run the `pip install` command again.
- **Weather Data Not Loading**
  - Check your internet connection.
  - Verify the API key in `main.py` (Step 4). If invalid, you’ll see "Error: Invalid API key." Generate a new key if needed.
- **Error: "FileNotFoundError: [Errno 2] No such file or directory: 'icons/logo.ico'"**
  - Ensure the `icons/` folder and all icon files are in the project directory.
