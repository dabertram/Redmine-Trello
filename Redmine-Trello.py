# To change this template, choose Tools | Templates
# and open the template in the editor.

###################### defines ######################

__author__ = "David"
__date__ = "$17.05.2014 12:09:27$"

###################### imports ######################

from RedmineManager import RedmineManager
from TrelloManager import TrelloManager
import ConfigManager

###################### main ######################

if __name__ == "__main__":
    print "Redmine-Trello"

    # try:

    configManager = ConfigManager.ConfigManager(False)
    configManager.loadConfigurationFromFiles()

    configuration = configManager.redmineTrelloConfiguration

    trelloManager = TrelloManager()
    trelloManager.connect_trello(configuration)

    redmineManager = RedmineManager()
    redmineManager.connect_redmine(configuration)

    #redmineManager.redmine_first_steps()

    unlinkedCards = trelloManager.get_unlinked_cards("Redmine-Trello-Workflow")
    for card in unlinkedCards:
        #redmineManager.create_issue_from_card(card)

        redmineManager.create_all_issues_from_card(card)

    # for card in TrelloManager().get_unlinked_cards("Redmine-Trello-Workflow"):
    #     RedmineManager().create_issue_from_unlinked_card(card)
    #
    trelloManager.get_linked_cards("Redmine-Trello-Workflow")

    print
    print "Redmine-Trello FINISHED"

    try:
        None
    except Exception as e:
        print
        print e
        print
        print "Redmine-Trello CRASHED!"


