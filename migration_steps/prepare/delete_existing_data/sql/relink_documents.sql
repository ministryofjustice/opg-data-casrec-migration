BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS temp_documents_on_cases(
    documentId int,
    caseType VARCHAR(255),
    clientId int,
    dateMoved timestamp
);

INSERT INTO temp_documents_on_cases ( documentId, caseType, clientId, dateMoved)
select d.id, c.casetype, p.id, now()
from documents d
         inner join caseitem_document cd on d.id = cd.document_id
         inner join cases c on c.id = cd.caseitem_id
         inner join persons p on p.id = c.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

INSERT INTO person_document ( person_id, document_id )
select c.client_id, d.id
from documents d
         inner join caseitem_document cd on d.id = cd.document_id
         inner join cases c on c.id = cd.caseitem_id
         inner join persons p on p.id = c.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

DELETE FROM caseitem_document where document_id in (
select d.id
from documents d
         inner join caseitem_document cd on d.id = cd.document_id
         inner join cases c on c.id = cd.caseitem_id
         inner join persons p on p.id = c.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null));
COMMIT TRANSACTION;
