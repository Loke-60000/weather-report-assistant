const url = "http://loknlp.eastus.azurecontainer.io:8000/chat";

const payload = {
  message: "start:",
  city: "Paris",
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
    console.log("Response:", data); 
  })
  .catch((error) => {
    console.error("Error:", error); 
  });
