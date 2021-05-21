select
-- violent warnings
(SELECT count(*) from casrec_csv.pat where "VWM" not in ('', '0')) +
-- special warnings
(SELECT count(*) from casrec_csv.pat where "SIM" not in ('', '0')) +
-- SAAR Check
(SELECT count(*) from casrec_csv.pat where "SAAR Check" not in ('', '0')) +
-- No Debt Check
(SELECT count(*) from casrec_csv.pat where "Debt chase" not in ('', '0')) +
-- Deputy violent warnings
(SELECT count(*) from casrec_csv.deputy where "VWM" not in ('', '0')) +
-- deputy special warnings
(SELECT count(*) from casrec_csv.deputy where "SIM" not in ('', '0'))
as warnings,

-- violent warnings
(SELECT count(*) from casrec_csv.pat where "VWM" not in ('', '0')) +
-- special warnings
(SELECT count(*) from casrec_csv.pat where "SIM" not in ('', '0')) +
-- SAAR Check
(SELECT count(*) from casrec_csv.pat where "SAAR Check" not in ('', '0')) +
-- No Debt Check
(SELECT count(*) from casrec_csv.pat where "Debt chase" not in ('', '0'))
as person_warnings_client,
-- Deputy violent warnings
(SELECT count(*) from casrec_csv.deputy where "VWM" not in ('', '0')) +
-- deputy special warnings
(SELECT count(*) from casrec_csv.deputy where "SIM" not in ('', '0'))
as person_warnings_deputy;
