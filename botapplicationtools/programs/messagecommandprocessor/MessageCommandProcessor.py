"""Program to process message commands"""

from praw import Reddit
from praw.models import Message
from praw.models.util import stream_generator


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
