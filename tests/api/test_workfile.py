import os
import time

from alpine import APIClient
from alpine.exception import *
from alpine.workfile import *
<<<<<<< HEAD
from alpine.datasource import DataSource

=======
>>>>>>> 8419756... Update properties for moudle attributes

from .alpineunittest import AlpineTestCase


class TestWorkfile(AlpineTestCase):

    def setUp(self):
        super(TestWorkfile, self).setUp()
        global workspace_name
        global workspace_id
        global workfile_name
        global workfile_id
        global db_datasource_id
        global database_id
        global hadoop_datasource_id
        # To pass the tests, we need a Hadoop Data Source with Name "API_Test_Hadoop"
        # and GPDB datas ource with name "API_Test_GPDB" created
        gpdb_datasource_name = "API_Test_GPDB"
        hadoop_datasource_name = "API_Test_Hadoop"
        database_name = "miner_demo"

        # Creating a Workspace for Job tests
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        db_datasource_id = alpine_session.datasource.get_id(gpdb_datasource_name, "Database")
        hadoop_datasource_id = alpine_session.datasource.get_id(hadoop_datasource_name, "Hadoop")

        try:
            workspace_id = alpine_session.workspace.get_id("Workspace for Workfile Tests")
            alpine_session.workspace.delete(workspace_id)
        except WorkspaceNotFoundException:
            pass
        workspace_info = alpine_session.workspace.create("Workspace for Workfile Tests")
        workspace_id = workspace_info['id']
        workspace_name = workspace_info['name']

        # Upload a DB flow
        base_dir = os.getcwd()
        afm_path = "{0}/../data/afm/db_row_fil_with_variable.afm".format(base_dir)
        # afm_path = "db_bat_row_fil.afm"
        try:
            workfile_id = alpine_session.workfile.get_id("db_row_fil_with_variable", workspace_id)
            alpine_session.workfile.delete(workfile_id)
        except WorkfileNotFoundException:
            pass
        database_list = alpine_session.datasource.get_database_list(db_datasource_id)
        for database in database_list:
            if database['name'] == "miner_demo":
                database_id = database['id']
        datasource_info = [{"data_source_type": DataSource.DSType.GreenplumDatabase,
                            "data_source_id": db_datasource_id,
                            "database_id": database_id
                            }]
        workfile_info = alpine_session.workfile.upload(workspace_id, afm_path, datasource_info)
        workfile_id = workfile_info['id']
        workfile_name = workfile_info['file_name']

        alpine_session.logout

    def tearDown(self):
        # Drop the datasources created in setup
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        #alpine_session.workspace.delete_workspace_if_exists("Workspace for Workfile Tests")

    def test_get_workfiles_list(self):
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_list = alpine_session.workfile.get_list(workspace_id)
        self.assertIsNotNone(workfile_list)
        self.assertEqual(workfile_list.__len__(), 1)

    def test_get_workfile_info(self):
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_id = alpine_session.workfile.get_id("db_row_fil_with_variable", workspace_id)
        workfile_info = alpine_session.workfile.get(workfile_id)
        self.assertIsNotNone(workfile_info)

    def test_get_workfile_id(self):
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        get_id = alpine_session.workfile.get_id("db_row_fil_with_variable", workspace_id)
        self.assertIsNotNone(get_id)
        self.assertEqual(workfile_id, get_id)

    def test_run_workflow(self):
        variables = [{"name": "@min_credit_line", "value": "7"}]
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_id = alpine_session.workfile.get_id(workfile_name, workspace_id)
        process_id = alpine_session.workfile.process.run(workfile_id, variables)
        alpine_session.workfile.process.wait_until_finished(process_id)

    def test_query_workflow_status(self):
        valid_workfile_status = ["WORKING", "FINISHED"]
        variables = [{"name": "@min_credit_line", "value": "7"}]
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_id = alpine_session.workfile.get_id(workfile_name, workspace_id)
        process_id = alpine_session.workfile.process.run(workfile_id, variables)
        for i in range(0, 100):
            workfile_status = alpine_session.workfile.process.query_status(process_id)
            if workfile_status in valid_workfile_status:
                if workfile_status == "FINISHED":
                    break
                else:
                    time.sleep(1)
            else:
                self.fail("Invalid workfile status {0}".format(workfile_status))

    def test_download_workflow_results(self):
        variables = [{"name": "@min_credit_line", "value": "7"}]
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_id = alpine_session.workfile.get_id(workfile_name, workspace_id)

        process_id = alpine_session.workfile.process.run(workfile_id, variables)
        workfile_status = alpine_session.workfile.process.query_status(process_id)
        while workfile_status != "FINISHED":
            time.sleep(1)
            workfile_status = alpine_session.workfile.process.query_status(process_id)
        response = alpine_session.workfile.process.download_results(workfile_id, process_id)

    def test_stop_workflow(self):
        variables = [{"name": "@min_credit_line", "value": "7"}]
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        workfile_id = alpine_session.workfile.get_id(workfile_name, workspace_id)
        process_id = alpine_session.workfile.process.run(workfile_id, variables)
        finish_state = alpine_session.workfile.process.stop(process_id)
        self.assertEqual(finish_state, "STOPPED")

    def test_upload_hdfs_afm(self):
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        base_dir = os.getcwd()
        afm_path = "{0}/../data/afm/demo_hadoop_row_filter_regression.afm".format(base_dir)
        #afm_path = "demo_hadoop_row_filter_regression.afm"
        try:
            workfile_id = alpine_session.workfile.get_id("demo_hadoop_row_filter_regression", workspace_id)
            alpine_session.workfile.delete(workfile_id)
        except WorkfileNotFoundException:
            pass
        datasource_info = [{"data_source_type": alpine_session.datasource.dsType.HadoopCluster,
                            "data_source_id": hadoop_datasource_id
                            }]
        workfile_info = alpine_session.workfile.upload(workspace_id, afm_path, datasource_info)
        self.assertEqual(workfile_info['file_name'], "demo_hadoop_row_filter_regression")

    def test_upload_db_afm(self):
        alpine_session = APIClient(self.host, self.port)
        alpine_session.login(self.username, self.password)
        base_dir = os.getcwd()
        afm_path = "{0}/../data/afm/db_bat_row_fil.afm".format(base_dir)
        #afm_path = "db_bat_row_fil.afm"
        try:
            workfile_id = alpine_session.workfile.get_id("db_bat_row_fil", workspace_id)
            alpine_session.workfile.delete(workfile_id)
        except WorkfileNotFoundException:
            pass

        #workfile_info = alpine_session.workfile.upload_db_afm(workspace_id, data_source_id, 1, "GpdbDataSource", "gpdb_database", afm_path)
        # datasource_info = [{"data_source_type": "HdfsDataSource", "data_source_id": "1", "database_type": "hdfs_data_source",
        #                     "database_id":""},
        #                    {"data_source_type": "JdbcDataSource", "data_source_id": "421", "database_type": "jdbc_data_source",
        #                     "database_id": ""},
        #                    {"data_source_type": "GpdbDataSource", "data_source_id": "1", "database_type": "gpdb_database",
        #                     "database_id": "42"}]
        datasource_info = [{"data_source_type": alpine_session.datasource.dsType.GreenplumDatabase,
                            "data_source_id": db_datasource_id,
                            "database_id": database_id}]
        workfile_info = alpine_session.workfile.upload(workspace_id, afm_path, datasource_info)
        self.assertEqual(workfile_info['file_name'], "db_bat_row_fil")
