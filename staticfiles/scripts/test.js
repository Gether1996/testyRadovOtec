
function setProgressBarPercentage(percentage) {
  const progressBar = document.getElementById('myProgressBar');
  progressBar.style.width = `${percentage}%`;
}

setProgressBarPercentage(percentage);


function saveToSession(question_id, picked_answer) {
    fetch('/save_progress_into_session/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ question_id: question_id, picked_answer: picked_answer }),
    }).then(response => {
        if (response.ok) {
            nextQuestion(hash, test_num, question_num);
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

function prevQuestion(hash, test_num, question_num) {
    if (question_num > 1) {
        window.location.href = `/test/${hash}/${test_num}/${question_num -1}/`;
    }
}

function nextQuestion(hash, test_num, question_num) {
    if (question_num < 40) {
        setTimeout(() => {
            window.location.href = `/test/${hash}/${test_num}/${question_num +1}/`;
        }, 50);
    }

    if (question_num === 40) {
        setTimeout(() => {
            window.location.reload();
        }, 50);
    }
}

document.addEventListener('keydown', handleKeyPress);
function handleKeyPress(event) {
  var keyCode = event.keyCode;
  if (keyCode === 37) {
    prevQuestion(hash, test_num, question_num);
  } else if (keyCode === 39) {
    nextQuestion(hash, test_num, question_num);
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
    Swal.fire({
        icon: 'warning',
        text: `Chystáte sa ukončiť test, Váš doterajší postup sa neuloží, pokračovať?`,
        confirmButtonText: 'Ukončiť test',
        showCancelButton: true,
        cancelButtonText: 'Zrušiť',
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/my_tests/${hash}/`;
        }
    });
}

var countdown = document.getElementById('countdown');
var futureTime = timer;
let targetDate = new Date(futureTime);

function updateCountdown() {
    var now = new Date();
    var difference = targetDate.getTime() - now.getTime();

    if (difference <= 0) {
        countdown.textContent = "Čas vypršal!";
        clearInterval(intervalId);
        finishTest(hash, test_num);
        return;
    }

    var seconds = Math.floor((difference / 1000) % 60);
    var minutes = Math.floor((difference / (1000 * 60)) % 60);

    var formattedTime = `Zostávajúci čas: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    countdown.textContent = formattedTime;
}

var intervalId = setInterval(updateCountdown, 1000);
updateCountdown();

function finishTestQuestion(hash, test_num) {
    Swal.fire({
        icon: 'question',
        text: `Chystáte sa vyhodnotiť test, pokračovať?`,
        confirmButtonText: 'Pokračovať',
        showCancelButton: true,
        cancelButtonText: 'Zrušiť',
    }).then((result) => {
        if (result.isConfirmed) {
            finishTest(hash, test_num);
        }
    });
}

function finishTest(hash, test_num) {
  Swal.fire({
    title: 'Vyhodnocujem test...',
    allowOutsideClick: false,
    showCancelButton: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();

      fetch('/finish_test/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ hash: hash, test_num: test_num }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          var points = data.points;
          var accomplished = points >= 64 ? 'Úspešne dokončený!' : 'Neúspešný test.';
          Swal.fire({
            icon: 'success',
            title: `Test ukončený<br><br>Dosiahnuté body: ${points}/80<br>${accomplished}`,
            confirmButtonText: 'OK',
            showCancelButton: false,
          }).then((result) => {
            if (result.isConfirmed || result.dismiss === Swal.DismissReason.cancel || result.dismiss === Swal.DismissReason.close) {
              window.location.href = `/test_history/${hash}/${test_num}/`;
            }
          });
        } else {
          Swal.fire({
            icon: 'error',
            title: 'wrong request',
            showConfirmButton: true,
          });
        }
      })
      .catch(error => {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Something went wrong while finishing the test.',
          showConfirmButton: true,
        });
      });
    }
  });
}