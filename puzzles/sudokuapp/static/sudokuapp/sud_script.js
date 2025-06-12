 // Utility to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Sudoku styling
const columns = document.querySelectorAll('.col');
const first_box = [
    0, 1, 2, 6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 24, 25, 26, 54,
    30, 31, 32, 39, 40, 41, 48, 49, 50, 55, 56,
    60, 61, 62, 63, 64, 65, 69, 70, 71, 72, 73, 74, 78, 79, 80,
];

for (let col = 0; col < columns.length; col++) {
    if (first_box.includes(col)) {
        columns[col].style.outline = '10px solid #555';
        columns[col].style.backgroundColor = '#555';
    } else {
        columns[col].style.outline = '10px solid #777';
        columns[col].style.backgroundColor = '#777';
    }
}

// Data sending logic
const sudokuUrl = document.body.dataset.sudokuUrl;
let selectedCell = null;

document.querySelectorAll(".col").forEach((cell) => {
      
     
    cell.addEventListener("click", () => {
        selectedCell = cell;
        
        
        
    });
});

document.querySelectorAll(".num").forEach((btn) => {
    btn.addEventListener("click", () => {
        if (!selectedCell) return;
        const row = selectedCell.dataset.row;
        const col = selectedCell.dataset.col;
        const val = btn.dataset.val;

        fetch(sudokuUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ row, col, val })
        })
        .then(res => res.json())
        .then(data => {
            if (data.valid) {
                selectedCell.textContent = val;
            } else {
                alert("Invalid move!");
            }
        })
        .catch(err => console.error("Error:", err));
    });
});
