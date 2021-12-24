_aliased_column_datatypes = {
    'c_ord_stat': {'data_type': 'string'},
    'c_ord_type': {'data_type': 'string'}
}

_mappings = [
    {
        'default_cols': {
            'orderstatus': None
        }
    },
    {
        'criteria': [
            'c_ord_stat == "Closed"',
        ],
        'output_cols': {
            'orderstatus': 'CLOSED'
        }
    },
    {
        'criteria': [
            'c_ord_stat == "Active"',
            'c_ord_type.isin(["26", "43", "45"])'
        ],
        'output_cols': {
            'orderstatus': 'OPEN'
        }
    },
    {
        'criteria': [
            'c_ord_stat == "Active"',
            '~c_ord_type.isin(["26", "43", "45"])'
        ],
        'output_cols': {
            'orderstatus': 'ACTIVE'
        }
    }
]


TABLE_TRANSFORM_CASES = {
    'datatypes': _aliased_column_datatypes,
    'mappings': _mappings,
    'local_vars': {}
}
