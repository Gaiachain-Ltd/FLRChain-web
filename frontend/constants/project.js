const STATUS = {
    FUNDRAISING: 1,
    ACTIVE: 2,
    CLOSED: 3,
};

const STATE = {
    INITIAL: 0,
    CREATED: 1,
    INITIALIZED: 2,
    POSTPONED: 3,
    STARTED: 4,
    FINISHED: 5,
    DELETED: 6
}

const APPROVAL = {
    INITIAL: 0,
    ACCEPTED: 1,
    REJECTED: 2
}

const SYNC = {
    INITIAL: 0,
    TO_SYNC: 1,
    SYNCED: 2
};

const TAG_TYPES = {
    TEXT_TYPE: 0,
    NUMBER_TYPE: 1,
    AREA_TYPE: 2,
    PHOTO_TYPE: 3
};

export { STATUS, STATE, SYNC, APPROVAL, TAG_TYPES };
