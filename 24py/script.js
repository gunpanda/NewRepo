const form = document.getElementById('calculatorForm');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    const length = parseFloat(document.getElementById('length').value);
    const width = parseFloat(document.getElementById('width').value);
    const gravelThickness = parseFloat(document.getElementById('gravelThickness').value) / 100; // Переводим в метры
    const sandThickness = parseFloat(document.getElementById('sandThickness').value) / 100;

    const area = length * width;
    const gravelVolume = area * gravelThickness;
    const sandVolume = area * sandThickness;

    resultDiv.innerHTML = `Для парковки площадью ${area.toFixed(2)} кв.м. потребуется:<br>
    * Гравий: ${gravelVolume.toFixed(2)} куб.м. (слой ${(gravelThickness * 100).toFixed(1)} см)<br>
    * Песок: ${sandVolume.toFixed(2)} куб.м. (слой ${(sandThickness * 100).toFixed(1)} см)`;
});