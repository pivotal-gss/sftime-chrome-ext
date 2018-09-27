from simple_salesforce import Salesforce
import os


class GetMetrics:

    def __init__(self):
        self.caseID = '180913'
        self.instance = os.environ['SALESFORCE_URI']
        self.username = os.environ['SALESFORCE_USER']
        self.password = os.environ['SALESFORCE_PASSWORD']
        self.token = os.environ['SALESFORCE_SECURITY_TOKEN']
        self.collector = []
        self.sf = Salesforce(instance=self.instance, username=self.username, password=self.password, security_token=self.token)

    def get_case_details(self):
        """
        Get the case number ID, since this is a test we except only one row
        """
        caseIDsf = ""
        query = "SELECT CaseID18__c,CaseNumber FROM Case WHERE CaseNumber = \'" + self.caseID + "\'"
        case_details = self.sf.query(query)['records']
        for x in case_details:
            caseIDsf = x['CaseID18__c']
        return caseIDsf

    def get_case_feeds(self, case_id, create_date):
        """
        Get the case body and the type, only one row will be returned here
        """
        query = "SELECT Body,CreatedDate,Type " \
                "FROM CaseFeed WHERE CreatedDate >= " + create_date + " AND " \
                "ParentId = \'" + case_id + "\' ORDER BY CreatedDate ASC NULLS LAST LIMIT 1"
        case_feeds = self.sf.query(query)['records']
        if len(case_feeds) == 0:
            return "", "", ""
        else:
            for x in case_feeds:
                return x['Body'], x['Type'], x['CreatedDate']

    def get_user_name(self, id):
        """
        Get the username associated with the time
        """
        query = "SELECT FirstName,LastName FROM User WHERE Id = \'" + id + "\'"
        user_name = self.sf.query(query)['records']
        for x in user_name:
            return x['FirstName'] + ' ' + x['LastName']

    def get_timer_information(self):
        """
        Get all the time on the feeds on the tickets
        """
        case_id = self.get_case_details()
        query = "SELECT CreatedById,CreatedDate,PCCT__Case__c,PCCT__Duration__c " \
                "FROM PCCT__Session_Time__C " \
                "WHERE PCCT__Case__c = \'" + case_id + "\'"
        time_details = self.sf.query(query)['records']
        for x in time_details:
            temp_collector = {}
            date = x['CreatedDate']
            duration = x['PCCT__Duration__c']
            user = x['CreatedById']
            casenumber = x['PCCT__Case__c']
            username = self.get_user_name(user)
            casebody, casetype, casedate = self.get_case_feeds(casenumber, date)
            temp_collector['name'] = username
            temp_collector['date'] = casedate
            temp_collector['type'] = casetype
            temp_collector['body'] = casebody
            temp_collector['time'] = duration
            self.collector.append(temp_collector)

        self.table_format()

    def table_format(self):
        """
        Change the Json to table
        """
        heading = ['Name', 'Date', 'Message Type', 'Body', 'Duration']
        fmt1 = '|{0:-<30}|{0:->30}|{0:->30}|{0:->60}|{0:->20}|'
        fmt2 = '|{0:<30}|{1:<30}|{2:<30}|{3:<60}|{4:<20}|'
        print(fmt1.format(''))
        print(fmt2.format(heading[0], heading[1], heading[2], heading[3], heading[4]))
        print(fmt1.format(''))
        for collection in self.collector:
            if collection['body'] == None:
                collection['body'] = ""
            collections = [
                collection['name'],
                collection['date'],
                collection['type'],
                collection['body'],
                collection['time'],
            ]
            print(fmt2.format(collections[0], collections[1], collections[2], collections[3], collections[4]))

        print(fmt1.format(''))


# Run the program
if __name__ == "__main__":
    GetMetrics().get_timer_information()

