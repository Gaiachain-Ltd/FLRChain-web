<template>
  <IndexPage :status="CLOSED_STATUS"></IndexPage>
</template>

<script>
import { STATUS } from "@/constants/project";

export default {
  data() {
    return {
      CLOSED_STATUS: STATUS.CLOSED,
    };
  },
  components: {
    IndexPage: () => import("@/pages/index.vue"),
  },
};
</script>