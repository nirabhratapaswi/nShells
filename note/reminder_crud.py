from note.db_setup import conn

def create_reminder(data: list or tuple):
    """ Db reminder : Create Reminder """

    query = 'INSERT INTO reminder(reminder_id, target_time, shell_id) VALUES(?, ?, ?);'
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    return cur.lastrowid

def list_reminders() -> list:
    """ Db reminder : List All Reminders """

    query = '''
                SELECT shell_id, vision, thought from shells WHERE shell_id IN
                (SELECT shell_id FROM reminder);
            '''
    cur = conn.cursor()
    cur.execute(query)
    data = []
    for row in cur:
        data.append({
            'shell_id': row[0],
            'title': row[1],
            'body': row[2],
        })
    return data

def list_reminders_from_shell_id(shell_id: str) -> list:
    """ Db reminder : List All Reminders with shell ids """

    query = '''
                SELECT reminder_id, pid, target_time from reminder where shell_id=?;
            '''
    cur = conn.cursor()
    cur.execute(query, [shell_id])
    data = []
    for row in cur:
        data.append({
            'reminder_id': row[0],
            'pid': row[1],
            'target_time': row[2],
        })
    return data

def get_reminder_from_id(id_: str ='') -> dict:
    """ Db reminder : Get reminder from id """

    query = f'SELECT reminder_id, target_time, shell_id FROM shells WHERE reminder_id=?;'
    cur = conn.cursor()
    cur.execute(query, [id_])
    data = None
    for row in cur:
        data = {
            'reminder_id': row[0],
            'target_time': row[1],
            'shell_id': row[2],
        }
        break

    return data

def update_reminder_pid(rowid, pid):
    """ Db reminder : Update reminder pid """
    query = f'UPDATE reminder SET pid=? WHERE rowid=?;'
    cur = conn.cursor()
    cur.execute(query, (pid, rowid))
    conn.commit()
    return cur.lastrowid

def delete_reminder_by_rowid(id_: str = ''):
    """ Db reminder : Delete reminder from rowid """

    query = f'DELETE FROM reminder WHERE rowid=?;'
    cur = conn.cursor()
    cur.execute(query, [id_])
    conn.commit()
    return cur.lastrowid

def delete_reminder_by_shell_id(id_: str = ''):
    """ Db reminder : Delete reminder from shell id """

    query = f'DELETE FROM reminder WHERE shell_id=?;'
    cur = conn.cursor()
    cur.execute(query, [id_])
    conn.commit()
    return cur.lastrowid
