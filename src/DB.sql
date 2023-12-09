-- Создание таблицы contacts
CREATE TABLE contacts (
    contact_id SERIAL PRIMARY KEY,
    last_name VARCHAR(255),
    first_name VARCHAR(255),
    birthday DATE,
    mail VARCHAR(255)
);

-- Создание таблицы contacts_audit
CREATE TABLE contacts_audit (
    contact_id INT,
    op_date TIMESTAMP,
    op_type CHAR(1),
    mail VARCHAR(255)
);

-- Создание триггерной функции
CREATE OR REPLACE FUNCTION contacts_before_change()
RETURNS TRIGGER AS 
'BEGIN
    IF TG_OP = ''INSERT'' THEN
        INSERT INTO contacts_audit(contact_id, op_date, op_type, mail)
        VALUES (NEW.contact_id, NOW(), ''i'', NEW.mail);
    ELSIF TG_OP = ''UPDATE'' THEN
        INSERT INTO contacts_audit(contact_id, op_date, op_type, mail)
        VALUES (NEW.contact_id, NOW(), ''u'', NEW.mail);
    ELSIF TG_OP = ''DELETE'' THEN
        INSERT INTO contacts_audit(contact_id, op_date, op_type, mail)
        VALUES (OLD.contact_id, NOW(), ''d'', OLD.mail);
        RETURN OLD;
    END IF;
    RETURN NEW;
END;' LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER contacts_before_change_trigger
BEFORE INSERT OR UPDATE OR DELETE ON contacts
FOR EACH ROW EXECUTE FUNCTION contacts_before_change();

-- Функция добавления контакта
CREATE OR REPLACE FUNCTION add_contact(_last_name VARCHAR, _first_name VARCHAR, _birthday DATE, _mail VARCHAR)
RETURNS void AS '
BEGIN
    INSERT INTO contacts (last_name, first_name, birthday, mail) 
    VALUES (_last_name, _first_name, _birthday, _mail);
END;
' LANGUAGE plpgsql;

-- Функция обновления контакта
CREATE OR REPLACE FUNCTION update_contact(
    _last_name VARCHAR, 
    _first_name VARCHAR, 
    _birthday DATE, 
    _mail VARCHAR
)
RETURNS void AS '
BEGIN
    UPDATE contacts 
    SET first_name = _first_name, 
        birthday = _birthday, 
        mail = _mail 
    WHERE last_name = _last_name;
END;
' LANGUAGE plpgsql;

-- Функция удаления контакта
CREATE OR REPLACE FUNCTION delete_contact(_last_name VARCHAR)
RETURNS void AS '
BEGIN
    DELETE FROM contacts 
    WHERE last_name = _last_name;
END;
' LANGUAGE plpgsql;
