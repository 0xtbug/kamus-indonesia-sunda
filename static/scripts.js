document.getElementById('wordForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const indonesian = document.getElementById('indonesian').value.toLowerCase();
    const sundanese = document.getElementById('sundanese').value.toLowerCase();

    const response = await fetch('/add_word', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({indonesian, sundanese})
    });

    if (response.ok) {
        Swal.fire({
            title: 'Berhasil!',
            text: 'Kata berhasil ditambahkan',
            icon: 'success',
            timer: 1000,
            showConfirmButton: false
        });
        fetchAllWords();
    } else if (response.status === 409) {
        Swal.fire({
            title: 'Gagal!',
            text: 'Kata sudah ada',
            icon: 'error',
            timer: 1000,
            showConfirmButton: false
        });
    } else {
        Swal.fire({
            title: 'Gagal!',
            text: 'Terjadi kesalahan saat menambahkan kata',
            icon: 'error',
            timer: 1000,
            showConfirmButton: false
        });
    }
});

async function fetchTranslation() {
    const searchType = document.getElementById('searchType').value;
    const searchWord = document.getElementById('searchWord').value.toLowerCase();
    const response = await fetch(`/get_translation?term=${searchWord}&lang=${searchType}`);
    const translations = await response.json();
    const translationTable = document.getElementById('translationTable');
    translationTable.innerHTML = '';
    if (translations.length > 0) {
        let tableContent = '<table class="table table-responsive"><thead><tr><th>Bahasa Indonesia</th><th>Bahasa Sunda</th></tr></thead><tbody>';
        translations.forEach(translation => {
            tableContent += `<tr><td>${translation.indonesian}</td><td>${translation.sundanese}</td></tr>`;
        });
        tableContent += '</tbody></table>';
        translationTable.innerHTML = tableContent;
    } else {
        translationTable.innerHTML = '<div class="alert alert-info" role="alert">Kata tidak ditemukan.</div>';
    }
}

async function fetchAllWords() {
    const response = await fetch('/get_all_words');
    const words = await response.json();
    const wordList = document.getElementById('wordList');
    wordList.innerHTML = '';
    words.forEach(word => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${word.indonesian}</td>
            <td>${word.sundanese}</td>
            <td><button class="btn btn-danger btn-sm" onclick="confirmDelete('${word.indonesian}', '${word.sundanese}')">Hapus</button></td>
        `;
        wordList.appendChild(row);
    });
}

async function confirmDelete(indonesian, sundanese) {
    const result = await Swal.fire({
        title: 'Konfirmasi',
        text: "Apakah Anda yakin ingin menghapus kata ini?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Hapus',
        cancelButtonText: 'Batal'
    });

    if (result.isConfirmed) {
        deleteWord(indonesian, sundanese);
    }
}

async function deleteWord(indonesian, sundanese) {
    const response = await fetch('/delete_word', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({indonesian, sundanese})
    });

    if (response.ok) {
        Swal.fire({
            title: 'Berhasil!',
            text: 'Kata berhasil dihapus',
            icon: 'success',
            timer: 1000,
            showConfirmButton: false
        });
        fetchAllWords();
    } else {
        Swal.fire({
            title: 'Gagal!',
            text: 'Terjadi kesalahan saat menghapus kata',
            icon: 'error',
            timer: 1000,
            showConfirmButton: false
        });
    }
}

fetchAllWords();
