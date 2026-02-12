import json
from flask import request, jsonify
from db_stuff import get_db_cursor

def handle_form_submission():
    data = request.json
    cursor = get_db_cursor()
    
    # --- SEPARATE FIELDS & PREPARE DATA ---
    # We explicitly look for schema columns, everything else goes to custom_fields
    standard_columns = ['name', 'email', 'phone_number', 'tags']
    
    insert_data = {}
    custom_fields = {}
    
    for key, value in data.items():
        if key in standard_columns:
            insert_data[key] = value
        else:
            custom_fields[key] = value
            
    # Ensure mandatory name is present (simple validation)
    if 'name' not in insert_data:
        return jsonify({"error": "Name is required"}), 400

    name = insert_data.get('name')
    email = insert_data.get('email')
    phone = insert_data.get('phone_number')
    tags = insert_data.get('tags')
    custom_json = json.dumps(custom_fields)

    # "Attempt to insert... if there's a duplicate it will throw error because of DB constraints"
    try:
        query_insert = """
            INSERT INTO leads (name, email, phone_number, tags, custom_fields)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (name, email, phone, tags, custom_json))
        cursor.connection.commit()
    except Exception as e:
        # Ignore duplicates for now
        print(f"Insert failed (likely duplicate): {e}")

    try:
        # Update existing leads that have same email/phone
        query_update = """
            UPDATE leads 
            SET name = %s, tags = %s, custom_fields = %s
            WHERE email = %s OR phone_number = %s
        """
        cursor.execute(query_update, (name, tags, custom_json, email, phone))
        cursor.connection.commit()
    except Exception as e:
        return jsonify({"error": f"Update failed: {e}"}), 500

    try:
        cursor.execute("SELECT DISTINCT email FROM leads WHERE email IS NOT NULL")
        all_emails = cursor.fetchall() # Returns list of tuples like [('bob@gmail.com',), ...]

        for email_record in all_emails:
            target_email = email_record[0]
            count = cursor.execute("SELECT COUNT(*) FROM leads WHERE email = %s", (target_email,)).fetchone()[0]

            if count > 1:
                raise Exception(f"CRITICAL INTEGRITY ERROR: Duplicate email found for {target_email}")
        
        cursor.execute("SELECT DISTINCT phone_number FROM leads WHERE phone_number IS NOT NULL")
        all_phones = cursor.fetchall()
        for phone_record in all_phones:
            target_phone = phone_record[0]
            
            cursor.execute("SELECT COUNT(*) FROM leads WHERE phone_number = %s", (target_phone,))
            count = cursor.fetchone()[0]
            
            if count > 1:
                raise Exception(f"CRITICAL INTEGRITY ERROR: Duplicate phone found for {target_phone}")
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 200