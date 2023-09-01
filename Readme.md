# Financial Times

This Financial Times scraper is designed to extract data from Financial Times website. Follow the steps below to set up and run the scraper.

## Prerequisites

Before you begin, make sure you have the following software installed on your system:

- Python (version 3.6 or higher)
- pip (Python package manager)

## Getting Started

1. Clone this repository to your local machine:

   ```shell
   git clone <repository_url>
   cd <repository_name>

2. Create a virtual environment
    ```shell
   python -m venv venv

3. Activate the virtual environment:
    ```shell
   source venv/bin/activate

4. Install the required packages from the requirements.txt file:
    ```shell
   pip install -r requirements.txt

## Getting Started

1. Navigate to the spiders directory:
    ```shell
   cd financial_times/financial_times/spiders/

2. To run the scraper, use the following command:
    ```shell
   scrapy crawl FinancialTimesScraper

3. The scraped data will be saved in output.json file

