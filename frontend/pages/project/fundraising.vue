<template>
  <IndexPage :status="FUNDRAISING_STATUS"></IndexPage>
</template>

<script>
import { STATUS } from "@/constants/project";

export default {
  data() {
    return {
      FUNDRAISING_STATUS: STATUS.FUNDRAISING,
    };
  },
  components: {
    IndexPage: () => import("@/pages/index.vue"),
  },
};
</script>