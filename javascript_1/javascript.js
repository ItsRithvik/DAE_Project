document.addEventListener("DOMContentLoaded", function () {
    const yearElement = document.getElementById("year");
    if (yearElement) {
        yearElement.innerText = new Date().getFullYear();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const value = document.getElementById("value");
    const risk = document.getElementById("risk");
    const rec = document.getElementById("rec");
    
    if (value && risk && rec) {
        const x = parseFloat(value.textContent) || 0;
        const y = parseFloat(risk.textContent) || 0;
        const result = (x * (100-y));
        if (result > 0) {
            rec.textContent = result.toFixed(2);
        } else {
            rec.textContent = 0.00
        }
    }
});
