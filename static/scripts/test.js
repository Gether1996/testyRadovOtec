
function setProgressBarPercentage(percentage) {
  const progressBar = document.getElementById('myProgressBar');
  progressBar.style.width = `${percentage}%`;
}

setProgressBarPercentage(percentage);

function checkAnswer(question_id, picked_answer) {
    fetch('/check_answer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ question_id: question_id, picked_answer: picked_answer }),
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.status === "success" && !data.correct_answer) {
            nextQuestion();
        } else {
            let selectedButton = document.querySelector(`[onclick="checkAnswer('${question_id}', '${picked_answer}')"]`);
            const nextButton = document.getElementById('nextButton');
            const aQuestionButton = document.getElementById('question-a');
            const bQuestionButton = document.getElementById('question-b');
            const cQuestionButton = document.getElementById('question-c');
            nextButton.classList.remove('initially-hidden');
            aQuestionButton.disabled = true;
            bQuestionButton.disabled = true;
            cQuestionButton.disabled = true;

            if (selectedButton) {
                selectedButton.style.backgroundColor = '#ff5252';
            }

            let correctButton = document.querySelector(`[onclick="checkAnswer('${question_id}', '${data.correct_answer}')"]`);
            console.log("Correct Button:", correctButton);

            if (correctButton) {
                correctButton.style.backgroundColor = '#5bc75b';
            }
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        Swal.fire({
            icon: 'error',
            title: 'Chyba',
            text: 'Nastala chyba pri ukladaní odpovede. Skúste to prosím znova.',
            confirmButtonText: 'OK'
        });
    });
}

var buttons = document.querySelectorAll('button');
document.addEventListener('click', (event) => {
  var clickedButton = event.target;
  if (clickedButton.tagName === 'BUTTON' && clickedButton.classList.contains('question-select-button')) {
    var clickedButtonId = clickedButton.id;

    var questionButtons = Array.from(buttons).filter(button => button.classList.contains('question-select-button'));
    questionButtons.forEach(button => {
      button.style.backgroundColor = 'white';
    });

    clickedButton.style.backgroundColor = 'grey';
  }
});

function nextQuestion() {
    window.location.reload();
}

document.addEventListener('keydown', function(event) {
  var key = event.key.toLowerCase(); // Get the pressed key in lowercase
  var buttonId = `question-${key}`; // Construct the button ID based on the key

  var button = document.getElementById(buttonId);
  if (button) {
    button.click();
  }
});

function cancelTestConfirmation() {
    window.location.href = '/';
}

document.addEventListener("DOMContentLoaded", function () {
    window.scrollTo(0, 0);
    let fontSizeLabel = document.getElementById("fontSizeLabel");
    let decreaseButton = document.getElementById("decreaseFontSize");
    let increaseButton = document.getElementById("increaseFontSize");

    function updateFontSize(newSize) {
        document.querySelectorAll(".question-select-button, .test-question-header, .cancel-test-button, .next-question-button").forEach(el => {
            el.style.fontSize = newSize + "px";
        });
        fetch(`save_font_size/${newSize}/`, { method: "GET" })
            .then(response => console.log(`Font size ${newSize} saved.`))
            .catch(error => console.error("Error saving font size:", error));
    }

    decreaseButton.addEventListener("click", function () {
        if (currentFontSize > 10) {
            currentFontSize -= 2;
            updateFontSize(currentFontSize);
        }
    });

    increaseButton.addEventListener("click", function () {
        if (currentFontSize < 40) {
            currentFontSize += 2;
            updateFontSize(currentFontSize);
        }
    });
});