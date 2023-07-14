from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions import data

class DetermineQueryTypeAction(Action):
    def name(self) -> Text:
        return "custom_select_function"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Check the user's intent
        intent = tracker.latest_message['intent'].get('name')

        if intent == 'balance_inquiry':
            # Set the slot value as 'account_balance' if the user is asking for an account balance check
            return [SlotSet('function', 'account_balance')]
        elif intent == 'transaction_inquiry':
            # Set the slot value as 'transaction_history' if the user is asking for transaction history
            return [SlotSet('function', 'transaction_history')]
        else:
            # Set the slot value as None if the intent does not match the expected queries
            return [SlotSet('function', None)]
        

class CustomAction(Action):
    def name(self) -> Text:
        return "custom_logic_function"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Perform custom logic
        s_name = tracker.get_slot("name").lower()
        s_account = tracker.get_slot("account")
        s_number = tracker.get_slot("number")
        s_function = tracker.get_slot("function")

        temp = data.check_avilable(s_name, s_account, s_number, data.d_data)

        if temp == 0:
            return [FollowupAction("utter_credentials_mismatch")]
        else:
            if s_function == 'account_balance':
                return [SlotSet('balance', data.d_data[s_name]['balance']), FollowupAction("utter_balance_info")]
            elif s_function == 'transaction_history':
                return [SlotSet('balance', data.trans_hist[s_name]), FollowupAction("utter_transaction_info")]


class ClearSlotsAction(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Clear all slots
        slots_to_clear = tracker.slots.keys()
        slot_events = [SlotSet(slot, None) for slot in slots_to_clear]
        
        # Return the slot events to clear all slots
        return slot_events

