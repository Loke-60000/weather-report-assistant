# Weather Report Assistant

### Overview

An AI-powered weather application that offers accurate and updated forecasts in both text and voice synthesis formats. This application is designed to collect, process, and store weather data, ensuring a personalized and user-friendly experience for its users.

### Features

- **Accurate Forecasts**: Receive up-to-date weather forecasts.
- **Text and Voice Synthesis**: Get weather information in your preferred format.
- **Data Handling**: Efficient collection, processing, and storage of weather data.
- **User Personalization**: Enjoy a tailored weather reporting experience.

### Data Collector

This component is responsible for fetching weather forecasts for a specified list of cities and storing the data in a PostgreSQL database. It can be executed manually or scheduled to run automatically using cron on Linux.

#### Manual Execution

Run the following command to manually execute the data collection script:

```bash
python collect.py
```

#### Scheduling with Cron

1. **Identify Your Conda Environment**

    ```bash
    conda env list | awk '{if ($1 != "#") print $2}'
    ```

2. **Edit Crontab**

    ```bash
    crontab -e
    ```

3. **Schedule the Script**

    Add the following line to schedule your script to run every 30 minutes. Replace `YOUR_CONDA_ENV` with your actual Conda environment name:

    ```bash
    */30 * * * * /home/lokman/anaconda3/envs/YOUR_CONDA_ENV/bin/python /path/to/collect.py
    ```

4. **Verify Cron Job**

    ```bash
    crontab -l
    ```

### NLP Module

Generates a weather report for a specified city from received data and converts it into an audio file in base64 format. Accessible through the API.

To run the NLP module:

```bash
python nlp.py
```

Navigate to the `nlp_weather` directory and execute the command above.

### HTTP Server

To initiate the HTTP server for the application:

```bash
python server.py
```

This starts the server, allowing for interaction with the application's front end.