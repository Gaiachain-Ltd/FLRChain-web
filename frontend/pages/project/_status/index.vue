<template>
  <IndexPage :status="redirectByName()"></IndexPage>
</template>

<script>
import { STATUS } from "@/constants/project";

export default {
  methods: {
    redirectByName() {
      switch(this.$route.params.status) {
        case "fundraising":
          return STATUS.FUNDRAISING;
        case "active":
          return STATUS.ACTIVE;
        case "closed":
          return STATUS.CLOSED;
        default:
          return "";
      }
    }
  },
  components: {
    IndexPage: () => import("@/pages/index.vue"),
  },
};
</script>