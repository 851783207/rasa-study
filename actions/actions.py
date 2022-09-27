import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import UserUtteranceReverted, ConversationResumed
from rasa_sdk.executor import CollectingDispatcher

import sqlite3

from rasa_sdk.types import DomainDict


# class ValidateEmailForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_email_form"
#
#     def validate_email(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: DomainDict,
#     ) -> Dict[Text, Any]:
#
#         # If the name is super short, it might be wrong.
#         order = tracker.latest_message.get("text")
#         if len(order) == 0:
#             dispatcher.utter_message(text="Shouldn't your order number be made of actual order number?")
#             return {"email": None}
#         elif len(order) < 4:
#             dispatcher.utter_message(
#                 text="That order number is way too short. How about you provide me a 4-character order number?")
#             return {"email": None}
#         elif len(order) > 4:
#             dispatcher.utter_message(
#                 text="That order number is way too long. How about you provide me a 4-character order number?")
#             return {"email": None}
#
#         return {"email": order}

class ValidateForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_email_form"

    def validate_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        # email = slot_value('email')
        # email = tracker.latest_message.get("text")
        pattern = re.compile(r'^[\w]{1,19}@((163)|(qq)|(126)|(gmail)).((com)|(cn))$', re.I)
        email = tracker.get_slot("email")
        e = pattern.match(str(email))
        if e is None:
            dispatcher.utter_message(text="{} is not a valid email".format(email))
            # return [UserUtteranceReverted()]
            return {"email": None}
        else:
            conn = sqlite3.connect("D:/bot/actions/customer.db")
            cursor = conn.cursor()
            query1 = "CREATE TABLE IF NOT EXISTS customer (id integer PRIMARY KEY,email text NOT NULL, phone integer NOT NULL);"
            cursor.execute(query1)
            query = "SELECT * FROM customer WHERE email = ?"
            e = email,
            cursor.execute(query, e)
            if not cursor.fetchall():
                dispatcher.utter_message(text="Email address {} does not exist in the database".format(email))
                cursor.close()
                conn.commit()
                conn.close()
                # return [UserUtteranceReverted()]
                return {"email": None}
            else:
                # if tracker.slots.get('phone_number'):
                #     phone = tracker.slots.get('phone_number')
                #     pattern = re.compile(r'(((\+86)|(86))?(1)\d{10})|([1-9][0-9]{10}|((\d{3,4}-)?\d{7,8}))')
                #     p = pattern.match(phone)
                #     if p is None:
                #         dispatcher.utter_message(text="Please enter a valid phone number")
                #         # return [UserUtteranceReverted()]
                #         return {"phone_number": None}
                # else:
                cursor.close()
                conn.commit()
                conn.close()
                return {"email": email}


class ActionPhone(Action):

    def name(self) -> Text:
        return "upload_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot('phone_number')
        email = tracker.get_slot('email')
        pattern = re.compile(r'(((\+86)|(86))?(1)\d{10})|([1-9][0-9]{10}|((\d{3,4}-)?\d{7,8}))')
        p = pattern.match(phone)
        if p is None:
            dispatcher.utter_message(text="Please enter a valid phone number")
            return [UserUtteranceReverted()]
            # return {"phone_number": None}
        else:
            conn = sqlite3.connect("D:/bot/actions/customer.db")
            cursor = conn.cursor()
            query1 = "CREATE TABLE IF NOT EXISTS connect (id integer PRIMARY KEY,email text NOT NULL, phone integer NOT NULL);"
            cursor.execute(query1)
            query3 = "SELECT email FROM connect WHERE email = ?"
            e = email,
            cursor.execute(query3, e)
            if not cursor.fetchall():
                query2 = "INSERT INTO connect(email, phone) VALUES(?, ?)"
                cursor.execute(query2, (email, phone))
                cursor.close()
                conn.commit()
                conn.close()
                return []


# class PhoneForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_phone_form"
#
#     def validate_phone(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         phone = tracker.get_slot('phone_number')
#         email = tracker.get_slot('email')
#         pattern = re.compile(r'(((\+86)|(86))?(1)\d{10})|([1-9][0-9]{10}|((\d{3,4}-)?\d{7,8}))')
#         p = pattern.match(phone)
#         if p is None:
#             dispatcher.utter_message(text="Please enter a valid phone number")
#             # return [UserUtteranceReverted()]
#             return {"phone_number": None}
#         else:
#             conn = sqlite3.connect("D:/bot/actions/customer.db")
#             cursor = conn.cursor()
#             query1 = "CREATE TABLE IF NOT EXISTS connect (id integer PRIMARY KEY,email text NOT NULL, phone integer NOT NULL);"
#             cursor.execute(query1)
#             query3 = "SELECT email FROM connect WHERE email = ?"
#             e = email,
#             cursor.execute(query3, e)
#             if not cursor.fetchall():
#                 query2 = "INSERT INTO connect(email, phone) VALUES(?, ?)"
#                 cursor.execute(query2, (email, phone))
#                 cursor.close()
#                 conn.commit()
#                 conn.close()
#                 return []
