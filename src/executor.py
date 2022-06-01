from pypika import MySQLQuery, Table


def _del_sql_query_builder(query):
    records = Table('AcronymRecords')
    q = MySQLQuery.from_(records).delete()

    if query['ACRONYM'] != 'default':
        q = q.where(records.acronym == query['ACRONYM'])
    if query['FULL_NAME'] != 'default':
        q = q.where(records.fullname == query['FULL_NAME'])
    if query['SCOPE'] != 'default':
        q = q.where(records.scope == query['SCOPE'])

    q = str(q) + ';'
    # print(q)
    return q


def _show_sql_query_builder(query, params_requested):
    records = Table('AcronymRecords')
    q = MySQLQuery.from_('AcronymRecords').select(
        records.acronym, records.fullname
    )

    if params_requested['ACRONYM']:
        q = q.where(records.acronym == query['ACRONYM'])
    if params_requested['FULL_NAME']:
        q = q.where(records.fullname == query['FULL_NAME'])
    if params_requested['SCOPE']:
        q = q.where(records.scope.like(query['SCOPE']))
        q = q.select(records.scope)
    if params_requested['TIME']:
        q = q.select(records.time)

    q = str(q) + ';'
    # print(q)
    return q


def _add_sql_query_builder(query):
    q = MySQLQuery.into('AcronymRecords').insert(
        query['ACRONYM'],
        query['FULL_NAME'],
        query['SCOPE'],
        query['TIME']
        )

    q = str(q) + ';'
    return q


class Executor:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def execute_query(self, query, params_requested):
        if query['COMMAND'] == 'add':
            self.db_handler.execute_query(_add_sql_query_builder(query))

        if query['COMMAND'] == 'show':
            labels, data = self.db_handler.execute_query(_show_sql_query_builder(query, params_requested), fetch=True)

            for record in data:
                d = {labels[i]: record[i] for i in range(len(labels))}

                s = f'{d["acronym"]} --> {d["fullname"]} '

                if params_requested['SCOPE']:
                    s += f'in the scope <{d["scope"]}> '
                if params_requested['TIME']:
                    s += f'loaded on {d["time"]} '

                print(s)

        if query['COMMAND'] == 'del':
            self.db_handler.execute_query(_del_sql_query_builder(query))
