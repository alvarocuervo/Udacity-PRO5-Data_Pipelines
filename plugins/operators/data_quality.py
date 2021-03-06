from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id = '',
                 tables_to_check = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.tables_to_check = tables_to_check

    def execute(self, context):
        """ Execute the operator in order to check the quality of the DAG's result

        Arguments:
            context
        Returns:
            None
        """

        #self.log.info('DataQualityOperator not implemented yet')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        for table in self.tables_to_check:
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            if len(records) < 1 or len(records[0]) < 1:
                self.log.error(f"Table {table} returned no results")
                raise ValueError(f"Data quality check failed. Table {table} returned no results")
            num_records = records[0][0]
            if num_records == 0:
                self.log.error(f"No records present in destination Table {table}")
                raise ValueError(f"No records present in destination Table {table}")
            self.log.info(f"Data quality on Table {table} check passed with {num_records} records")