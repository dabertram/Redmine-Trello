
import redmine
from redmine.resultsets import ResourceSet
import trello
import TrelloManager


# http://python-redmine.readthedocs.org/
###################### redmine config ######################

projectname_config = ""
redmine_url = ""
api_key = ""

###################### redmine functions ######################


class RedmineManager:

    redmine = None

    open_issues = {}
    assigned_issues = {}

    def __init__(self):
        self.project_name = None
        self.configuration = None

    def connect_redmine(self, configuration):
        self.project_name = configuration["redmine_projectname"]
        self.configuration = configuration
        self.redmine = redmine.Redmine(configuration["redmine_url"],
                                       key=configuration["redmine_api_key"],
                                       raise_attr_exception=False)

    def __del__(self):
        self.redmine = None

    def create_issue_from_unlinked_card(self, card):
        assert isinstance(card, trello.Card)
        assert len(card.name.split("{")) == 1 and len(card.name.split("}")) == 1

        # fetch card content
        card.fetch()
        ### cards as issue: issue name = card name + {card-ID}
        issue_name = card.name + " {" + str(card.short_id) + "}"
        print issue_name
        print "ISSUE CREATION NOT YET IMPLEMENTED"
        exit(1)
# redmine create issue

#check if there is a project for this card (boardname begins with Projectname)

        ### checklists as sub-issues: sub-issue name = card name + [checklist name] + {checklist-ID}
        # generate sub-issues
        checklists = card.checklists
        for checklist in checklists:
            assert isinstance(checklist, trello.Checklist)
            assert len(checklist.items) > 0
            sub_issue_name = checklist.name + " [" + str(checklist.id) + "]{" + str(card.short_id) + "}"
            print sub_issue_name
# redmine create sub issues

            ### checklist-items as sub-sub-issues: sub-sub-issue name = card name + [checklist name] + [checklist item name] + {checklistitem-ID}
            for item in checklist.items:
                assert isinstance(item, dict)
                assert item.get("name") is not None and item.get("id") is not None
                print item
                sub_sub_issue_name = item["name"] + " (" + item["id"] + ")[" + str(checklist.id) + "]{" + str(card.short_id) + "}"
                print sub_sub_issue_name
# redmine create sub sub issues

        # add issue ID to card name


    def is_checklistItem_in_issues(self, checklistItem):
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])

        #assert isinstance(checklist, trello.Checklist)

        #card = checklist.trello_card
        # print card, card.__class__
        # assert isinstance(card, trello.Card)
        # card.fetch()

        issueID = "(" + checklistItem["name"] + ")"  # + "{" + card + "}"
        #issueName = checklistItem.name

        # exists = False
        # for issue in issues:
        #     checklistID = issue.custom_fields["trello_checklistID"]
        #     subject = issue.subject
        #     print subject, subject.__class__
        #
        #     if checklistID == checklist.id:
        #         print "issue for this checklist already exists!"
        #         exists = True
        #         break

        exists = False
        for issue in issues:
            description = issue.description
            subject = issue.subject
            print subject, subject.__class__

            if description.endswith(issueID):
                print "issue for this checklistItem already exists!"
                exists = True
                break

        return exists

    def is_checklist_in_issues(self, checklist):
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])

        assert isinstance(checklist, trello.Checklist)

        card = checklist.trello_card
        # print card, card.__class__
        # assert isinstance(card, trello.Card)
        # card.fetch()

        issueID = "[" + checklist.id + "]"  # + "{" + card + "}"
        issueName = checklist.name

        # exists = False
        # for issue in issues:
        #     checklistID = issue.custom_fields["trello_checklistID"]
        #     subject = issue.subject
        #     print subject, subject.__class__
        #
        #     if checklistID == checklist.id:
        #         print "issue for this checklist already exists!"
        #         exists = True
        #         break

        exists = False
        for issue in issues:
            description = issue.description
            subject = issue.subject
            print subject, subject.__class__

            if description.endswith(issueID):
                print "issue for this checklist already exists!"
                exists = True
                break

        return exists

    def is_card_in_issues(self, card):
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])

        issueID = "{" + card.id + "}"
        issueName = card.name


        exists = False
        for issue in issues:
            description = issue.description
            subject = issue.subject

            print subject, subject.__class__

            if isinstance(description, unicode):
                if description.endswith(issueID):
                    print "issue for this card already exists!"
                    exists = True
                    break

        print "exists:", exists

        return exists


    def create_all_issues_from_card(self, card):
        self.create_issue_from_card(card)
        assert isinstance(card, trello.Card)
        # card.fetch()
        print dir(card)
        for checklist in card.checklists:
            self.create_issue_from_checklist(checklist, card)
            self.create_issues_from_checklistItems(checklist, card)

    def create_issue_from_card(self, card):
        assert isinstance(card, trello.Card)

        if not self.is_card_in_issues(card):

            issueID = "{" + card.id + "}"
            issueName = card.name

            description = issueID
            print "new issue name"
            print issueName, issueID

            # check existing issues for card id
            ## if not found -> create issue
            issue = self.redmine.issue.new()
            issue.subject = issueName
            issue.project_id = self.project_name
            issue.description = description
            # issue.custom_fields = [{"trello_cardID": card.id}]
            issue.save()

    def create_issue_from_checklist(self, checklist, card):
        assert isinstance(checklist, trello.Checklist)

        if not self.is_checklist_in_issues(checklist):

            issueID = "[" + checklist.id + "]"      # + "{" + card + "}"
            issueName = checklist.name + " [" + card.name + "]"

            description = issueID
            print "new issue name"
            print issueName, issueID

            # check existing issues for card id
            ## if not found -> create issue
            issue = self.redmine.issue.new()
            issue.subject = issueName
            issue.project_id = self.project_name
            issue.description = description
            parent_issue = self.get_issue_from_cardID(card.id)
            issue.parent_issue_id = parent_issue.id
            # issue.custom_fields = [{"trello_checklistID": checklist.id}]

            issue.save()

            # relation = self.redmine.issue_relation.new()
            #
            # relation.issue_id = issue.id
            # relation.issue_to_id = parent_issue.id
            # relation.relation_type = 'follows'
            # relation.delay = 0
            # relation.save()

            print "parent_issue.children:", parent_issue.children

    def create_issues_from_checklistItems(self,  checklist, card):
        assert isinstance(checklist, trello.Checklist)

        for item in checklist.items:

            if not self.is_checklistItem_in_issues(item):

                issueID = "(" + item["name"] + ")"      # + "{" + card + "}"
                issueName = item["name"] + " (" + checklist.name + ")"

                description = issueID
                print "new issue name"
                print issueName, issueID

                # check existing issues for card id
                ## if not found -> create issue
                issue = self.redmine.issue.new()
                issue.subject = issueName
                issue.project_id = self.project_name
                issue.description = description
                parent_issue = self.get_issue_from_checklistID(checklist.id)
                issue.parent_issue_id = parent_issue.id
                # issue.custom_fields = [{"trello_checklistID": checklist.id}]

                issue.save()

                # relation = self.redmine.issue_relation.new()
                #
                # relation.issue_id = issue.id
                # relation.issue_to_id = parent_issue.id
                # relation.relation_type = 'follows'
                # relation.delay = 0
                # relation.save()

                print "parent_issue.children:", parent_issue.children


    def get_issue_from_cardID(self, cardID):
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])

        issueID = None
        for issue in issues:
            assert isinstance(issue.description, unicode)
            find_issueID = "{" + cardID + "}"
            if issue.description.endswith(find_issueID):
                print "found issue for parent issue:", issue, dir(issue)
                return issue
                # issueID = issue.ID
                # print issueID

    def get_issue_from_checklistID(self, cardID):
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])

        issueID = None
        for issue in issues:
            assert isinstance(issue.description, unicode)
            find_issueID = "[" + cardID + "]"
            if issue.description.endswith(find_issueID):
                print "found issue for parent issue:", issue, dir(issue)
                return issue
                # issueID = issue.ID
                # print issueID

################### OLD ##########################
# first try out functions ##### just use as templates
    def print_resource_set(self, resourceset):
        for entry in resourceset:
            if isinstance(entry, ResourceSet):
                print "2 extracting value.."
                self.print_resource_set(entry)
            else:
                print " ++ ", entry

    def sort_issues(self, issues):
        print "sorting issues into open and assigned:"

        self.open_issues = {}
        self.assigned_issues = {}

        for issue in issues:
            if issue.assigned_to_id:
                self.assigned_issues[issue.subject] = issue
            else:
                self.open_issues[issue.subject] = issue
        print "finished sorting issues."


    def print_issue(self, issue):
        print " issue: ", issue.subject
        for attribute in dir(issue):
            if attribute == "time_entries":
                self.print_time_entries(issue[attribute])
            elif attribute == "children":
                print " skipped: ", attribute, "..because it was crashing.. why?"
            elif isinstance(issue[attribute], ResourceSet):
                print "1 extracting value..", attribute
                self.print_resource_set(issue[attribute])
            else:
                print "   - ", attribute, ":", issue[attribute]

    def print_time_entries(self, time_entries):
        print "    time_entries:"
        for time_entry in time_entries:
            print "    -- entry: "
            for attribute in dir(time_entry):
                try:
                    print "    --- ", attribute, ":", time_entry[attribute]
                except Exception as e:
                    print
                    print "!!", e
                    print

    def redmine_first_steps(self):

        print ""
        print "##################### Hello from RedmineManager ######################"
        print


        project = self.redmine.project.get(self.configuration["redmine_projectname"])
        print "loaded project:", project.name, "from:", self.configuration["redmine_url"], "object:", project

        print "loading project issues.."
        issues = self.redmine.issue.filter(project_id=self.configuration["redmine_projectname"])
        print "loaded issues:", issues

        self.sort_issues(issues)

        print
        print "listing all open issues:", self.open_issues
        for issue in self.open_issues.values():
            self.print_issue(issue)

        print
        print "listing all assigned issues:", self.assigned_issues
        for issue in self.assigned_issues.values():
            self.print_issue(issue)