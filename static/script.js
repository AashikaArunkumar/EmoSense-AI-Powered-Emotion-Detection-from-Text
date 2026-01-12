function predictEmotion() {
    const text = document.getElementById("textInput").value;
    const result = document.getElementById("resultText");

    if (text.trim() === "") {
        result.innerText = "Please enter some text";
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        result.innerText = "Emotion: " + data.emotion;
    })
    .catch(error => {
        result.innerText = "Server error";
        console.error(error);
    });
}
