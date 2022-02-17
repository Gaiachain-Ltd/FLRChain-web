import { STATUS } from "@/constants/project";

const Utility = {
    statusValueByName(status) {
        switch (status) {
            case "fundraising":
                return STATUS.FUNDRAISING;
            case "active":
                return STATUS.ACTIVE;
            case "closed":
                return STATUS.CLOSED;
            default:
                return null;
        }
    },
    statusNameByValue(status) {
        switch (status) {
            case STATUS.FUNDRAISING:
                return "fundraising";
            case STATUS.ACTIVE:
                return "active";
            case STATUS.CLOSED:
                return "closed";
            default:
                return "all";
        }
    }
}

export { Utility };