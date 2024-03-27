from connect import execute_query, fetch_pandas
from queries import *


def update_user(user_id, data):
    len_data = len(data)
    update_statements = ''
    i = 0
    keys = []
    for key in data:
        keys.append(key.upper())
        statement = f"{key}='{data[key]}'"
        if len_data != 1:
            if i != len_data - 1:
                statement += ','
        update_statements += statement
        i += 1

    formatted_q_get_user = q_get_user.format(user_id=user_id)

    try:
        current_user_data_df = fetch_pandas(formatted_q_get_user)
        prior_pii_data = current_user_data_df[keys].to_dict(orient='records')[
            0]

        formatted_q_write_audit_log = q_write_audit_log.format(
            user_id=user_id, prior_pii_data=prior_pii_data, new_pii_data=data)
        log_result = execute_query(formatted_q_write_audit_log)

        formatted_q_update_user = q_update_user.format(
            update_statements=update_statements, user_id=user_id)
        update_result = execute_query(formatted_q_update_user)

        status = 'complete'
        message = f'{user_id} successfully updated'
    except Exception as e:
        error_message = str(e)
        message = f'failed to make update: {error_message}'
        status = 'error'

    resp = {'status': status, 'message': message}
    return resp
