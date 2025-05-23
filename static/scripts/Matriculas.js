// Padrões portugueses
const formatosPortugueses = [
    /^[A-Z]{2}-\d{2}-\d{2}$/,  // AA-00-00
    /^\d{2}-\d{2}-[A-Z]{2}$/,  // 00-00-AA
    /^\d{2}-[A-Z]{2}-\d{2}$/,  // 00-AA-00
    /^[A-Z]{2}-\d{2}-[A-Z]{2}$/ // AA-00-AA
];

function verificarMatricula() {
    const input = document.getElementById("matriculaInput");
    const texto = input.value.trim();

    const valida = formatosPortugueses.some(pattern => pattern.test(texto));
    if (valida) {
        alert("✅ Matrícula válida!");
    } else {
        alert("❌ Matrícula inválida. Use o formato: AA-00-00 ou similar.");
    }
}

// Formatação dinâmica ao digitar
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("matriculaInput");

    input.addEventListener("input", function (e) {
        let valor = input.value.toUpperCase().replace(/[^A-Z0-9]/g, "");

        let formatado = '';
        for (let i = 0; i < valor.length; i++) {
            if (i > 0 && i % 2 === 0 && i < 6) {
                formatado += '-';
            }
            formatado += valor[i];
        }

        input.value = formatado;
    });
});