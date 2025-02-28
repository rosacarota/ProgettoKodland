document.addEventListener("DOMContentLoaded", function () {
    let currentQuestionIndex = 0;
    let questions = [];
    let selectedAnswers = {};

    // Elementi HTML
    const questionTitle = document.getElementById("question-title");
    const answerList = document.getElementById("answer-list");
    const prevBtn = document.getElementById("prev-btn");
    const nextBtn = document.getElementById("next-btn");
    const endQuizBtn = document.getElementById("end-quiz-btn");

    // Carica le domande dal server
    function loadQuestions() {
        fetch("/api/get_questions")
            .then(response => response.json())
            .then(data => {
                questions = data;
                if (questions.length > 0) {
                    displayQuestion(0);
                }
            });
    }

    // Mostra una domanda nel carosello
    function displayQuestion(index) {
        let question = questions[index];
        questionTitle.textContent = question.testo;
        answerList.innerHTML = "";

        question.risposte.forEach(risposta => {
            let answerLi = document.createElement("li");
            answerLi.textContent = risposta.testo;
            answerLi.classList.add("list-group-item", "list-group-item-action");
            answerLi.style.cursor = "pointer";

            // Se la risposta è già stata selezionata, evidenziala
            if (selectedAnswers[question.id] === risposta.id) {
                answerLi.classList.add("active");
            }

            answerLi.onclick = () => selectAnswer(question.id, risposta.id, answerLi);
            answerList.appendChild(answerLi);
        });
    }

    // Seleziona una risposta
    function selectAnswer(questionId, answerId, element) {
        // Rimuove evidenziazione precedente
        Array.from(answerList.children).forEach(child => child.classList.remove("active"));
        element.classList.add("active");

        // Salva la risposta scelta
        selectedAnswers[questionId] = answerId;
    }

    // Navigazione domande
    function nextQuestion() {
        currentQuestionIndex = (currentQuestionIndex + 1) % questions.length; // Circolare
        displayQuestion(currentQuestionIndex);
    }

    function prevQuestion() {
        currentQuestionIndex = (currentQuestionIndex - 1 + questions.length) % questions.length; // Circolare
        displayQuestion(currentQuestionIndex);
    }

    // Termina quiz
    function endQuiz() {
        fetch("/api/submit_quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: selectedAnswers })
        })
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect; // Reindirizza alla pagina di congratulazioni
                }
            });
    }

    // Event listeners
    nextBtn.addEventListener("click", nextQuestion);
    prevBtn.addEventListener("click", prevQuestion);
    endQuizBtn.addEventListener("click", endQuiz);

    // Carica le domande all'avvio
    loadQuestions();
});
