// static/js/chat.js

document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("themeToggle");
    const body = document.body;

    // Load theme from localStorage
    const savedTheme = localStorage.getItem("chat-theme") || "light-theme";
    body.classList.add(savedTheme);

    themeToggle.addEventListener("click", function () {
        if (body.classList.contains("light-theme")) {
            body.classList.remove("light-theme");
            body.classList.add("dark-theme");
            localStorage.setItem("chat-theme", "dark-theme");
        } else {
            body.classList.remove("dark-theme");
            body.classList.add("light-theme");
            localStorage.setItem("chat-theme", "light-theme");
        }
    });

    // Auto-scroll to bottom of chat
    const chatBox = document.querySelector(".chat-box");
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
