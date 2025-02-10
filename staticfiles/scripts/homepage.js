//function login() {
//    var pin = document.getElementById('login_pin').value;
//
//    if (!pin) {
//        Swal.fire({
//            icon: 'error',
//            title: 'PIN je povinný údaj',
//            showCancelButton: false,
//            showConfirmButton: true,
//        });
//        return false;
//    } else if (!isDigit(pin)) {
//        Swal.fire({
//          icon: 'error',
//          title: 'PIN musí obsahovať iba číslice',
//          showCancelButton: false,
//          showConfirmButton: true,
//        });
//        return false;
//    } else if (pin.length !== 8) {
//        Swal.fire({
//            icon: 'error',
//            title: 'PIN musí mať 8 znakov',
//            showCancelButton: false,
//            showConfirmButton: true,
//        });
//        return false;
//    }
//
//    fetch("/login_with_pin/", {
//        method: "POST",
//        headers: {
//          "Content-Type": "application/json",
//          'X-CSRFToken': csrfToken
//        },
//        body: JSON.stringify({
//          pin,
//        }),
//    })
//    .then(response => response.json())
//    .then(data => {
//        console.log(data);
//      if (data.status === 'success') {
//        window.location.href = `/my_tests/${data.hash}/`;
//      } else {
//          Swal.fire({
//            icon: 'error',
//            title: 'Nesprávny PIN',
//            showCancelButton: false,
//            showConfirmButton: true,
//          });
//      }
//    })
//}

//function isDigit(str) {
//  for (var i = 0; i < str.length; i++) {
//    var charCode = str.charCodeAt(i);
//    if (charCode < 48 || charCode > 57) {
//      return false;
//    }
//  }
//  return true;
//}
//
//document.addEventListener("DOMContentLoaded", function() {
//    const pinInput = document.getElementById("login_pin");
//    pinInput.focus();
//
//    pinInput.addEventListener("keypress", function(event) {
//        if (event.key === "Enter") {
//            login();
//        }
//    });
//});

function createTest() {
  Swal.fire({
    icon: 'question',
    title: 'Ak máte rozpracovaný test, vymaže sa, pokračovať?',
    showCancelButton: true,
    confirmButtonText: 'Pokračovať',
    cancelButtonText: 'Zrušiť',
  }).then((result) => {
    if (result.isConfirmed) {

      Swal.fire({
        title: 'Vytváram test...',
        icon: 'info',
        allowOutsideClick: false,
        showCancelButton: false,
        showConfirmButton: false,
        didOpen: () => {
          Swal.showLoading();

          fetch("/create_test/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': csrfToken
            }
          })
            .then(response => response.json())
            .then(data => {
              Swal.close();
              if (data.status === 'success') {
                window.location.href = `/test/`;
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

function continueInTest() {
  Swal.fire({
    allowOutsideClick: false,
    showCancelButton: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading();

      fetch("/continue_test/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': csrfToken
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            Swal.fire({
                icon: 'question',
                title: `Zodpovedaných ${data.progress} z celkových ${data.max} otázok, pokračovať?`,
                showCancelButton: true,
                confirmButtonText: 'Pokračovať',
                cancelButtonText: 'Zrušiť',
              }).then((result) => {
                  if (result.isConfirmed) {
                    window.location.href = `/test/`;
                  }
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

//function showPinModal(data) {
//  Swal.fire({
//    icon: 'success',
//    html: `
//      <div style="font-size: 20px; margin-bottom: 15px;">Váš pin kód na prihlásenie:</div>
//      <div style="font-size: 24px; font-weight: bold; margin-bottom: 15px;">${data.pin}</div>
//      <button id="copy-button" class="swal2-confirm swal2-styled" style="margin: 5px; background-color: #2c3e50;">Skopírovať PIN</button>
//      <button id="email-button" class="swal2-confirm swal2-styled" style="margin: 5px; background-color: #2c3e50;">Poslať na email</button>
//    `,
//    showCancelButton: false,
//    showConfirmButton: true,
//    confirmButtonText: 'Zatvoriť',
//    didOpen: () => {
//      document.getElementById('copy-button').addEventListener('click', () => {
//        navigator.clipboard.writeText(data.pin).then(() => {
//          alert('Pin skopírovaný');
//        });
//      });
//
//      document.getElementById('email-button').addEventListener('click', () => {
//        Swal.fire({
//          title: 'Zadajte Váš email',
//          input: 'email',
//          inputPlaceholder: 'email',
//          inputValidator: (value) => {
//            var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//            if (!emailPattern.test(value)) {
//              return 'Prosím zadajte email v správnom tvare';
//            }
//          },
//          showCancelButton: true,
//          confirmButtonText: 'Odoslať'
//        }).then((result) => {
//          if (result.isConfirmed) {
//            var email = result.value;
//
//            Swal.fire({
//              icon: 'success',
//              title: 'Email s pinom odoslaný',
//              timer: 1500,
//              showConfirmButton: false
//            }).then(() => {
//              window.location.href = `/my_tests/${data.pin_hash}/`;
//            });
//
//            fetch('/send_email/', {
//              method: 'POST',
//              headers: {
//                "Content-Type": "application/json",
//                'X-CSRFToken': csrfToken
//              },
//              body: JSON.stringify({ pin_hash: data.pin_hash, email: email })
//            }).catch((error) => {
//              console.error('Error sending email:', error);
//            });
//          }
//        });
//      });
//    }
//  }).then((result) => {
//    if (result.isConfirmed || result.dismiss) {
//      window.location.href = `/my_tests/${data.pin_hash}/`;
//    }
//  });
//}
//
//
//function setupPasswordToggle(passwordInputs, togglePasswords) {
//    togglePasswords.forEach(function (togglePassword, index) {
//        togglePassword.addEventListener('click', function () {
//            var passwordInput = passwordInputs[index];
//
//            if (passwordInput.type === 'password') {
//                passwordInput.type = 'text';
//                togglePassword.classList.remove('fa-eye');
//                togglePassword.classList.add('fa-eye-slash');
//                togglePassword.title = isEnglish ? 'Hide password' : 'Skryť heslo';
//            } else {
//                passwordInput.type = 'password';
//                togglePassword.classList.remove('fa-eye-slash');
//                togglePassword.classList.add('fa-eye');
//                togglePassword.title = isEnglish ? 'Show password' : 'Ukázať heslo';
//            }
//        });
//    });
//}
//
//function lectorLogin() {
//    Swal.fire({
//        title: 'Prihlásenie Lektora',
//        html:
//            '<div class="swal-layout-login">' +
//            '   <div class="swal-group">' +
//            '       <input id="pin-login" class="swal2-input" type="password" placeholder="PIN" autocomplete="new-password">' +
//            '       <i class="toggle-password fas fa-eye" id="toggle-pin-login" title="Ukázať PIN"></i>' +
//            '   </div>' +
//            '</div>',
//        confirmButtonText: 'Prihlásiť',
//        showCancelButton: true,
//        didOpen: function () {
//
//            document.getElementById('pin-login').addEventListener('keyup', function (event) {
//                if (event.keyCode === 13) {
//                    Swal.clickConfirm();
//                }
//            });
//
//            document.getElementById('pin-login').focus();
//
//            var swalLayout = document.querySelector('.swal-layout-login');
//            swalLayout.style.display = 'flex';
//            swalLayout.style.alignItems = 'center';
//            swalLayout.style.flexDirection = 'column';
//
//            var pinInput = document.getElementById('pin-login');
//            var togglePin = document.getElementById('toggle-pin-login');
//
//            setupPasswordToggle([pinInput], [togglePin]);
//        },
//        preConfirm: () => {
//            var pinInput = Swal.getPopup().querySelector('#pin-login');
//            var pin = pinInput.value;
//
//            if (!pin) {
//                Swal.showValidationMessage('Prosím, zadajte PIN.');
//                return false;
//            }
//
//            if (!/^\d+$/.test(pin)) {
//                Swal.showValidationMessage('Prosím, zadajte platný PIN obsahujúci iba číslice.');
//                return false;
//            }
//
//            return { pin };
//        },
//    }).then((result) => {
//        if (result.isConfirmed) {
//            fetch('/login_lector/', {
//                method: 'POST',
//                headers: {
//                    'Content-Type': 'application/json',
//                    'X-CSRFToken': csrfToken,
//                },
//                body: JSON.stringify(result.value),
//            })
//            .then(response => response.json())
//            .then(data => {
//                var user = data.user;
//                if (data.status === 'success') {
//                    Swal.fire({
//                        icon: 'success',
//                        title: data.message,
//                        showConfirmButton: false,
//                        timer: 1000,
//                    });
//                    setTimeout(() => {
//                        if (user === 'lector') {
//                            window.location.href = `/lector_view/${data.hash}/`;
//                        } else {
//                            window.location.href = `/course_view/${data.hash}/`;
//                        }
//                    }, 1000);
//                } else {
//                    Swal.fire({
//                        icon: 'error',
//                        title: data.message,
//                    });
//                }
//            })
//            .catch(error => {
//                Swal.fire({
//                    icon: 'error',
//                    title: 'Nastala chyba pri prihlásení',
//                    text: 'Skúste to prosím znova.',
//                });
//                console.error('Error during fetch:', error);
//            });
//        }
//    });
//}