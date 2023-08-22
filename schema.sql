
DROP TABLE IF EXISTS promotion;
DROP TABLE IF EXISTS pilot;

CREATE TABLE IF NOT EXISTS promotion (
    PromotionID INTEGER PRIMARY KEY AUTOINCREMENT,
    PromotionName varchar(255),
    PromotionStartDate varchar(255),
    PromotionEndDate varchar(255),
    PromotionNationality varchar(255)
);

CREATE TABLE IF NOT EXISTS pilot (
    PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
    PromotionID INTEGER,
    PiloteName varchar(255),
    PiloteSurname varchar(255),
    PiloteCodeName varchar(255),
    PiloteNationality varchar(255),
    FOREIGN KEY (PilotID) REFERENCES pilot (PilotID),
    FOREIGN KEY (PromotionID) REFERENCES promotion (PromotionID)
);