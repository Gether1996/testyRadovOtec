function createStudents(course_pin) {
  Swal.fire({
    icon: 'question',
    title: 'Koľkých študentov si prajete vytvoriť?',
    input: 'number',
    inputAttributes: {
      min: 1
    },
    inputValue: 20,
    inputValidator: (value) => {
      if (!value) {
        return 'Prosím vyplňte počet študentov, aspoň jedného.';
      } else if (!/^\d+$/.test(value)) {
        return 'Prosím vložte iba číslice.';
      } else if (value < 1) {
        return 'Počet musí byť aspoň 1.';
      }
    },
    showCancelButton: true,
    confirmButtonText: 'Pokračovať',
    cancelButtonText: 'Zrušiť',
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'Vytváram študentov...',
        icon: 'info',
        allowOutsideClick: false,
        showCancelButton: false,
        showConfirmButton: false,
        didOpen: () => {
          Swal.showLoading();

          fetch("/create_students/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ course_pin: course_pin, number_of_students: result.value })
          })
            .then(response => response.json())
            .then(data => {
              if (data.status === 'success') {
                Swal.fire({
                  icon: 'success',
                  title: 'Noví študenti vytvorení',
                  timer: 1200,
                  showConfirmButton: false
                }).then(() => {
                  window.location.reload();
                });
              } else {
                Swal.fire({
                  icon: 'error',
                  title: data.message,
                  showCancelButton: false,
                  showConfirmButton: true,
                });
              }
            })
            .catch(error => {
              Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Something went wrong while creating the tests.',
                showCancelButton: false,
                showConfirmButton: true,
              });
            });
        }
      });
    }
  });
}

function deletePin(pin_id, pin_num) {
    Swal.fire({
        title: `Pozor, chystáte sa vymazať pin ${pin_num}, pokračovať?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Áno',
        cancelButtonText: 'Nie',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: 'success',
                title: 'Pin vymazaný',
                showConfirmButton: true,
                showCancelButton: false,
            }).then((result) => {
                if (result.isConfirmed || result.dismiss) {
                    window.location.reload();
                }
            });

            fetch('/delete_pin/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({pin_id: pin_id}),
            });
        }
    });
}


function openPDF(course_hash) {
  Swal.fire({
    allowOutsideClick: false,
    showCancelButton: false,
    showConfirmButton: false,
    didOpen: () => {
        Swal.showLoading();

        fetch('/open_pdf/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({course_hash: course_hash}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Swal.close();
                window.open(data.pdf_url, '_blank');
            } else {
                Swal.fire({
                    icon: 'error',
                    title: data.message,
                    showCancelButton: false,
                    showConfirmButton: true,
                });
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Something went wrong while creating the tests.',
                showCancelButton: false,
                showConfirmButton: true,
            });
        });
    }
  });
}

function adjustNameSurname(pin_id, pin_num, pin_name_previous) {
    Swal.fire({
        title: `Zadajte nové meno a priezvisko pre pin ${pin_num}`,
        input: 'text',
        inputValue: pin_name_previous !== 'None' ? pin_name_previous : '',
        inputPlaceholder: pin_name_previous === 'None' ? 'Nové meno a priezvisko' : '',
        showCancelButton: true,
        confirmButtonText: 'Uložiť',
        cancelButtonText: 'Zrušiť',
        preConfirm: (inputValue) => {
            if (!inputValue) {
                Swal.showValidationMessage('Meno a priezvisko nemôžu byť prázdne!');
                return false;
            }
            return inputValue;
        }
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: 'success',
                title: 'Meno a priezvisko zmenené',
                showConfirmButton: true,
                showCancelButton: false,
            }).then(() => {
                window.location.reload();
            });

            fetch('/change_name_surname_pin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ pin_id: pin_id, new_name: result.value }),
            });
        }
    });
}

function removeQueryStringAndReload() {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);
    params.delete('input_from_search');
    url.search = params.toString();
    window.location.href = url.toString();
}