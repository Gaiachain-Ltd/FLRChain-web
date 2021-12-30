<template>
  <IndexPage :status="ACTIVE_STATUS"></IndexPage>
</template>

<script>
import { STATUS } from "@/constants/project";

export default {
  data() {
    return {
      ACTIVE_STATUS: STATUS.ACTIVE,
    };
  },
  components: {
    IndexPage: () => import("@/pages/index.vue"),
  },
};
</script>