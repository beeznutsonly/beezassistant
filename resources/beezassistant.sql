CREATE TABLE BotCredentials (
    user_agent     NOT NULL,
    client_id      NOT NULL,
    client_secret  NOT NULL,
    username       NOT NULL,
    password       NOT NULL,
    PRIMARY KEY (
        client_id,
        client_secret
    )
);

CREATE TABLE PostInfo (
    id          VARCHAR PRIMARY KEY
                        NOT NULL,
    Title       VARCHAR NOT NULL,
    TimeCreated INTEGER NOT NULL
);

CREATE TABLE SceneInfo (
    Movie VARCHAR NOT NULL,
    Star1 VARCHAR NOT NULL,
    Star2 VARCHAR NOT NULL,
    PRIMARY KEY (
        Movie,
        Star1,
        Star2
    )
);

CREATE TABLE SubmissionsAndInfo (
    submission_id VARCHAR PRIMARY KEY
                          NOT NULL,
    Movie         VARCHAR NOT NULL,
    Star1         VARCHAR NOT NULL,
    Star2         VARCHAR NOT NULL,
    FOREIGN KEY (
        submission_id
    )
    REFERENCES PostInfo (id) ON DELETE CASCADE
                             ON UPDATE CASCADE,
    FOREIGN KEY (
        Movie,
        Star1,
        Star2
    )
    REFERENCES SceneInfo (Movie,
    Star1,
    Star2) ON DELETE CASCADE
           ON UPDATE CASCADE
);

CREATE VIEW StarPairView AS
    SELECT SubmissionsAndInfo.submission_id,
           SubmissionsAndInfo.Star1,
           SubmissionsAndInfo.Star2,
           PostInfo.Title
      FROM SubmissionsAndInfo
           INNER JOIN
           PostInfo ON SubmissionsAndInfo.submission_id = PostInfo.id
     ORDER BY Star1,
              Star2 ASC;

CREATE VIEW StarView AS
    SELECT *
      FROM (
               SELECT SubmissionsAndInfo.submission_id,
                      SubmissionsAndInfo.Star1 AS Star,
                      PostInfo.Title
                 FROM SubmissionsAndInfo
                      INNER JOIN
                      PostInfo ON SubmissionsAndInfo.submission_id = PostInfo.id
               UNION
               SELECT SubmissionsAndInfo.submission_id,
                      SubmissionsAndInfo.Star2 AS Star,
                      PostInfo.Title
                 FROM SubmissionsAndInfo
                      INNER JOIN
                      PostInfo ON SubmissionsAndInfo.submission_id = PostInfo.id
           )
     ORDER BY Star ASC;
