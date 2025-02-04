
function startTestAgain(pin_hash, test_order) {
    Swal.fire({
        icon: 'warning',
        text: `Po novom vyhodnotení sa história tohto testu prepíše, začať znova?`,
        confirmButtonText: 'Začať',
        showCancelButton: true,
        cancelButtonText: 'Zrušiť',
    }).then((result) => {
        if (result.isConfirmed) {
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
    });
}