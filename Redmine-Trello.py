# To change this template, choose Tools | Templates
# and open the template in the editor.

###################### defines ######################

__author__ = ""
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

    unlinkedCards = trelloManager.get_unlinked_cards(configuration["trello_projectname"])
    for card in unlinkedCards:
        #redmineManager.create_issue_from_card(card)

        redmineManager.create_all_issues_from_card(card)

    # for card in TrelloManager().get_unlinked_cards("Redmine-Trello-Workflow"):
    #     RedmineManager().create_issue_from_unlinked_card(card)
    #
    trelloManager.get_linked_cards(configuration["trello_projectname"])

    print "TODO:"
    print " - export all relevant trello fields (planned time, due date, ..)"
    print " - update already existing issues with plausible new values from trello"
    print " - update trello checklist items from redmine issue status"
    print " - move trello card to 'in progress board', when at least 1 subtask has status in progress"
    print " - move trello card to 'review board', when all subtasks reach 'resolved' or any higher status"
    print
    print "## need to think about:"
    print " - mark issues when card is moved to another board via trello"
    print " - generate/create/export gantt to trello (where ever in there)"

    print
    print "Redmine-Trello FINISHED"

    try:        ## disabled this try-catch (was whole code) to have better debuggable output in console)
        None
    except Exception as e:
        print
        print e
        print
        print "Redmine-Trello CRASHED!"


