"""Program to process message commands"""

import time

from praw import Reddit
from praw.models import Message
from praw.models.util import stream_generator
from prawcore.exceptions import RequestException, ServerError


def execute(
        commandProcessors,
        prawReddit: Reddit,
        stopCondition
):
    """Execute the program"""
        
    # Create new stream of unread inbox messages
    unreadStream = stream_generator(
        prawReddit.inbox.unread,
        pause_after=0
    )

    while not stopCondition():

        try:

            for unread in unreadStream:
                # Handle "pause" token
                if unread is None:
                    # Exit program if stop condition
                    # satisfied
                    if stopCondition():
                        break
                    continue

                # Process if unread item is Message
                if isinstance(unread, Message):
                    message = unread

                    # Process if message is message command
                    if message.subject.startswith("!"):
                        command = message.subject[1:]

                        # Process if command is included in
                        # provided commands
                        if command in commandProcessors.keys():
                            print(command)
                            print(commandProcessors.keys())
                            commandProcessors[command].processMessage(
                                message
                            )

        # Handle for connection issues with the Reddit API                    
        except (RequestException, ServerError):

            time.sleep(30)  
