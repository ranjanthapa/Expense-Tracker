function openForm(formName) {
    if (formName === "income-btn") {
        document.getElementById('incomeForm').style.visibility = 'visible';
        console.log("hello")
    }
    if (formName === 'expense-btn') {
        document.getElementById('expenseForm').style.visibility = 'visible';
    }
}

function closeForm(formName) {
    if (formName === "income-btn") {
        document.getElementById('incomeForm').style.visibility = 'hidden';
        console.log("hello")
    }
    if (formName === 'expense-btn') {
        document.getElementById('expenseForm').style.visibility = 'hidden';
    }

}


// Hide the flash messages container after 4 seconds
setTimeout(function () {
    var container = document.querySelector('.flash-messages');
    if (container) {
        container.style.display = 'none';
    }
}, 4000);

