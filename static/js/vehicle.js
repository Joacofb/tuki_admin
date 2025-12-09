// PRUEBA JS ARCHIVO MODELO

document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn     = document.getElementById("toggleQuickCustomer");
    const wrapper       = document.getElementById("quickCustomerWrapper");
    const cancelBtn     = document.getElementById("cancelQuickCustomer");
    const errorsBox     = document.getElementById("quickCustomerErrors");
    const customerSelect = document.getElementById("id_customer");
    const form          = document.getElementById("quickCustomerForm");

    console.log("Refs:", { toggleBtn, wrapper, form, customerSelect });

    // 1) Si no hay botón o wrapper, no podemos ni mostrar/ocultar → salimos
    if (!toggleBtn || !wrapper) {
        console.warn("No se encontró toggleBtn o wrapper para quickCustomer");
        return;
    }

    // 2) Toggle mostrar/ocultar (solo necesita botón y wrapper)
    toggleBtn.addEventListener("click", function() {
        console.log("click en toggleQuickCustomer");
        if (wrapper.style.display === "none" || wrapper.style.display === "") {
            wrapper.style.display = "block";
        } else {
            wrapper.style.display = "none";
        }
    });

    // 3) Cancelar: solo si existe el botón de cancelar
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function() {
            wrapper.style.display = "none";
            if (form) form.reset();
            if (errorsBox) {
                errorsBox.style.display = "none";
                errorsBox.innerHTML = "";
            }
        });
    }

    // 4) Submit AJAX: solo si realmente existe el form y el select
    if (form && customerSelect) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();

            if (errorsBox) {
                errorsBox.style.display = "none";
                errorsBox.innerHTML = "";
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw data; });
                }
                return response.json();
            })
            .then(data => {
                if (data.ok) {
                    const opt = new Option(data.label, data.id, true, true);
                    customerSelect.add(opt);

                    form.reset();
                    wrapper.style.display = "none";
                } else {
                    if (errorsBox) showErrors(errorsBox, data.errors);
                }
            })
            .catch(errData => {
                console.log("errData:", errData);
                if (errData && errData.errors && errorsBox) {
                    showErrors(errorsBox, errData.errors);
                }
            });
        });
    } else {
        console.warn("Form o customerSelect no encontrados, solo funcionará el toggle.");
    }

    function showErrors(errorsBox, errors) {
        let html = '<div class="alert alert-danger mb-0"><ul class="mb-0">';
        for (const [field, msgs] of Object.entries(errors)) {
            msgs.forEach(msg => {
                html += `<li><strong>${field}:</strong> ${msg}</li>`;
            });
        }
        html += "</ul></div>";
        errorsBox.innerHTML = html;
        errorsBox.style.display = "block";
    }
});
