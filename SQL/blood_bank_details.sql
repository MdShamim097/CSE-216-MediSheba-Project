CREATE OR REPLACE FUNCTION get_blood_bank_details(
  id IN  MEDI_SHEBA.BLOOD_BANK.BLOOD_BANK_ID%TYPE
) RETURN MEDI_SHEBA.BLOOD_BANK%ROWTYPE
AS
  l_cust_record MEDI_SHEBA.BLOOD_BANK%ROWTYPE;
BEGIN
  SELECT *
  INTO   l_cust_record
  FROM   MEDI_SHEBA.BLOOD_BANK
  WHERE  BLOOD_BANK_ID=id;

  RETURN l_cust_record;
END;
/
/*
DECLARE
  r_acct  MEDI_SHEBA.BLOOD_BANK%ROWTYPE;
BEGIN
     r_acct := get_blood_bank_details(23);
		 DBMS_OUTPUT.PUT_LINE( r_acct.NAME ||'  ' ||	r_acct."A+"||'  ' ||	r_acct."A-"||'  ' ||	r_acct."B+"||'  ' ||r_acct."B-"||'  ' ||	r_acct."O+"||'  ' ||	r_acct."O-"||'  ' ||	r_acct."AB+"||'  ' ||	r_acct."AB-"|| '  '|| r_acct.FIRST_NAME|| '  ' || r_acct.LAST_NAME);
END;
/
 */