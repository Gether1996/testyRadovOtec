
function setProgressBarPercentage(percentage) {
  const progressBar = document.getElementById('myProgressBar');
  progressBar.style.width = `${percentage}%`;
}

setProgressBarPercentage(percentage);

function checkCorrect(question_id, picked_answer) {
    fetch('/check_correct/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ question_id: question_id, picked_answer: picked_answer }),
    }).then(response => {
        if (response.ok) {





            nextQuestion(question_num);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Chyba',
                text: 'Nastala chyba pri ukladaní odpovede. Skúste to prosím znova.',
                confirmButtonText: 'OK'
            });
        }
    }).catch(() => {
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

function prevQuestion(question_num) {
    if (question_num > 1) {
        window.location.href = `/test/${question_num -1}/`;
    }
}

function nextQuestion(question_num) {
    if (question_num < 40) {
        setTimeout(() => {
            window.location.href = `/test/${question_num +1}/`;
        }, 50);
    }

    if (question_num === 40) {
        setTimeout(() => {
            window.location.reload();
        }, 50);
    }
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