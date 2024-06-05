# Trending Topics Scraper

This project is a web application built with Flask that scrapes trending topics from X.com (formerly known as Twitter) using Selenium, and stores them in MongoDB. The application then displays the trending topics on a webpage along with the timestamp, IP address, and a JSON extract of the MongoDB record.

## Features

- Scrapes trending topics from X.com using Selenium.
- Stores the trending topics in a MongoDB database.
- Displays the trending topics on a webpage with additional information.

## Prerequisites

- Python 3.x
- MongoDB Atlas account
- Google Chrome and ChromeDriver
- Git

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/samarthvashishta/TrendingOnX.git
    cd TrendingOnX
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/downloads) and place it in the project directory.

4. Update the MongoDB connection string and credentials in `app.py`:

    ```python
    client = MongoClient("mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<appName>")
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Click the "Get Trending Topics" button to scrape the trending topics from X.com. The results will be displayed on a new page with the timestamp, IP address, and JSON extract of the MongoDB record.

## Project Structure

- `app.py`: The main Flask application that handles scraping and displaying trending topics.
- `chromedriver.exe`: ChromeDriver executable for Selenium.
- `requirements.txt`: List of required Python packages.
- `templates/`: Directory containing HTML templates.

## HTML Templates

- `index.html`: The home page with a button to trigger the scraping.
- `trending.html`: The page that displays the trending topics and additional information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

