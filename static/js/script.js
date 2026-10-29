document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.getElementById('fileName');
    const submitBtn = document.getElementById('submitBtn');
    const uploadForm = document.getElementById('uploadForm');

    // Deshabilitar el botón inicialmente
    submitBtn.disabled = true;

    // Escuchar cuando el usuario seleccione un archivo
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];

        if (file) {
            fileNameDisplay.textContent = `Archivo seleccionado: ${file.name}`;

            // Validar extensión en el frontend
            if(file.name.endsWith('.txt')) {
                submitBtn.disabled = false;
                fileNameDisplay.style.color = '#27ae60'; // Verde si es válido
            } else {
                submitBtn.disabled = true;
                fileNameDisplay.textContent += ' (Error: Solo se admiten archivos .txt)';
                fileNameDisplay.style.color = '#e74c3c'; // Rojo si es inválido
            }
        } else {
            fileNameDisplay.textContent = 'Ningún archivo seleccionado';
            submitBtn.disabled = true;
            fileNameDisplay.style.color = '#7f8c8d';
        }
    });

    // Pequeño feedback visual al enviar
    uploadForm.addEventListener('submit', () => {
        submitBtn.textContent = 'Procesando...';
        submitBtn.disabled = true;
    });
});