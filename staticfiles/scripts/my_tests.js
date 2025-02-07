
function openTest(pin_hash, test_order, test_done) {
    if (test_done === 'True') {
        window.location.href = `/test_history/${pin_hash}/${test_order}/`;
    } else {
        Swal.fire({
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        fetch('/delete_session/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            if (response.ok) {
                Swal.close();
                window.location.href = `/test/${pin_hash}/${test_order}/1/`;
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Chyba',
                    text: 'Nastala chyba pri spracovaní požiadavky. Skúste to prosím znova.',
                    confirmButtonText: 'OK'
                });
            }
        }).catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Chyba',
                text: 'Nastala chyba pri spracovaní požiadavky. Skúste to prosím znova.',
                confirmButtonText: 'OK'
            });
        });
    }
}

function setProgressBarPercentage(percentage) {
  const progressBar = document.getElementById('myProgressBar');
  progressBar.style.width = `${percentage}%`;
}

setProgressBarPercentage(percentage);