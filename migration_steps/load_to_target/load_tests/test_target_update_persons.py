from migration_steps.load_to_target.app.entities.client import target_update, target_add


def test_target_update(
    caplog,
    test_config,
    mock_persons_df,
    mock_execute_update_with_logs,
    mock_get_mapping_dict,
):

    config = test_config

    target_update(config=config, conn_migration="fake_db_1", conn_target="fake_db_2")

    expected_cols = [
        "id",
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
        "salutation",
        "casesmanagedashybrid",
    ]

    log_message_cols = f"cols: {expected_cols}"

    assert log_message_cols in caplog.text


def test_target_add(
    caplog,
    test_config,
    mock_persons_df,
    mock_execute_insert_with_logs,
    mock_result_from_sql_file,
    mock_get_mapping_dict,
):

    config = test_config

    target_add(config=config, conn_migration="fake_db_1", conn_target="fake_db_2")

    expected_cols = [
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
        "uid",
    ]
    # expected_tuples = [
    #     (0, "name1", "surname1", "CASRECMIGRATION", 2),
    #     (1, "name2", "surname2", "CASRECMIGRATION", 3),
    #     (2, "name3", "surname3", "CASRECMIGRATION", 4),
    # ]

    log_message_cols = f"cols: {','.join(expected_cols)}"
    # log_message_tuples = f"tuples: {expected_tuples}"

    assert log_message_cols in caplog.text
    # assert log_message_tuples in caplog.text
