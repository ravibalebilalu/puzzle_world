 
 


document.addEventListener('DOMContentLoaded', () => {
    console.log("shreekrishna")
    const canvas = document.getElementById('selectionCanvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.container');
    const labels = document.querySelectorAll('.container label');
    let isDragging = false;
    let startIndex = null;
    let selectedIndices = [];

    // Set canvas size
    function resizeCanvas() {
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Get grid position from mouse coordinates
    function getGridPosition(x, y) {
        const rect = canvas.getBoundingClientRect();
        const col = Math.floor(((x - rect.left) / rect.width) * 12);
        const row = Math.floor(((y - rect.top) / rect.height) * 12);
        if (col >= 0 && col < 12 && row >= 0 && row < 12) {
            return row * 12 + col;
        }
        return null;
    }

    // Draw line on canvas
    function drawLine(startIndex, endIndex) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (startIndex === null || endIndex === null) return;

        const startLabel = document.querySelector(`label[data-index="${startIndex}"]`);
        const endLabel = document.querySelector(`label[data-index="${endIndex}"]`);
        if (!startLabel || !endLabel) return;

        const startRect = startLabel.getBoundingClientRect();
        const endRect = endLabel.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();

        ctx.beginPath();
        ctx.moveTo(
            startRect.left + startRect.width / 2 - containerRect.left,
            startRect.top + startRect.height / 2 - containerRect.top
        );
        ctx.lineTo(
            endRect.left + endRect.width / 2 - containerRect.left,
            endRect.top + endRect.height / 2 - containerRect.top
        );
        ctx.strokeStyle = 'yellow';
        ctx.lineWidth = 30;
        ctx.stroke();
    }

    // Get indices between start and end (horizontal, vertical, or diagonal)
    function getSelectedIndices(start, end) {
        const indices = [];
        const startRow = Math.floor(start / 12);
        const startCol = start % 12;
        const endRow = Math.floor(end / 12);
        const endCol = end % 12;

        const rowDiff = endRow - startRow;
        const colDiff = endCol - startCol;
        const steps = Math.max(Math.abs(rowDiff), Math.abs(colDiff));

        if (steps === 0) return [start];

        const rowStep = rowDiff / steps;
        const colStep = colDiff / steps;

        for (let i = 0; i <= steps; i++) {
            const row = Math.round(startRow + i * rowStep);
            const col = Math.round(startCol + i * colStep);
            if (row >= 0 && row < 12 && col >= 0 && col < 12) {
                indices.push(row * 12 + col);
            }
        }
        return indices;
    }

    // Check selected word
     // Inside checkWord function, replace the selectedChars logic
function checkWord() {
    if (selectedIndices.length < 2) return;

    const selectedChars = selectedIndices.map(idx => {
        const input = document.getElementById(`id${idx}`);
        return input ? input.value[0] : '';
    }).join('');

    fetch('/check-word/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ word: selectedChars })
    })
    .then(response => response.json())
    .then(data => {
        if (data.correct) {
            selectedIndices.forEach(idx => {
                const label = document.querySelector(`label[data-index="${idx}"]`);
                if (label) label.style.color = 'rgb(136, 108, 108)';
            });
            const wordDiv = Array.from(document.querySelectorAll('.word')).find(div => 
                div.textContent.trim().toUpperCase() === selectedChars.toUpperCase() ||
                div.textContent.trim().toUpperCase() === selectedChars.toUpperCase().split('').reverse().join('')
            );
            if (wordDiv) wordDiv.style.color = 'green';
        }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });
}
    // Canvas event listeners
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        startIndex = getGridPosition(e.clientX, e.clientY);
        selectedIndices = [];
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const currentIndex = getGridPosition(e.clientX, e.clientY);
        if (currentIndex !== null) {
            selectedIndices = getSelectedIndices(startIndex, currentIndex);
            drawLine(startIndex, currentIndex);
        }
    });

    canvas.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            checkWord();
            selectedIndices = [];
            startIndex = null;
        }
    });

    canvas.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            selectedIndices = [];
            startIndex = null;
        }
    });
});