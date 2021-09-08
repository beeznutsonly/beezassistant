"""Program to process message commands"""
from praw import Reddit
from praw.models.util import stream_generator


def execute(
        commands,
        prawReddit: Reddit,
        stopCondition
):
    """Execute the program"""

    messageStream = stream_generator(
        prawReddit.inbox.messages,
        pause_after=0
    )

    for message in messageStream:
        if message is None:
            if stopCondition():
                break
            continue
        if message.subject.startswith("!"):
            command = message.subject[1:]
            if command in commands.keys():
                commands[command].processMessage(message)
