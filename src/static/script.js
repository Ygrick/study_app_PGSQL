document.getElementById('addContactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const lastName = document.getElementById('addLastName').value;
    const firstName = document.getElementById('addFirstName').value;
    const birthday = document.getElementById('addBirthday').value;
    const mail = document.getElementById('addMail').value;
    
    const dataToSend = {
        last_name: lastName,
        first_name: firstName,
        birthday: birthday,
        mail: mail
    };

    fetch('/add_contact/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ответ сервера:", data);
        loadContacts();
    });
});

document.getElementById('updateContactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const lastName = document.getElementById('updateLastName').value;
    const firstName = document.getElementById('updateFirstName').value;
    const birthday = document.getElementById('updateBirthday').value;
    const mail = document.getElementById('updateMail').value;
    
    const dataToSend = {
        last_name: lastName,
        first_name: firstName,
        birthday: birthday,
        mail: mail
    };

    fetch('/update_contact/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ответ сервера:", data);
        loadContacts();
    });
});

document.getElementById('deleteContactForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const lastName = document.getElementById('deleteLastName').value;
    
    fetch('/delete_contact/' + encodeURIComponent(lastName), {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ответ сервера:", data);
        loadContacts();
    });
});

function loadContacts() {
    fetch('/contacts/')
        .then(response => response.json())
        .then(data => {
            const contactsList = document.getElementById('contactsList');
            contactsList.innerHTML = '';
            data.forEach(contact => {
                const li = document.createElement('li');
                li.textContent = `Фамилия: ${contact.last_name}, Имя: ${contact.first_name}, День рождения: ${contact.birthday}, Почта: ${contact.mail}`;
                contactsList.appendChild(li);
            });
        });
}

function loadContactsAudit() {
fetch('/contacts_audit/')
    .then(response => response.json())
    .then(data => {
        const contactsAuditList = document.getElementById('contactsAuditList');
        contactsAuditList.innerHTML = '';
        data.forEach(audit => {
            const li = document.createElement('li');
            li.textContent = `ID контакта: ${audit.contact_id}, Дата операции: ${audit.op_date}, Тип операции: ${audit.op_type}, Почта: ${audit.mail}`;
            contactsAuditList.appendChild(li);
        });
    });
}