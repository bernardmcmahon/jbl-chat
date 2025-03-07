from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import json
import random
from datetime import datetime, timedelta


def random_datetime(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    random_seconds = random.randrange(int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


class Command(BaseCommand):
    help = 'Used for adding default password to "admin" for all users that have no password set.'

    def handle(self, *args, **options):

        # Define the time range for sent_at timestamps
        start_date = datetime(2023, 1, 1)
        end_date = datetime.today()

        # Sample messages to choose from
        sample_messages = [
            "Hi, how are you doing today?",
            "Can you help me with the report?",
            "I'll be there in 10 minutes.",
            "Did you check the latest update?",
            "Let's catch up later.",
            "I have sent the documents.",
            "Thanks for your assistance!",
            "Can we discuss the new project?",
            "Please review the changes.",
            "I'll get back to you soon."
        ]

        messages = []
        num_messages = 1000
        user_ids = [1, 2, 3, 4, 5]

        for i in range(1, num_messages + 1):
            # Randomly choose sender and receiver ensuring they are different.
            sender = random.choice(user_ids)
            recipient = random.choice(user_ids)
            while recipient == sender:
                recipient = random.choice(user_ids)

            # Generate a random sent_at timestamp.
            sent = random_datetime(start_date, end_date)
            sent_str = sent.isoformat() + "Z"

            message = {
                "model": "chat.message",
                "pk": i,
                "fields": {
                    "sender": sender,
                    "recipient": recipient,
                    "content": random.choice(sample_messages),
                    "sent_at": sent_str,
                }
            }
            messages.append(message)

        # Save the generated fixture to a file.
        with open("messages_fixture.json", "w") as f:
            json.dump(messages, f, indent=2)

        print("Fixture file 'messages_fixture.json' with 1000 messages generated.")