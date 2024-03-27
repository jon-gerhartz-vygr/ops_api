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
SELECT *
FROM LIQUIDATION_TRUST.SRC.USERS
WHERE id = '{user_id}'
"""
