q_write_audit_log = """
INSERT INTO LIQUIDATION_TRUST.SRC.AUDIT_LOG_EVENTS (
"ACTION_TS"
, "ACTION_CODE"
, "IDENTIFIER"
, "IDENTIFIER_TYPE"
, "AUTHOR_NAME"
, "AUTHOR_EMAIL"
, "AUTHOR_IP"
, "AUTHOR_COMMENT"
, "CLIENT_CODE"
, "DATA_BEFORE"
, "DATA_AFTER"
)
SELECT
    current_timestamp
    , 'UPDATE_ADDRESS'
    , '{user_id}'
    , 'USER_ID'
    , 'ServiceAccount'
    , 'svrc_acct@investvoyager.com'
    , current_ip_address()
    , 'updating user PII via python ops API'
    , 'PYTHON_OPS_API'
    , {prior_pii_data}::variant
    , {new_pii_data}::variant
"""

q_update_user = """
UPDATE LIQUIDATION_TRUST.SRC.USERS
SET 
{update_statements}
WHERE id = '{user_id}'
"""

q_get_user = """
SELECT 
    id
    , type
    , email
    , first_name
    , last_name
    , coalesce(address1, '') as address1
    , coalesce(address2, '') as address2
    , coalesce(city, '') as city
    , coalesce(state, '') as state
    , coalesce(zip, '') as zip
    , phone_country_code
    , phone
    , ssn
    , dob
    , address_updated_ts
    , email_updated_ts
    , name_updated_ts
    , country_code
    , is_foreign
    , can_log_in
    , has_claim
FROM LIQUIDATION_TRUST.SRC.USERS
WHERE id = '{user_id}'
"""

# queries for reissue requests api
q_get_eligible_check = """
SELECT usd.*
FROM LIQUIDATION_TRUST.SRC.USD_DISTRIBUTIONS usd
JOIN LIQUIDATION_TRUST.SRC.USER_CLAIM uc on uc.claim_number = usd.claim_number
JOIN LIQUIDATION_TRUST.SRC.USERS u on u.id = uc.user_id
WHERE
    u.id = '{user_id}'
    and usd.distribution_name = '{distribution_name}'
    and (usd.bank_status = 'UNCASHED' OR (usd.bank_status = 'VOID' and usd.mail_status = 'UNDELIVERABLE'))
    and usd.internal_status = 'ISSUED'
QUALIFY rank() over (partition by usd.claim_number order by check_date desc) = 1;
"""

q_update_internal_status = """
UPDATE LIQUIDATION_TRUST.SRC.USD_DISTRIBUTIONS
SET internal_status = '{internal_status}', internal_status_updated_ts = current_timestamp
WHERE check_number = '{check_number}'
"""
