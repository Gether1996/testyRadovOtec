function createNewCourse() {
  Swal.fire({
    title: 'Zadajte názov kurzu a dátum jeho začiatku',
    html: `
        <div class="column-container">
            <label for="course_name">Názov kurzu:</label>
            <input id="course_name" class="swal2-input">
            <br>
            <label for="starting_date">Začiatok:</label>
            <input id="starting_date" type="date" class="swal2-input">
        <div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Vytvoriť',
    cancelButtonText: 'Zrušiť',
    preConfirm: () => {
      var courseName = document.getElementById('course_name').value;
      var startingDate = document.getElementById('starting_date').value;

      if (!courseName || !startingDate) {
        Swal.showValidationMessage('Prosím vyplňte všetky polia');
        return false;
      }

      var today = new Date().toISOString().split('T')[0];
      if (startingDate < today) {
        Swal.showValidationMessage('Dátum začiatku nemôže byť v minulosti');
        return false;
      }

      return { courseName: courseName, startingDate: startingDate };
    }
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: 'Vytváram kurz...',
        icon: 'info',
        allowOutsideClick: false,
        showCancelButton: false,
        showConfirmButton: false,
        didOpen: () => {
          Swal.showLoading();

          fetch("/create_course/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ course_name: result.value.courseName, starting_date: result.value.startingDate })
          })
            .then(response => response.json())
            .then(data => {
              if (data.status === 'success') {
                Swal.fire({
                  icon: 'success',
                  title: 'Nový kurz vytvorený',
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
                showCancelButton: false,
                showConfirmButton: true,
              });
            });
        }
      });
    }
  });
}


function changeNameCourse(course_id, course_name, course_start) {
    Swal.fire({
        title: `Zadajte nový názov a dátum pre kurz ${course_name}`,
        html: `
            <div class="column-container">
                <label for="course_name">Názov kurzu:</label>
                <input id="course_name" class="swal2-input" value="${course_name}">
                <br>
                <label for="starting_date">Začiatok:</label>
                <input id="starting_date" type="date" class="swal2-input" value="${course_start}">
            <div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Uložiť',
        cancelButtonText: 'Zrušiť',
        preConfirm: () => {
          var courseName = document.getElementById('course_name').value;
          var startingDate = document.getElementById('starting_date').value;

          if (!courseName || !startingDate) {
            Swal.showValidationMessage('Prosím vyplňte všetky polia');
            return false;
          }

          var today = new Date().toISOString().split('T')[0];
          if (startingDate < today) {
            Swal.showValidationMessage('Dátum začiatku nemôže byť v minulosti');
            return false;
          }

          return { courseName: courseName, startingDate: startingDate };
        }
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: 'success',
                title: 'Názov a dátum zmenené',
                showConfirmButton: true,
                showCancelButton: false,
            }).then(() => {
                window.location.reload();
            });

            fetch('/change_name_start_course/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ course_id: course_id, new_name: result.value.courseName, new_start: result.value.startingDate })
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


//function createStudents(course_pin, course_name) {
//  Swal.fire({
//    icon: 'question',
//    title: `Koľkých študentov si prajete pridať do kurzu ${course_name}?`,
//    input: 'number',
//    inputAttributes: {
//      min: 1
//    },
//    inputValue: 1,
//    inputValidator: (value) => {
//      if (!value) {
//        return 'Prosím vyplňte počet študentov, aspoň jedného.';
//      } else if (!/^\d+$/.test(value)) {
//        return 'Prosím vložte iba číslice.';
//      } else if (value < 1) {
//        return 'Počet musí byť aspoň 1.';
//      }
//    },
//    showCancelButton: true,
//    confirmButtonText: 'Pokračovať',
//    cancelButtonText: 'Zrušiť',
//  }).then((result) => {
//    if (result.isConfirmed) {
//      Swal.fire({
//        title: 'Vytváram študentov...',
//        icon: 'info',
//        allowOutsideClick: false,
//        showCancelButton: false,
//        showConfirmButton: false,
//        didOpen: () => {
//          Swal.showLoading();
//
//          fetch("/create_students/", {
//            method: "POST",
//            headers: {
//              "Content-Type": "application/json",
//              'X-CSRFToken': csrfToken
//            },
//            body: JSON.stringify({ course_pin: course_pin, number_of_students: result.value })
//          })
//            .then(response => response.json())
//            .then(data => {
//              if (data.status === 'success') {
//                Swal.fire({
//                  icon: 'success',
//                  title: 'Noví študenti vytvorení',
//                  timer: 1200,
//                  showConfirmButton: false
//                }).then(() => {
//                  window.location.reload();
//                });
//              } else {
//                Swal.fire({
//                  icon: 'error',
//                  title: data.message,
//                  showCancelButton: false,
//                  showConfirmButton: true,
//                });
//              }
//            })
//            .catch(error => {
//              Swal.fire({
//                icon: 'error',
//                title: 'Error',
//                text: 'Something went wrong while creating the tests.',
//                showCancelButton: false,
//                showConfirmButton: true,
//              });
//            });
//        }
//      });
//    }
//  });
//}


function deleteCourse(course_id, course_name) {
    Swal.fire({
        title: `Pozor, chystáte sa vymazať kurz ${course_name}, pokračovať?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Áno',
        cancelButtonText: 'Nie',
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                icon: 'success',
                title: 'Kurz vymazaný',
                showConfirmButton: true,
                showCancelButton: false,
            }).then((result) => {
                if (result.isConfirmed || result.dismiss) {
                    window.location.reload();
                }
            });

            fetch('/delete_course/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({course_id: course_id}),
            });
        }
    });
}