### Urgent post migration fixes

#### Naming conventions

Due to activities that need immediate data amendments, we need a method to safely get fixes out to production quickly
whilst meeting the needs of the business.

This is subject to change but the current method of doing this is as follows:

Create a new folder named the same as the schema for the fix. We agreed to use a separate schema for each fix so as
to isolate each fix from the rest (in cases where it includes multiple table updates this will make tracking simpler).

Naming convention:

- ``pmf_<entity name>_<date of fix>_<jira reference>``

Within the fix each table that needs to be updated should have:

- an updates table that shows the problem and has original and expected values
- An audit table where the actual full rows from the table are copied out
(in case multiple changes affect the table so we have a point in time)

#### Approval

Before releasing your change, you should:

- Create a PR and get sign off from another dev
- Fully test all statements on non production environment
- Run validation before the change and afterwards
- Get business to spot check the results and sign off
- Do the Begin statement up to rollback so that you can rollback in case of wrong counts
- Remember to ``commit;``
- Do the fixes at end of the day and take a snapshot beforehand
- Do the release in a pair so you have a second pair of eyes

