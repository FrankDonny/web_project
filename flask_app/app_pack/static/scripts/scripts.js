const btn = document.getElementById('create')
btn.addEventListener('click', () => {
    const formDiv = document.getElementById('create_room');
    if (formDiv.style.display === 'none') {
        formDiv.style.display = 'block';
    } else {
        formDiv.style.display = 'none';
    }
})