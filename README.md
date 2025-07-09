# Spotify Track & Artist Analyzer

![Screenshot of the App]("photo.png")
A desktop application built with Python and PySimpleGUI that uses the Spotify API to search for artists and retrieve detailed information about their top tracks, including popularity, duration, and audio features.

This project was developed as an exercise in API integration, GUI development, and handling concurrent operations to ensure a responsive user experience.

---

## ✨ Features

* **Responsive GUI:** Built with PySimpleGUI, using `threading` to run slow network operations in the background, preventing the interface from freezing.
* **Secure API Authentication:** Uses `python-dotenv` to handle API credentials securely and a `subprocess` call to `curl` for robust authentication.
* **Artist Search:** Fetches detailed artist information including genres, popularity, and follower count.
* **Top Tracks Analysis:** Retrieves an artist's top 10 tracks and displays key data like album, popularity, and duration.
* **Audio Feature Retrieval:** Gathers advanced audio features for the top tracks (though not yet displayed in the current GUI version, the logic is implemented).
* **Real-time Feedback:** A status bar keeps the user informed about the progress of API calls.

---

## 🛠️ Technologies & Concepts

* **Python 3**
* **PySimpleGUI:** For the entire graphical user interface.
* **Requests & HTTPX:** For making robust HTTP requests to the Spotify API.
* **Threading:** To manage concurrency and ensure a non-blocking, responsive UI.
* **Subprocess:** To execute `curl` as a workaround for potential environment-specific network issues.
* **REST APIs & JSON:** Consuming and parsing data from the Spotify Web API.
* **Dotenv:** For secure management of environment variables and API credentials.

---

## 🚀 How to Run

1.  **Clone the repository.**
2.  **Create your credentials file:** Create a file named `.env` in the root directory and add your credentials:
    ```
    SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID_HERE
    SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
    ```
3.  **Create and activate a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
    *On Windows, use: `.\venv\Scripts\activate`*
4.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
5.  **Run the application!**
    ```sh
    python main_gui.py
    ```