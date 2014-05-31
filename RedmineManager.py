#
# import redmine
# from redmine.resultsets import ResourceSet
# import trello
# import TrelloManager
#
# ###################### redmine config ######################
#
# projectname_config = ""
# redmine_url = ""
# api_key = ""
#
# ###################### redmine functions ######################
#
#
# class RedmineManager:
#
#     redmine = None
#
#     open_issues = {}
#     assigned_issues = {}
#
#     def __init__(self):
#         self.redmine = redmine.Redmine(redmine_url, key=api_key, raise_attr_exception=False)
#
#     def __del__(self):
#         self.redmine = None
#
#     def create_issue_from_unlinked_card(self, card):
#         assert isinstance(card, trello.Card)
#         assert len(card.name.split("{")) == 1 and len(card.name.split("}")) == 1
#
#         # fetch card content
#         card.fetch()
#         ### cards as issue: issue name = card name + {card-ID}
#         issue_name = card.name + " {" + str(card.short_id) + "}"
#         print issue_name
#         print "ISSUE CREATION NOT YET IMPLEMENTED"
#         exit(1)
# # redmine create issue
#
# #check if there is a project for this card (boardname begins with Projectname)
#
#         ### checklists as sub-issues: sub-issue name = card name + [checklist name] + {checklist-ID}
#         # generate sub-issues
#         checklists = card.checklists
#         for checklist in checklists:
#             assert isinstance(checklist, trello.Checklist)
#             assert len(checklist.items) > 0
#             sub_issue_name = checklist.name + " [" + str(checklist.id) + "]{" + str(card.short_id) + "}"
#             print sub_issue_name
# # redmine create sub issues
#
#             ### checklist-items as sub-sub-issues: sub-sub-issue name = card name + [checklist name] + [checklist item name] + {checklistitem-ID}
#             for item in checklist.items:
#                 assert isinstance(item, dict)
#                 assert item.get("name") != None and item.get("id") != None
#                 print item
#                 sub_sub_issue_name = item["name"] + " (" + item["id"] + ")[" + str(checklist.id) + "]{" + str(card.short_id) + "}"
#                 print sub_sub_issue_name
# # redmine create sub sub issues
#
#         # add issue ID to card name
#
#
# # first try out functions ##### just use as templates
#     def print_resource_set(self, resourceset):
#         for entry in resourceset:
#             if isinstance(entry, ResourceSet):
#                 print "2 extracting value.."
#                 self.print_resource_set(entry)
#             else:
#                 print " ++ ", entry
#
#     def sort_issues(self, issues):
#         print "sorting issues into open and assigned:"
#
#         self.open_issues = {}
#         self.assigned_issues = {}
#
#         for issue in issues:
#             if issue.assigned_to_id:
#                 self.assigned_issues[issue.subject] = issue
#             else:
#                 self.open_issues[issue.subject] = issue
#         print "finished sorting issues."
#
#
#     def print_issue(self, issue):
#         print " issue: ", issue.subject
#         for attribute in dir(issue):
#             if attribute == "time_entries":
#                 self.print_time_entries(issue[attribute])
#             elif attribute == "children":
#                 print " skipped: ", attribute, "..because it was crashing.. why?"
#             elif isinstance(issue[attribute], ResourceSet):
#                 print "1 extracting value..", attribute
#                 self.print_resource_set(issue[attribute])
#             else:
#                 print "   - ", attribute, ":", issue[attribute]
#
#     def print_time_entries(self, time_entries):
#         print "    time_entries:"
#         for time_entry in time_entries:
#             print "    -- entry: "
#             for attribute in dir(time_entry):
#                 try:
#                     print "    --- ", attribute, ":", time_entry[attribute]
#                 except Exception as e:
#                     print
#                     print "!!", e
#                     print
#
#     def redmine_first_steps(self):
#
#         print ""
#         print "##################### Hello from RedmineManager ######################"
#         print
#
#         redmine_client = redmine.Redmine(redmine_url, key=api_key, raise_attr_exception=False)
#
#         project = redmine_client.project.get(projectname_config)
#         print "loaded project:", project.name, "from:", redmine_url, "object:", project
#
#         print "loading project issues.."
#         issues = redmine_client.issue.filter(project_id=projectname_config)
#         print "loaded issues:", issues
#
#         self.sort_issues(issues)
#
#         print
#         print "listing all open issues:", self.open_issues
#         for issue in self.open_issues.values():
#             self.print_issue(issue)
#
#         print
#         print "listing all assigned issues:", self.assigned_issues
#         for issue in self.assigned_issues.values():
#             self.print_issue(issue)