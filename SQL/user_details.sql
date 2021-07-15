CREATE OR REPLACE FUNCTION get_user_details(
  id IN  MEDI_SHEBA.USERS.USER_ID%TYPE
) RETURN MEDI_SHEBA.USERS%ROWTYPE
AS
  l_cust_record MEDI_SHEBA.USERS%ROWTYPE;
BEGIN
  SELECT *
  INTO   l_cust_record
  FROM   MEDI_SHEBA.USERS
  WHERE  USER_ID=id;

  RETURN l_cust_record;
END;
/
/*
DECLARE
  r_acct  MEDI_SHEBA.USERS%ROWTYPE;
BEGIN
     r_acct := get_user_details(1);
		 DBMS_OUTPUT.PUT_LINE( r_acct.FIRST_NAME ||'  ' ||	r_acct.LAST_NAME || '  ' || r_acct.PHONE || '   '|| r_acct.EMAIL || '  ' || r_acct.BLOOD_GROUP || '  ' || NVL(r_acct.ISBLOOD_AVAILABLE,0));
END;
/
*/