
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
    let menu = document.getElementById("font-size-menu");
    let fontSizeButton = document.getElementById('changeFontSizeButton');

    for (let size = 10; size <= 40; size += 2) {
        let listItem = document.createElement("li");
        let link = document.createElement("a");
        link.className = "dropdown-item";
        link.href = "#";
        link.textContent = size + "px";
        link.dataset.size = size;

        link.addEventListener("click", function (event) {
            event.preventDefault();
            let chosenSize = this.dataset.size;

            // Apply font size to buttons
            document.querySelectorAll(".question-select-button").forEach(button => {
                button.style.fontSize = chosenSize + "px";
            });

            // Update button text to show selected size
            fontSizeButton.textContent = `Veľkosť textu (${chosenSize}px)`;

            // Send GET request to save font size
            fetch(`save_font_size/${chosenSize}/`, { method: "GET" })
                .then(response => console.log(`Font size ${chosenSize} saved.`))
                .catch(error => console.error("Error saving font size:", error));
        });

        listItem.appendChild(link);
        menu.appendChild(listItem);
    }
});
