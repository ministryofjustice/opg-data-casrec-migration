DROP SCHEMA IF EXISTS reference CASCADE;

 CREATE SCHEMA reference;

CREATE TABLE reference.sagelink (
    "Sage No" varchar(8),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Partner No" varchar(8),
    "FILLER-1" varchar(14)
);

CREATE TABLE reference.cwserr (
    "Proc Date" varchar(8),
    "Proc Time" varchar(8),
    "Seq" varchar(4),
    "Error" varchar(30),
    "Data Rec" varchar(374),
    "Case" varchar(8),
    "Sender Bits" varchar(105),
    "Date Rcvd" varchar(8),
    "Form Type" varchar(34),
    "Scan Date" varchar(8),
    "Node ID" varchar(10),
    "Doc Type" varchar(32),
    "Doc ID" varchar(169)
);

CREATE TABLE reference.qasrec (
    "RECORD" varchar(400),
    "QAS Code" varchar(8),
    "QAS Lvl" varchar(1),
    "QAS Line" varchar(4),
    "QAS Details" varchar(70),
    "QAS Adrs1" varchar(60),
    "QAS Adrs2" varchar(60),
    "QAS Adrs3" varchar(60),
    "QAS Adrs4" varchar(60),
    "QAS Adrs5" varchar(60),
    "QAS State" varchar(4),
    "FILLER-1" varchar(15)
);

CREATE TABLE reference.drlog (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Deputy No" varchar(8),
    "Pri" varchar(1),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Logdate" varchar(8),
    "Logtime" varchar(8),
    "FILLER_1" varchar(28)
);

CREATE TABLE reference.newfee (
    "RECORD" varchar(150),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Date" varchar(8),
    "Date Paid" varchar(8),
    "Amount" varchar(8),
    "Amount Paid" varchar(8),
    "Amount OS" varchar(8),
    "Comment" varchar(2),
    "Fee Band" varchar(2),
    "Fee No" varchar(5),
    "Year" varchar(4),
    "Type" varchar(2),
    "Sage Ext" varchar(1),
    "Partner No" varchar(8),
    "Fee Suff" varchar(1),
    "Remis Flag" varchar(1),
    "Remis" varchar(2),
    "Exemp Flag" varchar(1),
    "Exempt" varchar(2),
    "Pay Type" varchar(1),
    "FILLER-1" varchar(42)
);

CREATE TABLE reference.panel_refer (
    "RECORD" varchar(150),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Case" varchar(8),
    "Application Date" varchar(8),
    "Referral Date" varchar(8),
    "App Req" varchar(1),
    "Last Contact" varchar(8),
    "Acc/Rej" varchar(1),
    "App Rcvd" varchar(1),
    "Pr Batchno" varchar(8),
    "Reject" varchar(2),
    "Case Type" varchar(1),
    "FILLER-1" varchar(70)
);

CREATE TABLE reference.setupextract (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Partner No" varchar(8),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "Order No" varchar(8),
    "ExtFlag" varchar(1),
    "Fee Deputy" varchar(8),
    "Fee Dep Addr" varchar(8),
    "Asf Flag" varchar(1),
    "Asf Annl" varchar(1),
    "Dcsd Flag" varchar(1),
    "Fee Order" varchar(8),
    "Dep Fee" varchar(1),
    "FOE Flag" varchar(1),
    "ODP Flag" varchar(1),
    "FILLER-1" varchar(1)
);

CREATE TABLE reference.sm_batch_acttrack (
    "LOG-RECORD" varchar(100),
    "SM Batch No" varchar(8),
    "Date Created" varchar(8),
    "Time Create" varchar(8),
    "Invcreate" varchar(8),
    "Invtime" varchar(8),
    "Create To" varchar(8),
    "Picked" varchar(2),
    "Skipped" varchar(2),
    "Run Type" varchar(1),
    "Adv Days" varchar(2),
    "Comp" varchar(1),
    "Date From" varchar(8),
    "FILLER-1" varchar(40)
);

CREATE TABLE reference.deputyaddrdup (
    "Dep Addr No" varchar(8),
    "Dup Addr No" varchar(8),
    "Comment" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Done" varchar(1),
    "FILLER-1" varchar(57)
);

CREATE TABLE reference.applicantdup (
    "Partner No" varchar(8),
    "Dup Partner No" varchar(8),
    "Comment" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "FILLER-1" varchar(58)
);

CREATE TABLE reference.orderhistory (
    "RECORD" varchar(200),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Order No" varchar(8),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Ord Stat" varchar(8),
    "Ord Type" varchar(2),
    "Made Date" varchar(8),
    "Issue Date" varchar(8),
    "Fee Rqd" varchar(1),
    "Bond Rqd" varchar(1),
    "Dep App" varchar(1),
    "Spvn Received" varchar(8),
    "Expiry Date" varchar(8),
    "Judge" varchar(2),
    "Clause Expiry" varchar(8),
    "Chase1" varchar(8),
    "Chase2" varchar(8),
    "Chs Ind" varchar(2),
    "Bond Co" varchar(2),
    "Bond No." varchar(6),
    "Bond Amount" varchar(3),
    "Bond Renewal" varchar(8),
    "Bond Discharge" varchar(8),
    "FiD-C" varchar(1),
    "Bondyy" varchar(2),
    "Ord Risk Lvl" varchar(2),
    "Asmt Cre" varchar(1),
    "Acc Rev" varchar(1),
    "Init AccRev" varchar(2),
    "Old Stat" varchar(8),
    "Last Rev" varchar(4),
    "Review Set" varchar(8),
    "Bond Pay Type" varchar(30),
    "FILLER-1" varchar(10)
);

CREATE TABLE reference.feeaas (
    "RECORD" varchar(880),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Order No" varchar(8),
    "Invoice Date" varchar(8),
    "Amount" varchar(8),
    "Amt Paid" varchar(8),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "Fee Type" varchar(2),
    "Fee Band" varchar(2),
    "Award Date" varchar(8),
    "Asmt Date" varchar(8),
    "Invoice No" varchar(10),
    "Break1" varchar(70),
    "Break2" varchar(70),
    "Break3" varchar(70),
    "Break4" varchar(70),
    "Break5" varchar(70),
    "Break6" varchar(70),
    "Comments" varchar(200),
    "Type 1" varchar(8),
    "Type 2A" varchar(8),
    "Type 2" varchar(8),
    "Type 3" varchar(8),
    "Remit" varchar(1),
    "Appl Type" varchar(2),
    "Sort by" varchar(28),
    "BatchNo" varchar(6),
    "Partner No" varchar(8),
    "Sageno" varchar(8),
    "Asmt Level" varchar(2),
    "Remis" varchar(2),
    "Exempt" varchar(2),
    "Remit Sent" varchar(1),
    "Evidence" varchar(1),
    "Refund" varchar(8),
    "Remitted" varchar(6),
    "Remit Date" varchar(8),
    "Remit by" varchar(3),
    "FinYr" varchar(4),
    "Refund Done" varchar(1),
    "Executor" varchar(1),
    "Keydate" varchar(14),
    "ODP" varchar(1),
    "Remis. 2" varchar(2),
    "Split1" varchar(8),
    "Split2" varchar(8),
    "FOE" varchar(1),
    "Notified" varchar(1),
    "FILLER-1" varchar(5)
);

CREATE TABLE reference.deppossdup (
    "Deputy No" varchar(8),
    "Poss Dup No" varchar(8),
    "Match" varchar(1),
    "Is Dup" varchar(1),
    "Dup" varchar(1),
    "FILLER-1" varchar(11)
);

CREATE TABLE reference.casestub (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Forename" varchar(25),
    "Surname" varchar(28),
    "Away Date" varchar(8),
    "Term Date" varchar(8),
    "Term type" varchar(1),
    "Was Dep" varchar(1),
    "Birth Date" varchar(8),
    "FILLER-1" varchar(10)
);

CREATE TABLE reference.risk_assessment (
    "RECORD" varchar(1406),
    "Asmt Id" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Order No" varchar(8),
    "Date Create" varchar(8),
    "Invcreate" varchar(8),
    "Date Complete" varchar(8),
    "Start Date" varchar(8),
    "Status" varchar(10),
    "Assessor" varchar(3),
    "Auto Ind" varchar(6),
    "Asmt Lvl" varchar(2),
    "Setter ID" varchar(3),
    "Rate Ovr Flag" varchar(1),
    "Override Date" varchar(8),
    "Override Comment" varchar(1106),
    "Ovr ID" varchar(3),
    "Next Asmt Date" varchar(8),
    "New Asmt Date" varchar(8),
    "Reason New" varchar(50),
    "New ID" varchar(3),
    "Next Created" varchar(1),
    "Appeal" varchar(1),
    "Order Made" varchar(8),
    "U Cnt" int,
    "X Cnt" int,
    "AB Cnt" int,
    "C Cnt" int,
    "DE Cnt" int,
    "Y Cnt" int,
    "N Cnt" int,
    "Old Stat" varchar(10),
    "Curr State Date" varchar(8),
    "OV Reason" varchar(2),
    "Date Rcvd" varchar(8),
    "FILLER-1" varchar(61)
);

CREATE TABLE reference.pletters (
    "RECORD" varchar(140),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Panel No" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Log Date" varchar(8),
    "Log Time" varchar(8),
    "Doc Type" varchar(30),
    "Desc" varchar(30),
    "FILLER-1" varchar(29)
);

CREATE TABLE reference.deputyship (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Appl No" varchar(8),
    "Joint" varchar(2),
    "Appointed" varchar(1),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "Order No" varchar(8),
    "Corr" varchar(1),
    "News Letter" varchar(1),
    "NOTUSED2" varchar(1),
    "Fee Payer" varchar(1),
    "FILLER" varchar(25)
);

CREATE TABLE reference.prlog (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Panel No" varchar(8),
    "Pri" varchar(1),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Logdate" varchar(8),
    "Logtime" varchar(8),
    "FILLER_1" varchar(28)
);

CREATE TABLE reference.appl (
    "RECORD" varchar(220),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "AppType" varchar(2),
    "App Date" varchar(8),
    "Source" varchar(1),
    "Status" varchar(2),
    "Location" varchar(6),
    "Flr" varchar(2),
    "Cab" varchar(2),
    "Shelf" varchar(2),
    "Loc Date" varchar(8),
    "Loc Time" varchar(8),
    "Fee Paid" varchar(1),
    "App Issue" varchar(8),
    "Outcome" varchar(2),
    "Perm Rqd" varchar(1),
    "Ack Rcvd" varchar(1),
    "Sec Rcvd" varchar(8),
    "Close Date" varchar(8),
    "Away Date" varchar(8),
    "Appl Term" varchar(2),
    "Serv Comp" varchar(1),
    "Fee Reqd" varchar(1),
    "Chq Rcvd" varchar(1),
    "Papers Create" varchar(8),
    "Papers Comp" varchar(8),
    "Papers Retn" varchar(8),
    "Strap1" varchar(16),
    "Strap2" varchar(16),
    "Box No" varchar(5),
    "Dest. Date" varchar(8),
    "Dest. Req." varchar(8),
    "Destruct" varchar(1),
    "TNT Date" varchar(8),
    "Status Date" varchar(8),
    "FILLER-1" varchar(23)
);

CREATE TABLE reference.risktype3 (
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Asmt Id" varchar(8),
    "Done" varchar(1),
    "High Lvl" varchar(2),
    "Order No" varchar(8),
    "Asmt Start Date" varchar(8),
    "Dep Surname" varchar(40),
    "Dep Type" varchar(2),
    "Dep Postcode" varchar(8),
    "Select" varchar(1),
    "Review Sent" varchar(8),
    "Rcvd Date" varchar(8),
    "Followup Date" varchar(8),
    "Further" varchar(2),
    "Follow Rcvd" varchar(8),
    "FILLER-1" varchar(40)
);

CREATE TABLE reference.cwsscan (
    "RAW-RECORD" varchar(375),
    "Case" varchar(8),
    "Sender Co" varchar(40),
    "Sender Forename" varchar(25),
    "Sender Surname" varchar(40),
    "Date Rcvd" varchar(8),
    "DATERECV-DD" varchar(2),
    "DATERECV-MM" varchar(2),
    "DATERECV-YYYY" varchar(4),
    "Form Type" varchar(34),
    "Scan Date" varchar(8),
    "Node Id" varchar(10),
    "Doc Type" varchar(32),
    "DocId" varchar(170)
);

CREATE TABLE reference.enclosures (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Encl No" varchar(8),
    "Call No" varchar(8),
    "Type" varchar(2),
    "Quantity" varchar(2),
    "FILLER-1" varchar(54)
);

CREATE TABLE reference.casepremca (
    "RECORD" varchar(950),
    "by" varchar(3),
    "Create" varchar(8),
    "at" varchar(2),
    "by.1" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "Case" varchar(8),
    "Rec Init" varchar(20),
    "Rec Surname" varchar(30),
    "R Adrs1" varchar(40),
    "R Adrs2" varchar(40),
    "R Adrs3" varchar(40),
    "R Adrs4" varchar(40),
    "R Adrs5" varchar(40),
    "R Postcode" varchar(8),
    "Rtype" varchar(2),
    "R Telephone" varchar(15),
    "R TelExt" varchar(4),
    "R Email" varchar(40),
    "R Mobile" varchar(15),
    "R DXNo" varchar(8),
    "R DX Exchange" varchar(20),
    "Case Type" varchar(1),
    "Order Date" varchar(8),
    "Area" varchar(3),
    "Last Visit" varchar(8),
    "InpMod" varchar(2),
    "Loadged" varchar(8),
    "Inv" varchar(1),
    "Benefit" varchar(18),
    "FicInd" varchar(1),
    "Valsecs" varchar(4),
    "Estate" varchar(4),
    "Pass Date" varchar(8),
    "Asset Mod" varchar(8),
    "V.P.L" varchar(1),
    "Fid Val" varchar(3),
    "Fid CO" varchar(2),
    "Fid Date Disch" varchar(8),
    "Friz" varchar(6),
    "R Band" varchar(5),
    "Letter" varchar(2),
    "Rev Due" varchar(3),
    "Brkr No" varchar(3),
    "Fee Due" varchar(8),
    "Next Visit" varchar(8),
    "Circuit" varchar(2),
    "Damages" varchar(1),
    "Issue Fdirs" varchar(8),
    "Inv Req" varchar(3),
    "Fee Ver Req" varchar(8),
    "Fee Ver" varchar(8),
    "Fee Amount" varchar(3),
    "Clean Date" varchar(8),
    "Clean Init" varchar(3),
    "Clean Comments" varchar(100),
    "Clean1" varchar(50),
    "Clean2" varchar(50),
    "Disab" varchar(1),
    "Location" varchar(6),
    "Loc Date" varchar(8),
    "Loc Time" varchar(8),
    "Inv Power" varchar(6),
    "Fid C" varchar(1),
    "Fid YY" varchar(2),
    "Empow" varchar(1),
    "Emp Date" varchar(8),
    "Religion" varchar(2),
    "Case Eval" varchar(1),
    "Comments" varchar(40),
    "Curr Visit" varchar(8),
    "Prev Visit" varchar(8),
    "First Visit" varchar(8),
    "Date Removed" varchar(8),
    "Med Visit" varchar(8),
    "byLcv" varchar(3),
    "ModifyLcv" varchar(8),
    "atLcv" varchar(2),
    "GOP Rcvd" varchar(8),
    "FD Rcvd" varchar(8),
    "Death Date" varchar(8),
    "FILLER-1" varchar(12)
);

CREATE TABLE reference.patstats (
    "Case" varchar(8),
    "Acc" varchar(1),
    "Lodge Date" varchar(8),
    "Review Date" varchar(8),
    "Not Lodged" varchar(2),
    "Not Review" varchar(2),
    "Count" varchar(2),
    "Appl" varchar(1),
    "Comms" varchar(1),
    "Calls" varchar(1),
    "Cont" varchar(1),
    "Cdiary" varchar(1),
    "Cws" varchar(1),
    "Date Rcvd" varchar(8),
    "Scan Date" varchar(8),
    "Complete Date" varchar(8),
    "Not Comp" varchar(4),
    "Count.1" varchar(4),
    "Dship" varchar(1),
    "Dup" varchar(1),
    "Dupd" varchar(1),
    "Fee" varchar(1),
    "Invoice Date" varchar(8),
    "Count2" varchar(2),
    "Kpi" varchar(1),
    "NFee" varchar(1),
    "Ord" varchar(1),
    "OrdC" varchar(1),
    "RVis" varchar(1),
    "Commission Dated" varchar(8),
    "Report Rcvd." varchar(8),
    "Review Date.1" varchar(8),
    "Succ Cnt" varchar(2),
    "Canc Cnt" varchar(2),
    "Abort Cnt" varchar(2),
    "Count3" varchar(2),
    "Asmt" varchar(1),
    "Date Complete" varchar(8),
    "Start Date" varchar(8),
    "Count4" varchar(2),
    "SAct" varchar(1),
    "Start Date.1" varchar(8),
    "Date Term" varchar(8),
    "Not Comp.1" varchar(2),
    "Count5" varchar(2),
    "Vis" varchar(1),
    "FILLER-1" varchar(19)
);

CREATE TABLE reference.appl_location (
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Date" varchar(8),
    "LOGYEAR" varchar(4),
    "LOGMONTH" varchar(2),
    "LOGDAY" varchar(2),
    "Log Time" varchar(8),
    "LOGHOUR" varchar(2),
    "LOGMIN" varchar(2),
    "LOGSEC" varchar(2),
    "Location" varchar(6),
    "Flr" varchar(2),
    "Cab" varchar(2),
    "Shelf" varchar(2),
    "F/A" varchar(1),
    "Check No" varchar(3),
    "Load Date" varchar(8),
    "Load Time" varchar(8),
    "Loc Sent" varchar(1),
    "Status" varchar(4),
    "Scan Loc" varchar(6),
    "Valid Loc" varchar(7),
    "FILLER-1" varchar(20)
);

CREATE TABLE reference.cfoload (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "CFO Case" varchar(20),
    "KEYDATE" varchar(8),
    "KEYTIME" varchar(8),
    "Client Name" varchar(60),
    "Forename" varchar(25),
    "Surname" varchar(28),
    "Account No" varchar(13),
    "Balance" varchar(10),
    "Error" varchar(2),
    "Error Message" varchar(30),
    "OPG Case" varchar(8),
    "OPG Type" varchar(4),
    "Upd" varchar(1),
    "FILLER-1" varchar(22)
);

CREATE TABLE reference.feedebt (
    "RECORD" varchar(420),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Invoice Date" varchar(8),
    "Invoice No." varchar(10),
    "Due Date" varchar(8),
    "Aged" varchar(6),
    "Amount" varchar(10),
    "Invoice Date30" varchar(8),
    "Invoice No30" varchar(10),
    "Due Date30" varchar(8),
    "Aged30" varchar(6),
    "Amount30" varchar(10),
    "Invoice Date60" varchar(8),
    "Invoice No60" varchar(10),
    "Due Date60" varchar(8),
    "Aged60" varchar(6),
    "Amount60" varchar(10),
    "Invoice Date90" varchar(8),
    "Invoice No90" varchar(10),
    "Due Date90" varchar(8),
    "Aged90" varchar(6),
    "Amount90" varchar(10),
    "Invoice Date120" varchar(8),
    "Invoice No120" varchar(10),
    "Due Date120" varchar(8),
    "Aged120" varchar(6),
    "Amount120" varchar(10),
    "Invoice Date150" varchar(8),
    "Invoice No150" varchar(10),
    "Due Date150" varchar(8),
    "Aged150" varchar(6),
    "Amount150" varchar(10),
    "Invoice Date180" varchar(8),
    "Invoice No180" varchar(10),
    "Due Date180" varchar(8),
    "Aged180" varchar(6),
    "Amount180" varchar(10),
    "OPG Total Debt" varchar(10),
    "Marsh Debt" varchar(10),
    "DBS Debt" varchar(10),
    "Key Date" varchar(8),
    "Key Time" varchar(8),
    "Key Date1" varchar(8),
    "Key Time1" varchar(8),
    "OPG Debt Zero" varchar(8),
    "Marsh Debt Zero" varchar(8),
    "UPD180" varchar(1),
    "FILLER-1" varchar(17)
);

CREATE TABLE reference.useraudit (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Screen" varchar(32),
    "Entry" varchar(1),
    "Exit" varchar(1),
    "Pid" varchar(8),
    "Seq" varchar(1),
    "FILLER-1" varchar(46)
);

CREATE TABLE reference.apprelation (
    "RECORD" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Rel CoP Case" varchar(10),
    "Rel Case" varchar(8),
    "Rel AppNo" varchar(2),
    "FILLER-1" varchar(4)
);

CREATE TABLE reference.applink (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Partner No" varchar(8),
    "Judge" varchar(2),
    "Appoint" varchar(1),
    "Appl Type" varchar(2),
    "DepShip" varchar(1),
    "Corr" varchar(1),
    "Dep Type" varchar(2),
    "Fee Payer" varchar(1),
    "Del Flg" varchar(1),
    "Ord Flag" varchar(1),
    "FILLER" varchar(4)
);

CREATE TABLE reference.kpidata (
    "RECORD" varchar(250),
    "KPINo" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Source" varchar(20),
    "KPI Type" varchar(30),
    "Call Rcvd" varchar(8),
    "Team Ref." varchar(20),
    "Staff" varchar(3),
    "Activity 1" varchar(20),
    "Activ Date1" varchar(8),
    "Return Date" varchar(8),
    "Staff2" varchar(3),
    "Activity 2" varchar(20),
    "Activ Date2" varchar(8),
    "Comp Date" varchar(8),
    "Case" varchar(8),
    "Branch" varchar(20),
    "Urg" varchar(1),
    "Due Date" varchar(8),
    "Due Date2" varchar(8),
    "Due Date3" varchar(8),
    "FILLER-1" varchar(7)
);

CREATE TABLE reference.pr_batch_select (
    "RECORD" varchar(100),
    "Batch No." varchar(8),
    "Created" varchar(8),
    "Time Created" varchar(8),
    "Invdate" varchar(8),
    "Invtime" varchar(8),
    "Picked" varchar(2),
    "Skipped" varchar(2),
    "Type" varchar(1),
    "Completed" varchar(1),
    "Geoarea" varchar(2),
    "Lang" varchar(2),
    "Exp1" varchar(2),
    "Exp2" varchar(2),
    "Skill1" varchar(2),
    "Skill2" varchar(2),
    "Skill3" varchar(2),
    "Skill4" varchar(2),
    "Value" varchar(1),
    "Need1" varchar(2),
    "Need2" varchar(2),
    "Need3" varchar(2),
    "Need4" varchar(2),
    "FILLER_1" varchar(33)
);

CREATE TABLE reference.bolog (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Pri" varchar(1),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Log Date" varchar(8),
    "Log Time" varchar(8),
    "Call No" varchar(8),
    "FILLER" varchar(20)
);

CREATE TABLE reference.bonddebt (
    "Run Type" varchar(2),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Key Date" varchar(8),
    "Key Time" varchar(8),
    "Forename" varchar(25),
    "Surname" varchar(28),
    "Broker" varchar(5),
    "Bond No." varchar(11),
    "Bond Renewal" varchar(8),
    "Prem" varchar(10),
    "Years" varchar(1),
    "Total OS" varchar(10),
    "Bal" varchar(10),
    "Sec Amount" varchar(10),
    "Code" varchar(1),
    "Dep Name" varchar(50),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Postcode" varchar(8),
    "Order No" varchar(8),
    "Upd" varchar(1),
    "Error" varchar(2),
    "Error Message" varchar(30),
    "OPG Type" varchar(1),
    "FILLER-1" varchar(24)
);

CREATE TABLE reference.sup_activity (
    "ACT-RECORD" varchar(900),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "SupID" varchar(8),
    "DefnID" varchar(8),
    "Status" varchar(8),
    "Create by" varchar(8),
    "Date Create" varchar(8),
    "Term By" varchar(8),
    "Date Term" varchar(8),
    "Act Type" varchar(3),
    "Sup Desc" varchar(200),
    "Req" varchar(3),
    "Freq" varchar(2),
    "Lead Time" varchar(3),
    "Target Period" varchar(3),
    "Start Date" varchar(8),
    "Target" varchar(8),
    "Track Completed" varchar(8),
    "Case" varchar(8),
    "Order No" varchar(8),
    "Next Due" varchar(8),
    "Comment" varchar(500),
    "Mand Ind" varchar(1),
    "Esc Ind" varchar(1),
    "Esc Lvl" varchar(2),
    "Old Stat" varchar(8),
    "Old Start" varchar(8),
    "Stat Reason" varchar(7),
    "Old Next Due" varchar(8),
    "Old Target" varchar(8),
    "Wdays Comp" varchar(3),
    "FILLER-1" varchar(10)
);

CREATE TABLE reference.deputy (
    "RECORD" varchar(300),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "by.1" varchar(3),
    "at.1" varchar(2),
    "Deputy No" varchar(8),
    "R-TYPER" varchar(2),
    "Dep Type" varchar(2),
    "Title" varchar(2),
    "Dep Forename" varchar(25),
    "SURNAMER" varchar(40),
    "Dep Surname" varchar(40),
    "INITIALSR" varchar(3),
    "Inits" varchar(3),
    "AKA Name" varchar(40),
    "Stat" varchar(2),
    "Mobile" varchar(15),
    "Welsh" varchar(1),
    "Email" varchar(40),
    "Addr Type" varchar(1),
    "Contact Telephone" varchar(15),
    "Special" varchar(2),
    "Disch Death" varchar(8),
    "By Email" varchar(1),
    "Compliant" varchar(1),
    "Not COmpliant" varchar(8),
    "Compliant Date" varchar(8),
    "Not Comp" varchar(2),
    "Comp Reason" varchar(2),
    "Work Days" varchar(3),
    "Investigation" varchar(1),
    "VWM" varchar(2),
    "SIM" varchar(2),
    "FILLER-1" varchar(40)
);

CREATE TABLE reference.int3rdparty (
    "RECORD" varchar(450),
    "by" varchar(3),
    "by.1" varchar(3),
    "Create" varchar(8),
    "Modify" varchar(8),
    "at" varchar(2),
    "at.1" varchar(2),
    "Case" varchar(8),
    "KayDate Time" varchar(14),
    "Contact Forename" varchar(25),
    "Contact Surname" varchar(28),
    "Inits" varchar(3),
    "Contact Address 1" varchar(40),
    "Contact Address 2" varchar(40),
    "Contact Address 3" varchar(40),
    "Contact Address 4" varchar(40),
    "Contact Address 5" varchar(40),
    "Postcode" varchar(8),
    "Phone" varchar(15),
    "Type" varchar(1),
    "Contact Email" varchar(40),
    "Title" varchar(2),
    "Stat" varchar(1),
    "Personal" varchar(1),
    "Comment" varchar(27),
    "Restrict Corr" varchar(1),
    "Fin Corr" varchar(1),
    "Conf Corr" varchar(1),
    "FILLER_1" varchar(48)
);

CREATE TABLE reference.court_diary (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Loc" varchar(2),
    "Hearing" varchar(8),
    "Time" varchar(8),
    "Hear Type" varchar(2),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Hear Late" varchar(2),
    "Judge" varchar(2),
    "Outcome" varchar(2),
    "Jud. Dir" varchar(8),
    "Target1" varchar(8),
    "Target2" varchar(8),
    "Target3" varchar(8),
    "FILLER-1" varchar(8)
);

CREATE TABLE reference.applicant (
    "RECORD" varchar(500),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Partner No" varchar(8),
    "Appl Type" varchar(2),
    "Title" varchar(2),
    "Forename" varchar(25),
    "Surname" varchar(30),
    "Inits" varchar(3),
    "Sex" varchar(1),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Adrs5" varchar(40),
    "Postcode" varchar(8),
    "Addr Type" varchar(1),
    "Stat" varchar(2),
    "Corr" varchar(1),
    "Day Tele" varchar(15),
    "Evening Tele" varchar(15),
    "Mobile" varchar(15),
    "Fax" varchar(15),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Email" varchar(40),
    "Dep Type" varchar(2),
    "Fee Payer" varchar(1),
    "AKA Name" varchar(30),
    "FILLER" varchar(30)
);

CREATE TABLE reference.custtxt (
    "RECORD" varchar(560),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Name" varchar(65),
    "Corref" varchar(3),
    "Forename" varchar(25),
    "Surname" varchar(40),
    "Inits" varchar(3),
    "Contact Telephone" varchar(15),
    "Mobile" varchar(15),
    "E-Mail" varchar(40),
    "Dep Stat" varchar(2),
    "Dep Type" varchar(2),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Adrs5" varchar(40),
    "Postcode" varchar(8),
    "Addr Telephone" varchar(15),
    "DX Number" varchar(8),
    "DX Exchange" varchar(20),
    "Fax" varchar(15),
    "Addr Stat" varchar(2),
    "Account" varchar(13),
    "Fee band" varchar(2),
    "Type" varchar(1),
    "To Send" varchar(1),
    "P or A" varchar(1),
    "FILLER-1" varchar(30)
);

CREATE TABLE reference.remshist (
    "RECORD" varchar(1060),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Log Type" varchar(2),
    "Logdate" varchar(8),
    "Logtime" varchar(8),
    "Remarks" varchar(1000),
    "Sect" varchar(4),
    "Deleted" varchar(1),
    "PRIORITY" varchar(1),
    "FILLER-1" varchar(17)
);

CREATE TABLE reference.cwsdata (
    "Cwsno" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CWSDATA-REC" varchar(686),
    "Source" varchar(20),
    "KPI Type" varchar(30),
    "Date Rcvd" varchar(8),
    "Branch" varchar(20),
    "Team Ref." varchar(20),
    "Case" varchar(8),
    "Staff" varchar(3),
    "Activity1" varchar(20),
    "Act Date1" varchar(8),
    "Complete Date" varchar(8),
    "Due Date" varchar(8),
    "Due Date2" varchar(8),
    "Due Date3" varchar(8),
    "Urg" varchar(1),
    "Stat" varchar(1),
    "FOI" varchar(1),
    "Scan Date" varchar(8),
    "Docid" varchar(170),
    "Node ID" varchar(8),
    "Sender Co" varchar(40),
    "Sender Forename" varchar(25),
    "Sender Surname" varchar(40),
    "Folder" varchar(30),
    "Comments" varchar(120),
    "Form Type" varchar(34),
    "Batch" varchar(8),
    "Work Station" varchar(20),
    "WDays Rcvd" varchar(3),
    "Wdays Scan" varchar(3),
    "Alpha" varchar(1),
    "FILLER-1" varchar(4)
);

CREATE TABLE reference.patexcept (
    "RECORD" varchar(100),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Exception" varchar(2),
    "Process" varchar(40),
    "Last End Date" varchar(8),
    "Order No" varchar(8),
    "FILLER-1" varchar(8)
);

CREATE TABLE reference.panlink (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "FILLER-1" varchar(10)
);

CREATE TABLE reference.visit (
    "RECORD" varchar(800),
    "Visit No" varchar(8),
    "Case" varchar(8),
    "Priority" varchar(1),
    "Crit" varchar(6),
    "Crit Code" varchar(1),
    "FILLER" varchar(5),
    "Other Comment" varchar(30),
    "Visit Inits" varchar(6),
    "Date Allocated" varchar(8),
    "PVisit Init1" varchar(6),
    "PDate Visit1" varchar(8),
    "PVisit Init2" varchar(6),
    "PDate Visit2" varchar(8),
    "Outcome" varchar(1),
    "Fail Reason" varchar(2),
    "Outcome Comment" varchar(30),
    "Redef Stat" varchar(2),
    "Curr Stat" varchar(2),
    "Date on List" varchar(8),
    "Addr Conf Req." varchar(8),
    "Instruct Sent" varchar(8),
    "Visit Made" varchar(8),
    "Report From Visitor" varchar(8),
    "Report To CaseWrk" varchar(8),
    "Chaseup to CaseWrk" varchar(8),
    "Report from CaseWrk" varchar(8),
    "Fee Approved" varchar(8),
    "Spot Chk" varchar(1),
    "Post Recommends" varchar(4),
    "Recomm1" varchar(1),
    "Recommend Comment" varchar(30),
    "Act Taken" varchar(1),
    "Attendees" varchar(6),
    "Attend1" varchar(1),
    "Other Attend" varchar(30),
    "Comments" varchar(30),
    "by" varchar(3),
    "Create" varchar(8),
    "at" varchar(3),
    "by.1" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(3),
    "Fee Amt" varchar(3),
    "Select Date" varchar(5),
    "DueDate For Visit" varchar(5),
    "Due Return" varchar(5),
    "Due Iss to Branch" varchar(5),
    "Due Action Report" varchar(5),
    "Extension1" varchar(8),
    "Extension2" varchar(8),
    "Extension3" varchar(8),
    "Categ" varchar(5),
    "by Email" varchar(1),
    "FILLER-1" varchar(350)
);

CREATE TABLE reference.deputydup (
    "Deputy No" varchar(8),
    "Dup Deputy No" varchar(8),
    "Comment" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Done" varchar(1),
    "FILLER-1" varchar(57)
);

CREATE TABLE reference.panel_remarks (
    "RECORD" varchar(3100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Tyoe" varchar(2),
    "Log Date" varchar(8),
    "Log Time" varchar(8),
    "Remarks" varchar(3000),
    "Sect" varchar(4),
    "FILLER-1" varchar(32)
);

CREATE TABLE reference.bondnew (
    "Run Type" varchar(2),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Forename" varchar(25),
    "Surname" varchar(28),
    "Broker" varchar(5),
    "Sec Amount" varchar(10),
    "Bond No." varchar(11),
    "Bond Type" varchar(30),
    "Bond Issued" varchar(8),
    "Bond Renewal" varchar(8),
    "Order No" varchar(8),
    "Upd" varchar(1),
    "Error" varchar(2),
    "Error Message" varchar(30),
    "Trust" varchar(3),
    "FILLER-1" varchar(8)
);

CREATE TABLE reference.file_location (
    "Case" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Date" varchar(8),
    "Log Year" varchar(4),
    "Log Month" varchar(2),
    "Log Day" varchar(2),
    "Log Time" varchar(8),
    "Log Hour" varchar(2),
    "Log Mins" varchar(2),
    "Log Secs" varchar(2),
    "Location" varchar(6),
    "Floor" varchar(2),
    "Cab" varchar(2),
    "Shelf" varchar(2),
    "F/A" varchar(1),
    "Check No" varchar(3),
    "Load Date" varchar(2),
    "Load Time" varchar(8),
    "Loc Sent" varchar(1),
    "Stat" varchar(4),
    "Scan Loc" varchar(6),
    "Valid Loc" varchar(7),
    "FILLER-1" varchar(6)
);

CREATE TABLE reference.deplink (
    "RECORD" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "Main Addr" varchar(1),
    "Dep Dup" varchar(1),
    "Addr Dup" varchar(1),
    "In Use" varchar(1),
    "FILLER-1" varchar(4)
);

CREATE TABLE reference.cfoaccount (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Account No" varchar(13),
    "Type" varchar(1),
    "Usage" varchar(1),
    "Stat" varchar(1),
    "Balance" varchar(10),
    "Prev Bal" varchar(10),
    "Loaded" varchar(8),
    "FILLER-1" varchar(22)
);

CREATE TABLE reference.type3_audit (
    "RECORD" varchar(80),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Type" varchar(2),
    "Count" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Chase No" varchar(6),
    "Fee Err" varchar(8),
    "Lay" varchar(8),
    "Prof" varchar(8),
    "FILLER-1" varchar(21)
);

CREATE TABLE reference.feeaudit (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Fee Type" varchar(2),
    "First No" varchar(16),
    "Last No" varchar(16),
    "Rec Count" varchar(8),
    "Amount" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Batch No" varchar(6),
    "Dup Count" varchar(2),
    "Let Count" varchar(8),
    "FinYr" varchar(4),
    "FILLER-1" varchar(7)
);

CREATE TABLE reference.depexcept (
    "RECORD" varchar(100),
    "Deputy No" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Exception" varchar(2),
    "Process" varchar(40),
    "Dep Addr No" varchar(8),
    "FILLER-1" varchar(16)
);

CREATE TABLE reference.deputy_remarks (
    "RECORD" varchar(1100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Deputy No" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Log Date" varchar(8),
    "Log Time" varchar(8),
    "Remarks" varchar(1000),
    "Sect" varchar(4),
    "FILLER-1" varchar(32)
);

CREATE TABLE reference.prneeds (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Needs" varchar(2),
    "Level" varchar(1),
    "FILLER_1" varchar(23)
);

CREATE TABLE reference.correspmon (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Date Rcvd" varchar(8),
    "Log Time" varchar(8),
    "Respond by" varchar(8),
    "Act Response" varchar(8),
    "Req" varchar(1),
    "Target" varchar(2),
    "FILLER-1" varchar(17)
);

CREATE TABLE reference.pat (
    "RECORD" varchar(700),
    "by" varchar(3),
    "Create" varchar(8),
    "at" varchar(2),
    "by.1" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "Case" varchar(8),
    "Forename" varchar(25),
    "Surname" varchar(28),
    "Init" varchar(3),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Adrs5" varchar(40),
    "Postcode" varchar(8),
    "Client Phone" varchar(15),
    "Title" varchar(2),
    "AKA Name" varchar(30),
    "Accom Type" varchar(3),
    "Birth Yr" varchar(4),
    "Sex" varchar(1),
    "Will" varchar(1),
    "WILL" varchar(1),
    "Fee Band" varchar(2),
    "Reason" varchar(2),
    "Term Date" varchar(8),
    "Term Type" varchar(1),
    "Away Date" varchar(8),
    "Term User" varchar(3),
    "Term by" varchar(1),
    "Report Due" varchar(8),
    "Due Date" varchar(4),
    "DUEDAY" varchar(2),
    "DUEMONTH" varchar(2),
    "ENDYEAR" varchar(2),
    "Award Date" varchar(8),
    "Remis" varchar(2),
    "Exempt" varchar(2),
    "Corref" varchar(3),
    "DOB" varchar(8),
    "Marital Status" varchar(1),
    "CFO Account" varchar(9),
    "Rev Stat" varchar(3),
    "Rev Date" varchar(8),
    "Rev Init" varchar(5),
    "Rev Type" varchar(20),
    "Final Account" varchar(8),
    "Notified" varchar(8),
    "Letter Sent" varchar(8),
    "Papers Create" varchar(8),
    "Papers Completed" varchar(8),
    "Paper to Date" varchar(8),
    "Strap1" varchar(16),
    "Strap2" varchar(16),
    "Papers to Loc" varchar(7),
    "Papers to Phone" varchar(4),
    "Papers Returned" varchar(8),
    "Boxno" varchar(5),
    "Destroy" varchar(8),
    "Destruct Req" varchar(8),
    "Destruct" varchar(1),
    "Tnt Date" varchar(8),
    "Complaint" varchar(1),
    "Investigation" varchar(2),
    "Notify" varchar(2),
    "Meris No" varchar(7),
    "Area Ref" varchar(4),
    "Medical Area" varchar(4),
    "Url Node" varchar(10),
    "AppNo" varchar(2),
    "Auto Term" varchar(1),
    "Open CWS/Appl" varchar(1),
    "Was Dep" varchar(1),
    "New Account No" varchar(13),
    "Proof" varchar(1),
    "VWM" varchar(2),
    "SIM" varchar(2),
    "FILLER_1" varchar(64)
);

CREATE TABLE reference.resetpswd (
    "RECORD" varchar(80),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Logon" varchar(6),
    "Done" varchar(1),
    "Action" varchar(1),
    "Req User" varchar(6),
    "FILLER-1" varchar(40)
);

CREATE TABLE reference.order_audit (
    "RECORD" varchar(80),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Ord Type" varchar(2),
    "Count" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Chase No" varchar(6),
    "Count1" varchar(8),
    "Count2" varchar(8),
    "Fee Err" varchar(8),
    "FILLER-1" varchar(21)
);

CREATE TABLE reference.call_notes (
    "Call No" varchar(8),
    "Note Id" varchar(8),
    "Notes" varchar(1600),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "FILLER-1" varchar(108)
);

CREATE TABLE reference.ordercop (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Order No" varchar(8),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Status" varchar(8),
    "Ord Type" varchar(2),
    "Made Date" varchar(8),
    "Issue Date" varchar(8),
    "Judge" varchar(2),
    "FILLER-1" varchar(28)
);

CREATE TABLE reference.pantemp (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Panel No" varchar(8),
    "Sortid" varchar(4),
    "Batch No." varchar(8),
    "Sort Code" varchar(12),
    "Sortpv" varchar(1),
    "Pcount" varchar(4),
    "Vcount" varchar(4),
    "FILLER_1" varchar(6)
);

CREATE TABLE reference.feeexport (
    "RECORD" varchar(200),
    "Batch No" varchar(6),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Invoice Date" varchar(8),
    "Due Date" varchar(8),
    "Invoice No" varchar(10),
    "Ref 2" varchar(10),
    "Amount" varchar(8),
    "Vat Amount" varchar(8),
    "GL Code" varchar(16),
    "Line Amount" varchar(8),
    "Cust Ref" varchar(20),
    "Service Code" varchar(20),
    "GL Ind" varchar(10),
    "Sage No" varchar(8),
    "Asmt Lvl" varchar(2),
    "FinYr" varchar(4),
    "FILLER-1" varchar(20)
);

CREATE TABLE reference.dephist (
    "RECORD" varchar(300),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "by.1" varchar(3),
    "at.1" varchar(2),
    "Deputy No" varchar(8),
    "Dep Type" varchar(2),
    "Title" varchar(2),
    "Dep Forename" varchar(25),
    "Dep Surname" varchar(40),
    "Inits" varchar(3),
    "AKA Name" varchar(40),
    "Stat" varchar(2),
    "Mobile" varchar(15),
    "Welsh" varchar(1),
    "Email" varchar(40),
    "Addr Type" varchar(1),
    "Telephone" varchar(15),
    "Special" varchar(2),
    "Disch Death" varchar(8),
    "By Email" varchar(1),
    "Compliant" varchar(1),
    "Not Compliant" varchar(8),
    "Compliant Date" varchar(8),
    "Not Comp" varchar(2),
    "Comp Reason" varchar(2),
    "Work Days" varchar(3),
    "Investigation" varchar(1),
    "VWM" varchar(2),
    "SIM" varchar(2),
    "FILLER-1" varchar(40)
);

CREATE TABLE reference.contact (
    "RECORD" varchar(620),
    "Case" varchar(8),
    "KeyDateTime" varchar(14),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "C Forename" varchar(25),
    "C Surname" varchar(40),
    "Inits" varchar(3),
    "C Adrs1" varchar(40),
    "C Adrs2" varchar(40),
    "C Adrs3" varchar(40),
    "C Adrs4" varchar(40),
    "C Adrs5" varchar(40),
    "Postcode" varchar(8),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Phone" varchar(15),
    "Mobile" varchar(15),
    "Email" varchar(40),
    "CoType" varchar(1),
    "Title" varchar(2),
    "Status" varchar(1),
    "Personal" varchar(1),
    "Sols Ref" varchar(50),
    "Relationship" varchar(60),
    "Comments" varchar(60),
    "Letter Sent" varchar(1),
    "FILLER-1" varchar(22)
);

CREATE TABLE reference.deputy_address (
    "RECORD" varchar(350),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Dep Addr No" varchar(8),
    "Dep Adrs1" varchar(40),
    "Dep Adrs2" varchar(40),
    "Dep Adrs3" varchar(40),
    "Dep Adrs4" varchar(40),
    "Dep Adrs5" varchar(40),
    "Dep Postcode" varchar(8),
    "Telephone" varchar(15),
    "Tel Ext." varchar(4),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Addr Stat" varchar(2),
    "Fax" varchar(15),
    "FILLER-1" varchar(44)
);

CREATE TABLE reference.order_chase (
    "RECORD" varchar(80),
    "Order No" varchar(8),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Chase No" varchar(6),
    "Expiry Date" varchar(8),
    "Chase1" varchar(1),
    "Chase2" varchar(1),
    "Chase Term" varchar(1),
    "FILLER-1" varchar(21)
);

CREATE TABLE reference.calls (
    "RECORD" varchar(600),
    "Call No" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Secs" varchar(4),
    "Save Date" varchar(8),
    "Save Time" varchar(2),
    "Title" varchar(2),
    "Forename" varchar(30),
    "Surname" varchar(30),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Adrs5" varchar(40),
    "Postcode" varchar(8),
    "Telephone" varchar(15),
    "Keyword" varchar(30),
    "QType" varchar(2),
    "Forms Sent" varchar(8),
    "Amt Code" varchar(2),
    "Forms Due" varchar(8),
    "Form Req" varchar(1),
    "Forms O/S" varchar(1),
    "Form Comp" varchar(1),
    "Actions" varchar(2),
    "Where" varchar(2),
    "Leaflet" varchar(2),
    "Aware" varchar(1),
    "Pens Ben" varchar(1),
    "Exists" varchar(1),
    "Case" varchar(8),
    "Meris No" varchar(8),
    "Sec Val" varchar(1),
    "Prev Aware" varchar(1),
    "Comp" varchar(1),
    "Log Time" varchar(8),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Copies" varchar(4),
    "Rcvr" varchar(1),
    "Cpd Ind" varchar(1),
    "RTP Ind" varchar(1),
    "FILLER-1" varchar(145)
);

CREATE TABLE reference.depaddrhist (
    "RECORD" varchar(350),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Dep Addr No" varchar(8),
    "D Adrs1" varchar(40),
    "D Adrs2" varchar(40),
    "D Adrs3" varchar(40),
    "D Adrs4" varchar(40),
    "D Adrs5" varchar(40),
    "Postcode" varchar(8),
    "Phone" varchar(15),
    "Tele Ext" varchar(4),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Stat" varchar(2),
    "Fax" varchar(15),
    "FILLER-1" varchar(44)
);

CREATE TABLE reference.activity_tracking (
    "RECORD" varchar(810),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Track Id" varchar(8),
    "Sup ID" varchar(8),
    "Defn ID" varchar(8),
    "Status" varchar(11),
    "Date Created" varchar(8),
    "Comp Target Date" varchar(8),
    "Notused1" varchar(8),
    "Notused2" varchar(40),
    "Notused3" varchar(60),
    "Outcome" varchar(1),
    "Invcreate" varchar(8),
    "Notused4" varchar(35),
    "Action by" varchar(3),
    "Further" varchar(2),
    "Follow Target" varchar(8),
    "Date Completed" varchar(8),
    "Start Date" varchar(8),
    "Invstart" varchar(8),
    "Case" varchar(8),
    "Order No" varchar(8),
    "Comment" varchar(500),
    "FILLER_1" varchar(28)
);

CREATE TABLE reference.ordersupcase (
    "Case" varchar(8),
    "Fin Cnt" varchar(2),
    "Fin Act Cnt" varchar(2),
    "HW Cnt" varchar(2),
    "HW Act Cnt" varchar(2),
    "FP Cnt" varchar(2),
    "FP Deputy No" varchar(8),
    "FP Dep Addr No" varchar(8),
    "End Date" varchar(8),
    "Lodge Date" varchar(8),
    "Review Date" varchar(8),
    "Visit Date" varchar(8),
    "Old Visit Date" varchar(8),
    "Activity Date" varchar(8),
    "Assess Date" varchar(8),
    "Chase Date" varchar(8),
    "Old Review" varchar(8),
    "Old Visit" varchar(8),
    "Old OldVisit" varchar(8),
    "Old Activity" varchar(8),
    "OlD Assess" varchar(8),
    "Old Chase" varchar(8),
    "Visit OS" varchar(2),
    "Old Visit OS" varchar(2),
    "Risk Cnt" varchar(2),
    "Curr Cnt" varchar(2),
    "Clos Cnt" varchar(2),
    "Supe Cnt" varchar(2),
    "Sche Cnt" varchar(2),
    "First Asmt" varchar(1),
    "Incl Act" varchar(1),
    "High Lvl" varchar(2),
    "Clos High" varchar(2),
    "Supe High" varchar(2),
    "PA Lvl" varchar(2),
    "PA Lvl1" varchar(2),
    "PA Lvl2" varchar(2),
    "PA Lvl3" varchar(2),
    "PA Date" varchar(8),
    "PA Date1" varchar(8),
    "PA Date2" varchar(8),
    "PA Date3" varchar(8),
    "HW Lvl" varchar(2),
    "HW Lvl1" varchar(2),
    "HW Lvl2" varchar(2),
    "HW Lvl3" varchar(2),
    "HW Date" varchar(8),
    "HW Date1" varchar(8),
    "HW Date2" varchar(8),
    "HW Date3" varchar(8),
    "FAct Order" varchar(8),
    "Report No" varchar(8),
    "Late Act Date1" varchar(8),
    "Late Act Date2" varchar(8),
    "Late Act Date3" varchar(8),
    "Old Act Date1" varchar(8),
    "Old Act Date2" varchar(8),
    "Old Act Date3" varchar(8),
    "Late Vis Date1" varchar(8),
    "Late Vis Date2" varchar(8),
    "Late Vis Date3" varchar(8),
    "Old Vis Date1" varchar(8),
    "Old Vis Date2" varchar(8),
    "Old Vis Date3" varchar(8),
    "Late Acc Date1" varchar(8),
    "Late Acc Date2" varchar(8),
    "Late Acc Date3" varchar(8),
    "Old Acc Date1" varchar(8),
    "Old Acc Date2" varchar(8),
    "Old Acc Date3" varchar(8),
    "Late Asmt Date1" varchar(8),
    "Late Asmt Date2" varchar(8),
    "Late Asmt Date3" varchar(8),
    "Old Asmt Date1" varchar(8),
    "Old Asmt Date2" varchar(8),
    "Old Asmt Date3" varchar(8),
    "Late OrdExp Date1" varchar(8),
    "Late OrdExp Date2" varchar(8),
    "Late OrdExp Date3" varchar(8),
    "Old OrdExp Date1" varchar(8),
    "Old OrdExp Date2" varchar(8),
    "Old OrdExp Date3" varchar(8),
    "KPI3 Late1" varchar(8),
    "KPI3 Late2" varchar(8),
    "KPI3 Late3" varchar(8),
    "KPI3 Late4" varchar(8),
    "KPI3 Late Typ1" varchar(2),
    "KPI3 Late Typ2" varchar(2),
    "KPI3 Late Typ3" varchar(2),
    "KPI3 Late Typ4" varchar(2),
    "KPI3 Old1" varchar(8),
    "KPI3 Old2" varchar(8),
    "KPI3 Old3" varchar(8),
    "KPI3 Old4" varchar(8),
    "KPI3 Old Typ1" varchar(2),
    "KPI3 Old Typ2" varchar(2),
    "KPI3 Old Typ3" varchar(2),
    "KPI3 Old Typ4" varchar(2),
    "Caseload Date" varchar(8),
    "FILLER-1" varchar(8)
);

CREATE TABLE reference.merisdebt (
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Meris Case" varchar(8),
    "KEYDATE" varchar(8),
    "KEYTIME" varchar(8),
    "Client Name" varchar(60),
    "Meris Forename" varchar(25),
    "Meris Surname" varchar(28),
    "Balance" varchar(10),
    "Inv Date" varchar(8),
    "Invoice No" varchar(10),
    "Due Date" varchar(8),
    "Aged" varchar(6),
    "Div" varchar(6),
    "Error" varchar(2),
    "Error Message" varchar(30),
    "OPG Type" varchar(4),
    "FILLER-1" varchar(18)
);

CREATE TABLE reference.risk_del (
    "RECORD" varchar(1406),
    "Asmt ID" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Order No" varchar(8),
    "Date Create" varchar(8),
    "Invcreate" varchar(8),
    "Date Complete" varchar(8),
    "Start Date" varchar(8),
    "Status" varchar(10),
    "Assessor" varchar(3),
    "Auto Ind" varchar(6),
    "Asmt Lvl" varchar(2),
    "Setter ID" varchar(3),
    "Rate Ovr Flag" varchar(1),
    "Override Date" varchar(8),
    "Override Comment" varchar(1106),
    "Ovr ID" varchar(3),
    "Next Asmt Date" varchar(8),
    "New Asmt Date" varchar(8),
    "Reason New" varchar(50),
    "New Set ID" varchar(3),
    "Next Created" varchar(1),
    "Appeal" varchar(1),
    "Order Made" varchar(8),
    "U Cnt" int,
    "X Cnt" int,
    "AB Cnt" int,
    "C Cnt" int,
    "DE Cnt" int,
    "Y Cnt" int,
    "N Cnt" int,
    "Old Stat" varchar(10),
    "Curr State Date" varchar(8),
    "OV Reason" varchar(2),
    "FILLER-1" varchar(69)
);

CREATE TABLE reference.type3_chase (
    "RECORD" varchar(80),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Chase No" varchar(6),
    "Review Sent" varchar(8),
    "Chase1" varchar(1),
    "FILLER-1" varchar(31)
);

CREATE TABLE reference.remarks (
    "RECORD" varchar(1100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Logdate" varchar(8),
    "Logtime" varchar(8),
    "Remarks" varchar(1000),
    "Call No" varchar(8),
    "Sect" varchar(4),
    "Pri" varchar(1),
    "FILLER-1" varchar(23)
);

CREATE TABLE reference.applhistory (
    "RECORD" varchar(180),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Appl Type" varchar(2),
    "App Date" varchar(8),
    "P-S" varchar(1),
    "Status" varchar(2),
    "Location" varchar(6),
    "Flr" varchar(2),
    "Cab" varchar(2),
    "Shelf" varchar(2),
    "Loc Date" varchar(8),
    "Loc Time" varchar(8),
    "Fee Paid" varchar(1),
    "App Issue" varchar(8),
    "Outcome" varchar(2),
    "Perm Rqd" varchar(1),
    "Ack Rcvd" varchar(1),
    "Sec Rcvd" varchar(8),
    "Sec Req" varchar(1),
    "Close Date" varchar(8),
    "Appl Term" varchar(2),
    "Serv Comp" varchar(1),
    "Status Date" varchar(8),
    "FILLER-1" varchar(83)
);

CREATE TABLE reference.account (
    "RECORD" varchar(440),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Case" varchar(8),
    "Acc Ind" varchar(1),
    "End Date" varchar(8),
    "Lodge Date" varchar(8),
    "Followup Date" varchar(8),
    "Further Code" varchar(2),
    "Review Date" varchar(8),
    "Rcvd Date" varchar(8),
    "Type" varchar(1),
    "Late Reason" varchar(1),
    "Revise Date" varchar(8),
    "Review by" varchar(3),
    "Rev Stat" varchar(1),
    "Review Code" varchar(2),
    "Init" varchar(3),
    "Next Yr" varchar(1),
    "Annual Sent" varchar(8),
    "Chase 1" varchar(8),
    "Chase 2" varchar(8),
    "Review Chase" varchar(8),
    "Further Date" varchar(8),
    "Further Date1" varchar(8),
    "Further Date2" varchar(8),
    "Further Date3" varchar(8),
    "Further Date4" varchar(8),
    "Further Date6" varchar(8),
    "Further Date6.1" varchar(8),
    "Sent" varchar(8),
    "Sent1" varchar(8),
    "Sent2" varchar(8),
    "Sent3" varchar(8),
    "Sent4" varchar(8),
    "Sent5" varchar(8),
    "Sent6" varchar(8),
    "Further" varchar(2),
    "Further1" varchar(2),
    "Further2" varchar(2),
    "Further3" varchar(2),
    "Further4" varchar(2),
    "Further5" varchar(2),
    "Further6" varchar(2),
    "Rcvd Date.1" varchar(8),
    "Rcvd Date1" varchar(8),
    "Rcvd Date2" varchar(8),
    "Rcvd Date3" varchar(8),
    "Rcvd Date4" varchar(8),
    "Rcvd Date5" varchar(8),
    "Rcvd Date6" varchar(8),
    "Chase1" varchar(8),
    "Chase11" varchar(8),
    "Chase21" varchar(8),
    "Chase31" varchar(8),
    "Chase41" varchar(8),
    "Chase51" varchar(8),
    "Chase61" varchar(8),
    "Chase2" varchar(8),
    "Chase12" varchar(8),
    "Chase22" varchar(8),
    "Chase32" varchar(8),
    "Chase42" varchar(8),
    "Chase52" varchar(8),
    "Chase62" varchar(8),
    "WDays Lodge" varchar(3),
    "WDays Review" varchar(3),
    "WDays Rcvd" varchar(3),
    "WRDays Lodge" varchar(3),
    "WRDays Review" varchar(3),
    "W4Days Lodge" varchar(3),
    "W4Days Review" varchar(3),
    "FILLER-1" varchar(38)
);

CREATE TABLE reference.sletters (
    "RECORD" varchar(140),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Case" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Log Type" varchar(2),
    "Logdate" varchar(8),
    "Logtime" varchar(8),
    "Doc Type" varchar(30),
    "Desc" varchar(30),
    "FILLER-1" varchar(29)
);

CREATE TABLE reference.cwshistory (
    "RECORD" varchar(720),
    "CWSNo" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "CWSDATA-REC" varchar(699),
    "Source" varchar(20),
    "KPI Type" varchar(30),
    "Date Rcvd" varchar(8),
    "Branch" varchar(20),
    "Team" varchar(20),
    "Case" varchar(8),
    "Staff" varchar(3),
    "Activity1" varchar(20),
    "Act Date1" varchar(8),
    "Complete Date" varchar(8),
    "Due Date" varchar(8),
    "Due Date2" varchar(8),
    "Due Date3" varchar(8),
    "Urg" varchar(1),
    "Stat" varchar(1),
    "FOI" varchar(1),
    "Scan Date" varchar(8),
    "Docid" varchar(170),
    "Node id" varchar(8),
    "Sender Co" varchar(40),
    "Sender Forename" varchar(25),
    "Sender Surname" varchar(40),
    "Folder" varchar(30),
    "Comments" varchar(120),
    "FILLER-1" varchar(86)
);

CREATE TABLE reference.orderasmt (
    "Case" varchar(8),
    "Order No" varchar(8),
    "Count" varchar(2),
    "Date Inverse" varchar(8),
    "Cwsno" varchar(8),
    "Date Created" varchar(8),
    "Start Date" varchar(8),
    "Date Complete" varchar(8),
    "Asmt Lvl" varchar(2),
    "Rcvd Days" varchar(4),
    "Asmt Days" varchar(4),
    "FILLER-1" varchar(6)
);

CREATE TABLE reference.repvis (
    "RECORD" varchar(460),
    "by" varchar(3),
    "Create" varchar(8),
    "at" varchar(3),
    "by.1" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(3),
    "Report No" varchar(8),
    "Case" varchar(8),
    "Req By" varchar(2),
    "Rep On" varchar(1),
    "Report Type" varchar(2),
    "Reason Code" varchar(2),
    "Source" varchar(2),
    "Visitor" varchar(6),
    "Date Allocated" varchar(8),
    "Prev Visitor" varchar(6),
    "Prev Allocated" varchar(8),
    "Prev2 Visitor" varchar(6),
    "Prev2 Allocted" varchar(8),
    "Commission Dated" varchar(8),
    "Commission Issued" varchar(8),
    "Report Due" varchar(8),
    "Report Rcvd." varchar(8),
    "Outcome" varchar(1),
    "Reason" varchar(2),
    "Outcome Comment" varchar(30),
    "Fee Approved" varchar(8),
    "Recomms" varchar(4),
    "Recom1" varchar(1),
    "Recomm Comment" varchar(30),
    "Attendees" varchar(6),
    "Att1" varchar(1),
    "Other Attendee" varchar(30),
    "Comments" varchar(30),
    "Fee Amount" varchar(3),
    "Categ" varchar(5),
    "Email" varchar(1),
    "Review" varchar(2),
    "Judge" varchar(2),
    "Deputy No" varchar(8),
    "Dep Addr No" varchar(8),
    "Area" varchar(5),
    "Quest" varchar(1),
    "S49 Date" varchar(8),
    "Partner No" varchar(8),
    "Asmt Lvl" varchar(2),
    "Extension 1" varchar(8),
    "Extension 2" varchar(8),
    "Fee band" varchar(2),
    "Rep Xref" varchar(8),
    "Review Date" varchar(8),
    "Rev By" varchar(3),
    "Fee Ref" varchar(6),
    "FILLER-1" varchar(36)
);

CREATE TABLE reference.prexpertise (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Expertise" varchar(2),
    "Level" varchar(1),
    "FILLER_1" varchar(23)
);

CREATE TABLE reference.account_audit (
    "RECORD" varchar(100),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Acc Type" varchar(2),
    "First No" varchar(8),
    "Last No" varchar(8),
    "Count" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Chase No" varchar(6),
    "Count1" varchar(8),
    "Count2" varchar(8),
    "Count3" varchar(8),
    "CWS OS" varchar(8),
    "Errors" varchar(8),
    "FILLER-1" varchar(13)
);

CREATE TABLE reference.assessment_rev (
    "REV-RECORD" varchar(400),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Rev ID" varchar(8),
    "Asmt ID" varchar(8),
    "Received Date" varchar(8),
    "Requested Date" varchar(8),
    "Reviewer" varchar(60),
    "Due Date" varchar(8),
    "Published Date" varchar(8),
    "1st Result" varchar(60),
    "2nd Review Date" varchar(8),
    "Adjudication Date" varchar(8),
    "Adjudicator" varchar(60),
    "Adjudocation Date" varchar(8),
    "2nd Result" varchar(60),
    "OPG Sent" varchar(8),
    "Rev Status" varchar(3),
    "SLA Rev Date" varchar(8),
    "SLA Comm Date" varchar(8),
    "SLA2 Rev Date" varchar(8),
    "SLA2 Comm Date" varchar(8),
    "FILLER-1" varchar(19)
);

CREATE TABLE reference.hsbclog (
    "RECORD" varchar(50),
    "Case" varchar(8),
    "Rep Type" varchar(2),
    "Date Recorded" varchar(8),
    "Old Corref" varchar(3),
    "New Corref" varchar(3),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "New Reptype" varchar(2),
    "Old Term Date" varchar(8),
    "FILLER-1" varchar(3)
);

CREATE TABLE reference.setuperr (
    "RECORD" varchar(75),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Order No" varchar(8),
    "Err Flag" varchar(1),
    "FILLER-1" varchar(30)
);

CREATE TABLE reference.prskills (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Skill" varchar(2),
    "Level" varchar(1),
    "FILLER_1" varchar(23)
);

CREATE TABLE reference.prlang (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Lang" varchar(2),
    "Level" varchar(1),
    "FILLER_1" varchar(23)
);

CREATE TABLE reference.prgeoarea (
    "RECORD" varchar(60),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Geo Area" varchar(2),
    "Level" varchar(1),
    "FILLER_1" varchar(23)
);

CREATE TABLE reference.account_chase (
    "RECORD" varchar(100),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Chase No" varchar(6),
    "End Date" varchar(8),
    "Chase" varchar(1),
    "Chase 1" varchar(1),
    "Chase 2" varchar(1),
    "ChaseR" varchar(1),
    "Follow" varchar(1),
    "Cwsno" varchar(8),
    "CWS o/s" varchar(1),
    "FILLER-1" varchar(38)
);

CREATE TABLE reference.panel_audit (
    "RECORD" varchar(150),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Keydate" varchar(8),
    "Keytime" varchar(8),
    "Due Date" varchar(8),
    "Completed Date" varchar(8),
    "Type" varchar(1),
    "Outcome" varchar(2),
    "Followup Date" varchar(8),
    "Info Req." varchar(1),
    "FILLER-1" varchar(74)
);

CREATE TABLE reference.ra_batch_newassess (
    "RECORD" varchar(110),
    "RA Batchno" varchar(8),
    "Date Created" varchar(8),
    "Time Create" varchar(8),
    "Invdate" varchar(8),
    "Invtime" varchar(8),
    "Date To" varchar(8),
    "Picked" varchar(2),
    "Skipped" varchar(2),
    "Run Type" varchar(1),
    "Adv Days" varchar(2),
    "Comp" varchar(1),
    "FILLER-1" varchar(58)
);

CREATE TABLE reference.order (
    "RECORD" varchar(240),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Order No" varchar(8),
    "CoP Case" varchar(10),
    "Case" varchar(8),
    "AppNo" varchar(2),
    "Ord Stat" varchar(8),
    "Ord Type" varchar(2),
    "Made Date" varchar(8),
    "Issue Date" varchar(8),
    "Fee Rqd" varchar(1),
    "Bond Rqd" varchar(1),
    "Dep App" varchar(1),
    "Spvn Received" varchar(8),
    "Expiry Date" varchar(8),
    "Judge" varchar(2),
    "Clause Expiry" varchar(8),
    "Chase1" varchar(8),
    "Chase2" varchar(8),
    "Chs Ind" varchar(2),
    "Bond Co" varchar(2),
    "Bond No." varchar(11),
    "Bond Amount" varchar(3),
    "Bond Renewal" varchar(8),
    "Bond Discharge" varchar(8),
    "Bondc" varchar(1),
    "Bondyy" varchar(2),
    "Ord Risk Lvl" varchar(2),
    "Asmt Cre" varchar(1),
    "Acc Rev" varchar(1),
    "Init AccRev" varchar(2),
    "Old Stat" varchar(8),
    "Last Rev" varchar(4),
    "Review Set" varchar(8),
    "Bond Pay Type" varchar(30),
    "Bond OS" varchar(1),
    "FILLER-1" varchar(31)
);

CREATE TABLE reference.risk_assessment_aud (
    "RECORD" varchar(1200),
    "Case" varchar(8),
    "Order No" varchar(8),
    "Asmt ID" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Old Asmt Lvl" varchar(2),
    "Override Date" varchar(8),
    "Ovr ID" varchar(3),
    "Override Comment" varchar(1106),
    "New Asmt Lvl" varchar(2),
    "Ovr Reason" varchar(2),
    "FILLER" varchar(40)
);

CREATE TABLE reference.riskcase (
    "Case" varchar(8),
    "Asmt ID" varchar(8),
    "Done" varchar(1),
    "High Lvl" varchar(2),
    "Order No" varchar(8),
    "Asmt Start Date" varchar(8),
    "Fin Count" varchar(2),
    "Fin Act Cnt" varchar(2),
    "HW Count" varchar(2),
    "HW Act Cnt" varchar(2),
    "FP Count" varchar(2),
    "FP Deputy No" varchar(8),
    "FP Dep Addr No" varchar(8),
    "FP Order No" varchar(8),
    "FILLER-1" varchar(31)
);

CREATE TABLE reference.pataudit (
    "RECORD" varchar(150),
    "Case" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Away Date" varchar(8),
    "Term Date" varchar(8),
    "ID Screen" varchar(20),
    "Term Type" varchar(1),
    "Notify Code" varchar(2),
    "Term By" varchar(1),
    "Notify Date" varchar(8),
    "Letter Sent" varchar(8),
    "Final Account" varchar(8),
    "FILLER-1" varchar(65)
);

CREATE TABLE reference.panrec (
    "RECORD" varchar(600),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Panel No" varchar(8),
    "Surnamer" varchar(40),
    "Surname" varchar(40),
    "Forename" varchar(25),
    "Initsr" varchar(3),
    "Inits" varchar(3),
    "Title" varchar(2),
    "AKA Name" varchar(40),
    "Type" varchar(1),
    "Status" varchar(2),
    "Email" varchar(40),
    "Mobile" varchar(15),
    "Telephone" varchar(15),
    "Day Tele" varchar(15),
    "Fax" varchar(15),
    "adrs1r" varchar(40),
    "Adrs1" varchar(40),
    "Adrs2" varchar(40),
    "Adrs3" varchar(40),
    "Adrs4" varchar(40),
    "Adrs5" varchar(40),
    "Postcode" varchar(8),
    "DX No" varchar(8),
    "DX Exchange" varchar(20),
    "Addr Type" varchar(1),
    "Appoint Date" varchar(8),
    "Removal Date" varchar(8),
    "Category" varchar(5),
    "Urlnode" varchar(10),
    "Removal" varchar(3),
    "Old Categ" varchar(5),
    "FILLER_1" varchar(77)
);

CREATE TABLE reference.patdup (
    "Case" varchar(8),
    "Dup Case" varchar(8),
    "Comment" varchar(50),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "FILLER-1" varchar(58)
);

CREATE TABLE reference.risks_assessed (
    "RECORD" varchar(200),
    "Asmt Id" varchar(8),
    "Crit Id" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Crit Type" varchar(3),
    "Crit Categ" varchar(3),
    "Criteria Name" varchar(50),
    "Desc" varchar(40),
    "Weighting" int,
    "Range" int,
    "Score" varchar(1),
    "Help file" varchar(30),
    "Cat Ver Date" varchar(8),
    "Cat Ver Time" varchar(8),
    "Sort" varchar(4),
    "FILLER-1" varchar(9)
);

CREATE TABLE reference.risks_del (
    "RECORD" varchar(200),
    "Asmt Id" varchar(8),
    "Crit Id" varchar(8),
    "Create" varchar(8),
    "at" varchar(2),
    "by" varchar(3),
    "Modify" varchar(8),
    "at.1" varchar(2),
    "by.1" varchar(3),
    "Crit Type" varchar(3),
    "Crit Categ" varchar(3),
    "Criteria Name" varchar(50),
    "Desc" varchar(40),
    "Weighting" int,
    "Range" int,
    "Score" varchar(1),
    "Help file" varchar(30),
    "Cat Ver Date" varchar(8),
    "Cat Ver Time" varchar(8),
    "Sort" varchar(4),
    "FILLER-1" varchar(9)
);

ALTER TABLE reference.account ADD CONSTRAINT unique_account_case UNIQUE ("Case");
ALTER TABLE reference.account_chase ADD CONSTRAINT unique_account_chase_case UNIQUE ("Case");
ALTER TABLE reference.appl ADD CONSTRAINT unique_appl_cop_case UNIQUE ("CoP Case");
ALTER TABLE reference.appl ADD CONSTRAINT unique_appl_case UNIQUE ("Case");
ALTER TABLE reference.applhistory ADD CONSTRAINT unique_applhistory_cop_case UNIQUE ("CoP Case");
ALTER TABLE reference.applhistory ADD CONSTRAINT unique_applhistory_case UNIQUE ("Case");
ALTER TABLE reference.applicant ADD CONSTRAINT unique_applicant_partner_no UNIQUE ("Partner No");
ALTER TABLE reference.applicantdup ADD CONSTRAINT unique_applicantdup_partner_no UNIQUE ("Partner No");
ALTER TABLE reference.applink ADD CONSTRAINT unique_applink_case UNIQUE ("Case");
ALTER TABLE reference.appl_location ADD CONSTRAINT unique_appl_location_case UNIQUE ("Case");
ALTER TABLE reference.bonddebt ADD CONSTRAINT unique_bonddebt_order_no UNIQUE ("Order No");
ALTER TABLE reference.bonddebt ADD CONSTRAINT unique_bonddebt_case UNIQUE ("Case");
ALTER TABLE reference.bondnew ADD CONSTRAINT unique_bondnew_order_no UNIQUE ("Order No");
ALTER TABLE reference.bondnew ADD CONSTRAINT unique_bondnew_case UNIQUE ("Case");
ALTER TABLE reference.calls ADD CONSTRAINT unique_calls_call_no UNIQUE ("Call No");
ALTER TABLE reference.calls ADD CONSTRAINT unique_calls_case UNIQUE ("Case");
ALTER TABLE reference.cfoaccount ADD CONSTRAINT unique_cfoaccount_case UNIQUE ("Case");
ALTER TABLE reference.cfoload ADD CONSTRAINT unique_cfoload_case UNIQUE ("OPG Case");
ALTER TABLE reference.contact ADD CONSTRAINT unique_contact_case UNIQUE ("Case");
ALTER TABLE reference.court_diary ADD CONSTRAINT unique_court_diary_cop_case UNIQUE ("CoP Case");
ALTER TABLE reference.cwsdata ADD CONSTRAINT unique_cwsdata_case UNIQUE ("Case");
ALTER TABLE reference.cwshistory ADD CONSTRAINT unique_cwshistory_case UNIQUE ("Case");
ALTER TABLE reference.deplink ADD CONSTRAINT unique_deplink_dep_addr_no UNIQUE ("Dep Addr No");
ALTER TABLE reference.deputy ADD CONSTRAINT unique_deputy_deputy_no UNIQUE ("Deputy No");
ALTER TABLE reference.deputyaddrdup ADD CONSTRAINT unique_deputyaddrdup_dep_addr_no UNIQUE ("Dep Addr No");
ALTER TABLE reference.deputydup ADD CONSTRAINT unique_deputydup_deputy_no UNIQUE ("Deputy No");
ALTER TABLE reference.deputyship ADD CONSTRAINT unique_deputyship_dep_addr_no UNIQUE ("Dep Addr No");
ALTER TABLE reference.deputyship ADD CONSTRAINT unique_deputyship_deputy_no UNIQUE ("Deputy No");
ALTER TABLE reference.deputyship ADD CONSTRAINT unique_deputyship_order_no UNIQUE ("Order No");
ALTER TABLE reference.deputyship ADD CONSTRAINT unique_deputyship_case UNIQUE ("Case");
ALTER TABLE reference.deputy_address ADD CONSTRAINT unique_deputy_address_dep_addr_no UNIQUE ("Dep Addr No");
ALTER TABLE reference.feeaas ADD CONSTRAINT unique_feeaas_deputy_no UNIQUE ("Deputy No");
ALTER TABLE reference.feeaas ADD CONSTRAINT unique_feeaas_dep_addr_no UNIQUE ("Dep Addr No");
ALTER TABLE reference.feeaas ADD CONSTRAINT unique_feeaas_order_no UNIQUE ("Order No");
ALTER TABLE reference.feeaas ADD CONSTRAINT unique_feeaas_case UNIQUE ("Case");
ALTER TABLE reference.feedebt ADD CONSTRAINT unique_feedebt_case UNIQUE ("Case");
ALTER TABLE reference.file_location ADD CONSTRAINT unique_file_location_case UNIQUE ("Case");
ALTER TABLE reference.hsbclog ADD CONSTRAINT unique_hsbclog_case UNIQUE ("Case");
ALTER TABLE reference.kpidata ADD CONSTRAINT unique_kpidata_case UNIQUE ("Case");
ALTER TABLE reference.merisdebt ADD CONSTRAINT unique_merisdebt_case UNIQUE ("Meris Case");
ALTER TABLE reference.newfee ADD CONSTRAINT unique_newfee_partner_no UNIQUE ("Partner No");
ALTER TABLE reference.newfee ADD CONSTRAINT unique_newfee_case UNIQUE ("Case");
ALTER TABLE reference.order ADD CONSTRAINT unique_order_case UNIQUE ("Case");
ALTER TABLE reference.order ADD CONSTRAINT unique_order_cop_case UNIQUE ("CoP Case");
ALTER TABLE reference.order ADD CONSTRAINT unique_order_order_no UNIQUE ("Order No");
ALTER TABLE reference.ordercop ADD CONSTRAINT unique_ordercop_cop_case UNIQUE ("CoP Case");
ALTER TABLE reference.ordercop ADD CONSTRAINT unique_ordercop_case UNIQUE ("Case");
ALTER TABLE reference.orderhistory ADD CONSTRAINT unique_orderhistory_case UNIQUE ("Case");
ALTER TABLE reference.order_chase ADD CONSTRAINT unique_order_chase_case UNIQUE ("Case");
ALTER TABLE reference.panrec ADD CONSTRAINT unique_panrec_panel_no UNIQUE ("Panel No");
ALTER TABLE reference.pat ADD CONSTRAINT unique_pat_case UNIQUE ("Case");
ALTER TABLE reference.patdup ADD CONSTRAINT unique_patdup_case UNIQUE ("Case");
ALTER TABLE reference.patstats ADD CONSTRAINT unique_patstats_case UNIQUE ("Case");
ALTER TABLE reference.pletters ADD CONSTRAINT unique_pletters_panel_no UNIQUE ("Panel No");
ALTER TABLE reference.remarks ADD CONSTRAINT unique_remarks_call_no UNIQUE ("Call No");
ALTER TABLE reference.remarks ADD CONSTRAINT unique_remarks_case UNIQUE ("Case");
ALTER TABLE reference.remshist ADD CONSTRAINT unique_remshist_case UNIQUE ("Case");
ALTER TABLE reference.repvis ADD CONSTRAINT unique_repvis_case UNIQUE ("Case");
ALTER TABLE reference.risks_assessed ADD CONSTRAINT unique_risks_assessed_asmt_id UNIQUE ("Asmt Id");
ALTER TABLE reference.risks_del ADD CONSTRAINT unique_risks_del_asmt_id UNIQUE ("Asmt Id");
ALTER TABLE reference.risk_assessment ADD CONSTRAINT unique_risk_assessment_asmt_id UNIQUE ("Asmt Id");
ALTER TABLE reference.risk_assessment ADD CONSTRAINT unique_risk_assessment_order_no UNIQUE ("Order No");
ALTER TABLE reference.risk_del ADD CONSTRAINT unique_risk_del_asmt_id UNIQUE ("Asmt ID");
ALTER TABLE reference.risk_del ADD CONSTRAINT unique_risk_del_order_no UNIQUE ("Order No");
ALTER TABLE reference.setuperr ADD CONSTRAINT unique_setuperr_order_no UNIQUE ("Order No");
ALTER TABLE reference.setuperr ADD CONSTRAINT unique_setuperr_case UNIQUE ("Case");
ALTER TABLE reference.setupextract ADD CONSTRAINT unique_setupextract_order_no UNIQUE ("Order No");
ALTER TABLE reference.setupextract ADD CONSTRAINT unique_setupextract_case UNIQUE ("Case");
ALTER TABLE reference.sletters ADD CONSTRAINT unique_sletters_case UNIQUE ("Case");
ALTER TABLE reference.sup_activity ADD CONSTRAINT unique_sup_activity_sup_id UNIQUE ("SupID");
ALTER TABLE reference.sup_activity ADD CONSTRAINT unique_sup_activity_order_no UNIQUE ("Order No");
ALTER TABLE reference.sup_activity ADD CONSTRAINT unique_sup_activity_case UNIQUE ("Case");
ALTER TABLE reference.type3_chase ADD CONSTRAINT unique_type3_chase_case UNIQUE ("Case");
ALTER TABLE reference.visit ADD CONSTRAINT unique_visit_case UNIQUE ("Case");

ALTER TABLE reference.deputyship
    ADD CONSTRAINT fk_deputyship_account FOREIGN KEY ("Case") REFERENCES reference.account ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_account FOREIGN KEY ("Case") REFERENCES reference.account ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_account FOREIGN KEY ("Case") REFERENCES reference.account ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_account_chase FOREIGN KEY ("Case") REFERENCES reference.account_chase ("Case");


ALTER TABLE reference.riskcase
    ADD CONSTRAINT fk_riskcase_account_chase FOREIGN KEY ("Case") REFERENCES reference.account_chase ("Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_appl FOREIGN KEY ("CoP Case") REFERENCES reference.appl ("CoP Case");


ALTER TABLE reference.apprelation
    ADD CONSTRAINT fk_apprelation_appl FOREIGN KEY ("CoP Case") REFERENCES reference.appl ("CoP Case");


ALTER TABLE reference.court_diary
    ADD CONSTRAINT fk_court_diary_appl FOREIGN KEY ("CoP Case") REFERENCES reference.appl ("CoP Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_appl FOREIGN KEY ("CoP Case") REFERENCES reference.appl ("CoP Case");


ALTER TABLE reference.ordercop
    ADD CONSTRAINT fk_ordercop_appl FOREIGN KEY ("CoP Case") REFERENCES reference.appl ("CoP Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_appl FOREIGN KEY ("Case") REFERENCES reference.appl ("Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_applhistory FOREIGN KEY ("CoP Case") REFERENCES reference.applhistory ("CoP Case");


ALTER TABLE reference.apprelation
    ADD CONSTRAINT fk_apprelation_applhistory FOREIGN KEY ("CoP Case") REFERENCES reference.applhistory ("CoP Case");


ALTER TABLE reference.court_diary
    ADD CONSTRAINT fk_court_diary_applhistory FOREIGN KEY ("CoP Case") REFERENCES reference.applhistory ("CoP Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_applhistory FOREIGN KEY ("Case") REFERENCES reference.applhistory ("Case");


ALTER TABLE reference.applicantdup
    ADD CONSTRAINT fk_applicantdup_applicant FOREIGN KEY ("Partner No") REFERENCES reference.applicant ("Partner No");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_applicant FOREIGN KEY ("Partner No") REFERENCES reference.applicant ("Partner No");


ALTER TABLE reference.applicant
    ADD CONSTRAINT fk_applicant_applicantdup FOREIGN KEY ("Partner No") REFERENCES reference.applicantdup ("Partner No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_applink FOREIGN KEY ("Case") REFERENCES reference.applink ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_appl_location FOREIGN KEY ("Case") REFERENCES reference.appl_location ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_bonddebt FOREIGN KEY ("Order No") REFERENCES reference.bonddebt ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_bonddebt FOREIGN KEY ("Case") REFERENCES reference.bonddebt ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_bondnew FOREIGN KEY ("Order No") REFERENCES reference.bondnew ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_bondnew FOREIGN KEY ("Case") REFERENCES reference.bondnew ("Case");


ALTER TABLE reference.call_notes
    ADD CONSTRAINT fk_call_notes_calls FOREIGN KEY ("Call No") REFERENCES reference.calls ("Call No");


ALTER TABLE reference.enclosures
    ADD CONSTRAINT fk_enclosures_calls FOREIGN KEY ("Call No") REFERENCES reference.calls ("Call No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_calls FOREIGN KEY ("Case") REFERENCES reference.calls ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_cfoaccount FOREIGN KEY ("Case") REFERENCES reference.cfoaccount ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_cfoload FOREIGN KEY ("Case") REFERENCES reference.cfoload ("OPG Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_contact FOREIGN KEY ("Case") REFERENCES reference.contact ("Case");


ALTER TABLE reference.appl
    ADD CONSTRAINT fk_appl_court_diary FOREIGN KEY ("CoP Case") REFERENCES reference.court_diary ("CoP Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_court_diary FOREIGN KEY ("CoP Case") REFERENCES reference.court_diary ("CoP Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_cwsdata FOREIGN KEY ("Case") REFERENCES reference.cwsdata ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_cwshistory FOREIGN KEY ("Case") REFERENCES reference.cwshistory ("Case");


ALTER TABLE reference.depaddrhist
    ADD CONSTRAINT fk_depaddrhist_deplink FOREIGN KEY ("Dep Addr No") REFERENCES reference.deplink ("Dep Addr No");


ALTER TABLE reference.deputy_address
    ADD CONSTRAINT fk_deputy_address_deplink FOREIGN KEY ("Dep Addr No") REFERENCES reference.deplink ("Dep Addr No");


ALTER TABLE reference.deplink
    ADD CONSTRAINT fk_deplink_deputy FOREIGN KEY ("Deputy No") REFERENCES reference.deputy ("Deputy No");


ALTER TABLE reference.deputydup
    ADD CONSTRAINT fk_deputydup_deputy FOREIGN KEY ("Deputy No") REFERENCES reference.deputy ("Deputy No");


ALTER TABLE reference.deputyship
    ADD CONSTRAINT fk_deputyship_deputy FOREIGN KEY ("Deputy No") REFERENCES reference.deputy ("Deputy No");


ALTER TABLE reference.deputy_address
    ADD CONSTRAINT fk_deputy_address_deputyaddrdup FOREIGN KEY ("Dep Addr No") REFERENCES reference.deputyaddrdup ("Dep Addr No");


ALTER TABLE reference.deputy
    ADD CONSTRAINT fk_deputy_deputydup FOREIGN KEY ("Deputy No") REFERENCES reference.deputydup ("Deputy No");


ALTER TABLE reference.depaddrhist
    ADD CONSTRAINT fk_depaddrhist_deputyship FOREIGN KEY ("Dep Addr No") REFERENCES reference.deputyship ("Dep Addr No");


ALTER TABLE reference.dephist
    ADD CONSTRAINT fk_dephist_deputyship FOREIGN KEY ("Deputy No") REFERENCES reference.deputyship ("Deputy No");


ALTER TABLE reference.deputy
    ADD CONSTRAINT fk_deputy_deputyship FOREIGN KEY ("Deputy No") REFERENCES reference.deputyship ("Deputy No");


ALTER TABLE reference.deputy_address
    ADD CONSTRAINT fk_deputy_address_deputyship FOREIGN KEY ("Dep Addr No") REFERENCES reference.deputyship ("Dep Addr No");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_deputyship FOREIGN KEY ("Order No") REFERENCES reference.deputyship ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_deputyship FOREIGN KEY ("Case") REFERENCES reference.deputyship ("Case");


ALTER TABLE reference.deputyaddrdup
    ADD CONSTRAINT fk_deputyaddrdup_deputy_address FOREIGN KEY ("Dep Addr No") REFERENCES reference.deputy_address ("Dep Addr No");


ALTER TABLE reference.deputy
    ADD CONSTRAINT fk_deputy_feeaas FOREIGN KEY ("Deputy No") REFERENCES reference.feeaas ("Deputy No");


ALTER TABLE reference.deputy_address
    ADD CONSTRAINT fk_deputy_address_feeaas FOREIGN KEY ("Dep Addr No") REFERENCES reference.feeaas ("Dep Addr No");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_feeaas FOREIGN KEY ("Order No") REFERENCES reference.feeaas ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_feeaas FOREIGN KEY ("Case") REFERENCES reference.feeaas ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_feedebt FOREIGN KEY ("Case") REFERENCES reference.feedebt ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_file_location FOREIGN KEY ("Case") REFERENCES reference.file_location ("Case");


ALTER TABLE reference.cfoaccount
    ADD CONSTRAINT fk_cfoaccount_hsbclog FOREIGN KEY ("Case") REFERENCES reference.hsbclog ("Case");


ALTER TABLE reference.deputyship
    ADD CONSTRAINT fk_deputyship_hsbclog FOREIGN KEY ("Case") REFERENCES reference.hsbclog ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_hsbclog FOREIGN KEY ("Case") REFERENCES reference.hsbclog ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_hsbclog FOREIGN KEY ("Case") REFERENCES reference.hsbclog ("Case");


ALTER TABLE reference.setupextract
    ADD CONSTRAINT fk_setupextract_hsbclog FOREIGN KEY ("Case") REFERENCES reference.hsbclog ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_kpidata FOREIGN KEY ("Case") REFERENCES reference.kpidata ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_merisdebt FOREIGN KEY ("Case") REFERENCES reference.merisdebt ("Meris Case");


ALTER TABLE reference.applicant
    ADD CONSTRAINT fk_applicant_newfee FOREIGN KEY ("Partner No") REFERENCES reference.newfee ("Partner No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_newfee FOREIGN KEY ("Case") REFERENCES reference.newfee ("Case");


ALTER TABLE reference.account
    ADD CONSTRAINT fk_account_order FOREIGN KEY ("Case") REFERENCES reference.order ("Case");


ALTER TABLE reference.appl
    ADD CONSTRAINT fk_appl_order FOREIGN KEY ("CoP Case") REFERENCES reference.order ("CoP Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_order FOREIGN KEY ("CoP Case") REFERENCES reference.order ("CoP Case");


ALTER TABLE reference.deputyship
    ADD CONSTRAINT fk_deputyship_order FOREIGN KEY ("Order No") REFERENCES reference.order ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_order FOREIGN KEY ("Case") REFERENCES reference.order ("Case");


ALTER TABLE reference.appl
    ADD CONSTRAINT fk_appl_ordercop FOREIGN KEY ("CoP Case") REFERENCES reference.ordercop ("CoP Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_ordercop FOREIGN KEY ("CoP Case") REFERENCES reference.ordercop ("CoP Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_ordercop FOREIGN KEY ("Case") REFERENCES reference.ordercop ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_orderhistory FOREIGN KEY ("Case") REFERENCES reference.orderhistory ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_order_chase FOREIGN KEY ("Case") REFERENCES reference.order_chase ("Case");


ALTER TABLE reference.riskcase
    ADD CONSTRAINT fk_riskcase_order_chase FOREIGN KEY ("Case") REFERENCES reference.order_chase ("Case");


ALTER TABLE reference.prexpertise
    ADD CONSTRAINT fk_prexpertise_panrec FOREIGN KEY ("Panel No") REFERENCES reference.panrec ("Panel No");


ALTER TABLE reference.prgeoarea
    ADD CONSTRAINT fk_prgeoarea_panrec FOREIGN KEY ("Panel No") REFERENCES reference.panrec ("Panel No");


ALTER TABLE reference.prlang
    ADD CONSTRAINT fk_prlang_panrec FOREIGN KEY ("Panel No") REFERENCES reference.panrec ("Panel No");


ALTER TABLE reference.prneeds
    ADD CONSTRAINT fk_prneeds_panrec FOREIGN KEY ("Panel No") REFERENCES reference.panrec ("Panel No");


ALTER TABLE reference.prskills
    ADD CONSTRAINT fk_prskills_panrec FOREIGN KEY ("Panel No") REFERENCES reference.panrec ("Panel No");


ALTER TABLE reference.account
    ADD CONSTRAINT fk_account_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.appl
    ADD CONSTRAINT fk_appl_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.applink
    ADD CONSTRAINT fk_applink_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.appl_location
    ADD CONSTRAINT fk_appl_location_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.apprelation
    ADD CONSTRAINT fk_apprelation_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.bolog
    ADD CONSTRAINT fk_bolog_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.casepremca
    ADD CONSTRAINT fk_casepremca_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.cfoaccount
    ADD CONSTRAINT fk_cfoaccount_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.contact
    ADD CONSTRAINT fk_contact_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.cwshistory
    ADD CONSTRAINT fk_cwshistory_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.deputyship
    ADD CONSTRAINT fk_deputyship_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.feedebt
    ADD CONSTRAINT fk_feedebt_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.file_location
    ADD CONSTRAINT fk_file_location_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.hsbclog
    ADD CONSTRAINT fk_hsbclog_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.newfee
    ADD CONSTRAINT fk_newfee_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.ordercop
    ADD CONSTRAINT fk_ordercop_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.patdup
    ADD CONSTRAINT fk_patdup_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.remshist
    ADD CONSTRAINT fk_remshist_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.repvis
    ADD CONSTRAINT fk_repvis_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.setupextract
    ADD CONSTRAINT fk_setupextract_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.visit
    ADD CONSTRAINT fk_visit_pat FOREIGN KEY ("Case") REFERENCES reference.pat ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_patdup FOREIGN KEY ("Case") REFERENCES reference.patdup ("Case");


ALTER TABLE reference.patexcept
    ADD CONSTRAINT fk_patexcept_patstats FOREIGN KEY ("Case") REFERENCES reference.patstats ("Case");


ALTER TABLE reference.panrec
    ADD CONSTRAINT fk_panrec_pletters FOREIGN KEY ("Panel No") REFERENCES reference.pletters ("Panel No");


ALTER TABLE reference.calls
    ADD CONSTRAINT fk_calls_remarks FOREIGN KEY ("Call No") REFERENCES reference.remarks ("Call No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_remarks FOREIGN KEY ("Case") REFERENCES reference.remarks ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_remshist FOREIGN KEY ("Case") REFERENCES reference.remshist ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_repvis FOREIGN KEY ("Case") REFERENCES reference.repvis ("Case");


ALTER TABLE reference.risk_assessment
    ADD CONSTRAINT fk_risk_assessment_risks_assessed FOREIGN KEY ("Asmt Id") REFERENCES reference.risks_assessed ("Asmt Id");


ALTER TABLE reference.risk_del
    ADD CONSTRAINT fk_risk_del_risks_assessed FOREIGN KEY ("Asmt ID") REFERENCES reference.risks_assessed ("Asmt Id");


ALTER TABLE reference.risk_assessment
    ADD CONSTRAINT fk_risk_assessment_risks_del FOREIGN KEY ("Asmt Id") REFERENCES reference.risks_del ("Asmt Id");


ALTER TABLE reference.risk_del
    ADD CONSTRAINT fk_risk_del_risks_del FOREIGN KEY ("Asmt ID") REFERENCES reference.risks_del ("Asmt Id");


ALTER TABLE reference.assessment_rev
    ADD CONSTRAINT fk_assessment_rev_risk_assessment FOREIGN KEY ("Asmt ID") REFERENCES reference.risk_assessment ("Asmt Id");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_risk_assessment FOREIGN KEY ("Order No") REFERENCES reference.risk_assessment ("Order No");


ALTER TABLE reference.risks_assessed
    ADD CONSTRAINT fk_risks_assessed_risk_assessment FOREIGN KEY ("Asmt Id") REFERENCES reference.risk_assessment ("Asmt Id");


ALTER TABLE reference.risks_del
    ADD CONSTRAINT fk_risks_del_risk_assessment FOREIGN KEY ("Asmt Id") REFERENCES reference.risk_assessment ("Asmt Id");


ALTER TABLE reference.assessment_rev
    ADD CONSTRAINT fk_assessment_rev_risk_del FOREIGN KEY ("Asmt ID") REFERENCES reference.risk_del ("Asmt ID");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_risk_del FOREIGN KEY ("Order No") REFERENCES reference.risk_del ("Order No");


ALTER TABLE reference.risks_assessed
    ADD CONSTRAINT fk_risks_assessed_risk_del FOREIGN KEY ("Asmt Id") REFERENCES reference.risk_del ("Asmt ID");


ALTER TABLE reference.risks_del
    ADD CONSTRAINT fk_risks_del_risk_del FOREIGN KEY ("Asmt Id") REFERENCES reference.risk_del ("Asmt ID");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_setuperr FOREIGN KEY ("Order No") REFERENCES reference.setuperr ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_setuperr FOREIGN KEY ("Case") REFERENCES reference.setuperr ("Case");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_setupextract FOREIGN KEY ("Order No") REFERENCES reference.setupextract ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_setupextract FOREIGN KEY ("Case") REFERENCES reference.setupextract ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_sletters FOREIGN KEY ("Case") REFERENCES reference.sletters ("Case");


ALTER TABLE reference.activity_tracking
    ADD CONSTRAINT fk_activity_tracking_sup_activity FOREIGN KEY ("Sup ID") REFERENCES reference.sup_activity ("SupID");


ALTER TABLE reference.order
    ADD CONSTRAINT fk_order_sup_activity FOREIGN KEY ("Order No") REFERENCES reference.sup_activity ("Order No");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_sup_activity FOREIGN KEY ("Case") REFERENCES reference.sup_activity ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_type3_chase FOREIGN KEY ("Case") REFERENCES reference.type3_chase ("Case");


ALTER TABLE reference.riskcase
    ADD CONSTRAINT fk_riskcase_type3_chase FOREIGN KEY ("Case") REFERENCES reference.type3_chase ("Case");


ALTER TABLE reference.pat
    ADD CONSTRAINT fk_pat_visit FOREIGN KEY ("Case") REFERENCES reference.visit ("Case");

