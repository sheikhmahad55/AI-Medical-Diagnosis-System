/*======================================
    AI Medical Diagnosis System
    Main JavaScript File
======================================*/

document.addEventListener("DOMContentLoaded", function () {

    initNavbar();

    initScrollTop();

    initSmoothScroll();

    initCurrentYear();

});





/*======================================
        Navbar Scroll Effect
======================================*/

function initNavbar() {

    const navbar = document.querySelector(".navbar");

    if (!navbar) return;

    window.addEventListener("scroll", function () {

        if (window.scrollY > 50) {

            navbar.classList.add("navbar-scrolled");

        } else {

            navbar.classList.remove("navbar-scrolled");

        }

    });

}





/*======================================
        Scroll To Top
======================================*/

function initScrollTop() {

    const button = document.getElementById("scrollTop");

    if (!button) return;

    window.addEventListener("scroll", function () {

        if (window.scrollY > 300) {

            button.style.display = "flex";

        }

        else {

            button.style.display = "none";

        }

    });

    button.addEventListener("click", function () {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}





/*======================================
        Smooth Scrolling
======================================*/

function initSmoothScroll() {

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({

                behavior: "smooth"

            });

        });

    });

}





/*======================================
        Footer Year
======================================*/

function initCurrentYear() {

    const year = new Date().getFullYear();

    document.querySelectorAll(".current-year").forEach(item => {

        item.textContent = year;

    });

}
/*======================================
    Diagnosis Form Logic
======================================*/

document.addEventListener("DOMContentLoaded", function () {

    initDiagnosisForm();

});

function initDiagnosisForm() {

    const form = document.getElementById("diagnosisForm");

    if (!form) return;

    const height = document.getElementById("height");
    const weight = document.getElementById("weight");
    const bmi = document.getElementById("bmi");

    if (height && weight && bmi) {

        height.addEventListener("input", calculateBMI);
        weight.addEventListener("input", calculateBMI);

    }

    form.addEventListener("submit", validateDiagnosisForm);
    document.getElementById("glucose")
    ?.addEventListener("input", updateHealthSummary);

    document.getElementById("bmi")
    ?.addEventListener("input", updateHealthSummary);

}
/*======================================
        BMI Calculator
======================================*/

function calculateBMI() {

    const height = parseFloat(document.getElementById("height").value);

    const weight = parseFloat(document.getElementById("weight").value);

    const bmi = document.getElementById("bmi");

    if (!height || !weight) {

        bmi.value = "";

        return;

    }

    const meter = height / 100;

    const result = (weight / (meter * meter)).toFixed(1);

    bmi.value = result;

    updateHealthSummary();

}

/*======================================
    Live Health Summary
======================================*/

function updateHealthSummary() {

    const bmi = parseFloat(document.getElementById("bmi")?.value) || 0;
    const glucose = parseFloat(document.getElementById("glucose")?.value) || 0;

    const bmiResult = document.getElementById("bmiResult");
    const healthStatus = document.getElementById("healthStatus");
    const riskBar = document.getElementById("riskBar");

    if (!bmiResult || !healthStatus || !riskBar) return;

    bmiResult.textContent = bmi.toFixed(1);

    let risk = 0;

    // BMI Score
    if (bmi >= 30) {
        risk += 40;
    } else if (bmi >= 25) {
        risk += 20;
    }

    // Glucose Score
    if (glucose >= 180) {
        risk += 60;
    } else if (glucose >= 140) {
        risk += 40;
    } else if (glucose >= 100) {
        risk += 20;
    }

    if (risk > 100) risk = 100;

    riskBar.style.width = risk + "%";
    riskBar.textContent = risk + "%";

    if (risk <= 30) {

        healthStatus.textContent = "Healthy";
        healthStatus.style.color = "#16A34A";

        riskBar.className =
        "progress-bar progress-bar-striped progress-bar-animated bg-success";

    }

    else if (risk <= 60) {

        healthStatus.textContent = "Moderate Risk";
        healthStatus.style.color = "#D97706";

        riskBar.className =
        "progress-bar progress-bar-striped progress-bar-animated bg-warning";

    }

    else {

        healthStatus.textContent = "High Risk";
        healthStatus.style.color = "#DC2626";

        riskBar.className =
        "progress-bar progress-bar-striped progress-bar-animated bg-danger";

    }

}

/*======================================
        Form Validation
======================================*/

function validateDiagnosisForm(event) {

    const age = parseInt(document.getElementById("age").value);

    if (age < 1 || age > 120) {

        alert("Please enter a valid age.");

        // event.preventDefault();
        return;

    }

    const requiredFields = [

        "pregnancies",
        "glucose",
        "bloodPressure",
        "skinThickness",
        "insulin",
        "bmi",
        "diabetesPedigree",
        "age"

    ];

    for (let field of requiredFields) {

        const input = document.getElementById(field);

        if (!input || input.value.trim() === "") {

            alert("Please fill all required fields.");

            input.focus();

            event.preventDefault();
            return;

        }

    }

    savePatientData();

    return true;

}

/*======================================
        AI Loading Screen
======================================*/

document.addEventListener("DOMContentLoaded", function () {

    initLoadingScreen();

});

function initLoadingScreen() {

    const loadingBar = document.getElementById("loadingBar");
    const loadingText = document.getElementById("loadingText");

    if (!loadingBar || !loadingText) return;

    const messages = [

        "Initializing AI Engine...",

        "Collecting Patient Data...",

        "Validating Medical Information...",

        "Running Machine Learning Model...",

        "Analyzing Diabetes Risk...",

        "Preparing Medical Report...",

        "Finalizing Prediction..."

    ];

    let progress = 0;
    let messageIndex = 0;

    const interval = setInterval(function () {

        progress++;

        loadingBar.style.width = progress + "%";
        loadingBar.innerHTML = progress + "%";

        if (
            progress % 15 === 0 &&
            messageIndex < messages.length - 1
        ) {

            messageIndex++;

            loadingText.innerHTML = messages[messageIndex];

        }

        if (progress >= 100) {

            clearInterval(interval);

            redirectToResult();

        }

    }, 50);

}

/*======================================
        Redirect Logic
======================================*/

function redirectToResult() {

    /*
    Later Flask will decide
    Positive or Negative result.
    */

    const prediction = localStorage.getItem("prediction");

    if (prediction === "positive") {

        window.location.href = "result-positive.html";

    }

    else if (prediction === "negative") {

        window.location.href = "result-negative.html";

    }

    else {

        /*
        Default page for frontend testing
        */

        window.location.href = "result-positive.html";

    }

}

/*======================================
        Fake Prediction
======================================*/

function generateFakePrediction() {

    const glucose = parseFloat(
        document.getElementById("glucose").value
    );

    if (glucose >= 140) {

        localStorage.setItem(
            "prediction",
            "positive"
        );

    }

    else {

        localStorage.setItem(
            "prediction",
            "negative"
        );

    }

}

/*======================================
        Save Patient Data
======================================*/

function savePatientData() {

    const patient = {

        name: document.getElementById("patientNameInput")?.value || "",

        age: document.getElementById("age")?.value || "",

        gender: document.getElementById("gender")?.value || "",

        height: document.getElementById("height")?.value || "",

        weight: document.getElementById("weight")?.value || "",

        bmi: document.getElementById("bmi")?.value || "",

        glucose: document.getElementById("glucose")?.value || "",

        bloodPressure: document.getElementById("bloodPressure")?.value || "",

        insulin: document.getElementById("insulin")?.value || "",

        pregnancies: document.getElementById("pregnancies")?.value || "",

        skinThickness: document.getElementById("skinThickness")?.value || "",

        diabetesPedigree: document.getElementById("diabetesPedigree")?.value || ""

    };

    localStorage.setItem(

        "patient",

        JSON.stringify(patient)

    );

}

/*======================================
        Load Patient Data
======================================*/

function loadPatientData() {

    const patient = JSON.parse(

        localStorage.getItem("patient")

    );

    if (!patient) return;

    setText("patientName", patient.name);

    setText("patientAge", patient.age);

    setText("patientGender", patient.gender);

    setText("patientBMI", patient.bmi);

    setText("patientGlucose", patient.glucose);

}

/*======================================
        Helper Function
======================================*/

function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {

        element.textContent = value;

    }

}

/*======================================
        Auto Load
======================================*/

document.addEventListener(

    "DOMContentLoaded",

    function () {

        loadPatientData();

    }

);
/*======================================
    Report Actions
======================================*/

document.addEventListener("DOMContentLoaded", function () {

    initReportActions();

});

function initReportActions() {

    const printBtn = document.getElementById("printReport");
    const pdfBtn = document.getElementById("downloadPDF");

    if (printBtn) {

        printBtn.addEventListener("click", function () {

            window.print();

        });

    }

    if (pdfBtn) {

        pdfBtn.addEventListener("click", function () {

            alert("PDF Download feature will be connected with Flask Backend.");

        });

    }

}
/*======================================
    Clear Form
======================================*/

function clearDiagnosisForm() {

    const form = document.getElementById("diagnosisForm");

    if (!form) return;

    form.reset();

    const bmi = document.getElementById("bmi");
    const bmiResult = document.getElementById("bmiResult");
    const healthStatus = document.getElementById("healthStatus");
    const riskBar = document.getElementById("riskBar");

    if (bmi) bmi.value = "";

    if (bmiResult) {

        bmiResult.textContent = "---";

    }

    if (healthStatus) {

        healthStatus.textContent = "Waiting...";

        healthStatus.style.color = "";

    }

    if (riskBar) {

        riskBar.style.width = "0%";

        riskBar.textContent = "0%";

        riskBar.className =
        "progress-bar progress-bar-striped progress-bar-animated";

    }

}
/*======================================
    Local Storage
======================================*/

function clearPatientData() {

    localStorage.removeItem("patient");

    localStorage.removeItem("prediction");

}
/*======================================
    Utility Functions
======================================*/

function getPatientData() {

    return JSON.parse(

        localStorage.getItem("patient")

    );

}

function getPrediction() {

    return localStorage.getItem(

        "prediction"

    );

}
/*======================================
    Final Initialization
======================================*/

document.addEventListener("DOMContentLoaded", function () {

    console.log("===================================");

    console.log("AI Medical Diagnosis System Loaded");

    console.log("Frontend Version 1.0");

    console.log("Ready For Flask Backend");

    console.log("===================================");

});
