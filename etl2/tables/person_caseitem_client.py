

def final(persons_df, cases_df):


    persons_df = persons_df[['id', 'caserecnumber']]
    cases_df = cases_df[['id', 'caserecnumber']]

    person_caseitem_df = cases_df.merge(persons_df, how='left', left_on='caserecnumber',
                                        right_on='caserecnumber', suffixes=['_case',
                                                                            '_person'])

    person_caseitem_df = person_caseitem_df.drop(columns=['caserecnumber'])
    person_caseitem_df = person_caseitem_df.rename(columns={'id_case':'case_id',
                                                            'id_person': 'person_id'})

    return person_caseitem_df
