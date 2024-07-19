function checkPassword(form) {
    var password = form.password.value;
    var confirmPassword = form.cnfpassword.value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false; 
    }
    return true; 
}