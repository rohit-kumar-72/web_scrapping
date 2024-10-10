# This project scrapes product information from the Noon website and saves the data into a CSV file.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd product-scraper
   ```

2. **Install the required libraries:**
   You can install the necessary packages using pip:
   ```bash
   pip install pandas
   pip install matplotlib
   pip install selenium
   ```

3. **Make sure you have Firefox browser ready else change the code at line no. 35 to**
   ```python
   driver = webdriver.Chrome()
   ```
   
## How to Run

1. Run the script using Python:
   ```bash
   python main.py
   ```

2. After the script runs, it will prompt you with options:
   - Enter `1` to get the most expensive product.
   - Enter `2` to get the cheapest product.
   - Enter `3` to see the number of products from each brand.
   - Enter `4` to exit.

3. The scraped data will be saved in a CSV file named `data.csv`.
```
