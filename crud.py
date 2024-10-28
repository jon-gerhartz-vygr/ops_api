from connect import execute_query, fetch_pandas
from queries import *
from utils import write_log


allowed_keys = {'EMAIL', 'FIRST_NAME', 'LAST_NAME', 'ADDRESS1', 'ADDRESS2', 'CITY',
                'STATE', 'ZIP', 'PHONE_COUNTRY_CODE', 'PHONE', 'COUNTRY_CODE', 'IS_FOREIGN', 'HAS_CLAIM'}

address_fields = ['ADDRESS1', 'ADDRESS2', 'CITY',
                  'STATE', 'ZIP', 'COUNTRY_CODE']

name_fields = ['FIRST_NAME', 'LAST_NAME']


def update_user(user_id, data):
    len_data = len(data)
    update_statements = ''
    i = 0
    keys = []
    update_name = False
    update_address = False
    update_email = False

    for key in data:
        upper_key = key.upper()
        keys.append(upper_key)
        statement = f"{key}='{data[key]}'"
        if len_data != 1:
            if i != len_data - 1:
                statement += ','
        update_statements += statement

        if upper_key in address_fields:
            update_address = True
        elif upper_key in name_fields:
            update_name = True
        elif upper_key == 'EMAIL':
            update_email = True

        i += 1

    if update_address == True:
        update_statements += ', ADDRESS_UPDATED_TS = CURRENT_TIMESTAMP'
    if update_name == True:
        update_statements += ', NAME_UPDATED_TS = CURRENT_TIMESTAMP'
    if update_email == True:
        update_statements += ', EMAIL_UPDATED_TS = CURRENT_TIMESTAMP'

    formatted_q_get_user = q_get_user.format(user_id=user_id)
    upper_data_keys = set([key.upper() for key in data.keys()])
    try:
        current_user_data_df = fetch_pandas(formatted_q_get_user)

        unallowed_keys = upper_data_keys - allowed_keys
        assert len(
            unallowed_keys) == 0, f'Invalid keys passed: {str(unallowed_keys)}'

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
        message = f'{user_id} failed to make update: {error_message}'
        status = 'error'
        write_log('ERROR', user_id, 'VYGR_USER_ID', message, data)

    resp = {'status': status, 'message': message}
    return resp


def handle_reissue_request(user_id, data):
    distribution_name = data['distribution_name']
    formatted_get_eligible_check = q_get_eligible_check.format(
        user_id=user_id, distribution_name=distribution_name)
    try:
        resissue_check_df = fetch_pandas(formatted_get_eligible_check)
        assert len(resissue_check_df) > 0, 'No eligible checks found'

        check_amount = resissue_check_df['CHECK_AMOUNT'][0]
        check_number = resissue_check_df['CHECK_NUMBER'][0]

        internal_status = 'REISSUE_APPROVED'

        formatted_q_update_internal_status = q_update_internal_status.format(
            internal_status=internal_status, check_number=check_number)
        execute_query(formatted_q_update_internal_status)

        status = 'complete'
        message = f'{check_number} successfully updated to {internal_status}'
    except Exception as e:
        error_message = str(e)
        message = f'{user_id} failed to process reissue request: {error_message}'
        status = 'error'
        write_log('ERROR', user_id, 'VYGR_USER_ID', message, data)

    resp = {'status': status, 'message': message}
    return resp
