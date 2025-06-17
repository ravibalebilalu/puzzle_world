const grid_side_cells = [
    0, 1, 2, 9, 10, 11, 18, 19, 20, 6, 7, 8, 15, 16, 17, 24, 25, 26, 30, 31, 32,
    39, 40, 41, 48, 49, 50, 54, 55, 56, 60, 61, 62, 63, 64, 65, 69, 70, 71, 72,
    73, 74, 78, 79, 80,
];

const cells = document.querySelectorAll('.cells');
const cell_values = document.querySelectorAll('.cv');

// background for cells
cells.forEach((cell, index) => {
    if (grid_side_cells.includes(index)) {
        cell.style.backgroundColor = '#777';
    } else {
        cell.style.backgroundColor = '#444';
    }
});
// hide '.' in cells
cell_values.forEach((cv) => {
    if (cv.textContent == '.') {
        cv.style.opacity = '0';
    }
});

// highlight cell when selected

document.addEventListener('DOMContentLoaded', function () {
    const radioes = document.querySelectorAll('input[name="selected"]');
    radioes.forEach((radio) => {
        radio.addEventListener('change', function () {
            document.querySelectorAll('label.cells').forEach((label) => {
                label.style.border = ' 1px solid rgb(33, 83, 96)';
            });
            const selectedId = this.id;
            const label = document.querySelector(`label[for="${selectedId}"]`);
            if (label) {
                label.style.border = '3px solid #990';
            }
        });
    });
});
