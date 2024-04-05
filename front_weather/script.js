document.getElementById("searchButton").addEventListener("click", function () {
  const city = document.getElementById("cityInput").value.trim();

  const url = "http://loknlp.eastus.azurecontainer.io:8000/chat";

  const payload = {
    message: "start:",
    city: city,
  };

  const headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
  };

  fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (!data || !data.weather_info || !data.response || !data.audio) {
        throw new Error("Missing essential data from the API response");
      }

      let weatherIcon = "❓";
      const responseLower = data.response.toLowerCase();
      if (
        responseLower.includes("rain") ||
        responseLower.includes("storm") ||
        responseLower.includes("shower") ||
        responseLower.includes("drizzle") ||
        responseLower.includes("thunder")
      ) {
        weatherIcon = "🌧️";
        weatherlabel = "Rain";
      } else if (responseLower.includes("cloud")) {
        weatherIcon = "☁️";
        weatherlabel = "Cloudy";
      } else if (
        responseLower.includes("sun") ||
        responseLower.includes("clear")
      ) {
        weatherIcon = "☀️";
        weatherlabel = "Sunny";
      }
      document.getElementById("weatherIcon").textContent = weatherIcon;

      document.getElementById("date").textContent =
        "Date: " + new Date().toLocaleDateString();
      document.getElementById("city").textContent = "City: " + city;
      const tempMatch = data.weather_info.match(/Temperature: ([\d.]+)°C/);

      document.getElementById("temperature").textContent = tempMatch
        ? "Temperature: " + tempMatch[1] + "°C"
        : "Temperature data not available";
      document.getElementById("weather").textContent = weatherlabel
        ? "Weather: " + weatherlabel
        : "Weather data not available";

      const audio = document.getElementById("audio");
      audio.src = "data:audio/wav;base64," + data.audio;
      audio.play();
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("temperature").textContent =
        "Error retrieving data";
      document.getElementById("weather").textContent = "Please try again";
      document.getElementById("audio").src = "";
    });
});
