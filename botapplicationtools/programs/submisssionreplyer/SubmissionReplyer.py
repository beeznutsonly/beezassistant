
def execute(
        submissionStream,
        submissionReplyerStorage,
        stopCondition
):
    submissionReplyerCommentedDAO = submissionReplyerStorage \
        .getSubmissionReplyerCommentedDAO
    submissionReplyDetailsDAO = submissionReplyerStorage \
        .getSubmissionReplyDetailsDAO
    for submission in submissionStream:

        if submission is None:
            if stopCondition():
                break
            continue

        if submissionReplyerCommentedDAO.checkExists(submission.id):
            continue

        if submissionReplyDetailsDAO.checkExists(submission.url):
            submissionReplyDetails = submissionReplyDetailsDAO.retrieve(
                submission.url
            )
            submission.reply(submissionReplyDetails.getReply)
            submissionReplyerCommentedDAO.acknowledgeSubmission(
                submission.id, submissionReplyDetails.getUrl
            )

            if submissionReplyDetails.getOneOff:
                submissionReplyDetailsDAO.remove(
                    submissionReplyDetails.getUrl
                )
