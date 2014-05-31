# # To change this template, choose Tools | Templates
# # and open the template in the editor.
#
# ###################### defines ######################
#
# __author__ = "David"
# __date__ = "$17.05.2014 12:09:27$"
#
# ###################### imports ######################
#
# from RedmineManager import RedmineManager
# from TrelloManager import TrelloManager
# import ConfigManager
#
# ###################### main ######################
#
# if __name__ == "__main__":
#     print "Redmine-Trello"
#
#     try:
#
#
#         configManager = ConfigManager.ConfigManager(False)
#
#         configManager.loadConfigurationFromFiles()
#
#         # use this line to first generate keys and tokens that need to be filled in TrelloManager.py
#         #TrelloManager().get_oauth_token_and_secret()
#
#         #RedmineManager().redmine_first_steps()
#         #TrelloManager().trello_first_steps()
#
#         # TrelloManager().get_unlinked_cards("Redmine-Trello-Workflow")
#         # for card in TrelloManager().get_unlinked_cards("Redmine-Trello-Workflow"):
#         #     RedmineManager().create_issue_from_unlinked_card(card)
#         #
#         # TrelloManager().get_linked_cards("Redmine-Trello-Workflow")
#
#         print
#         print "Redmine-Trello FINISHED"
#
#     except Exception as e:
#         print
#         print e
#         print
#         print "Redmine-Trello CRASHED!"
#
#
