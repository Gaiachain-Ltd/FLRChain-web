<template>
  <ResetAuthCard></ResetAuthCard>
</template>

<script>
export default {
  layout: "auth",
  auth: false,
  components: {
    ResetAuthCard: () => import("@/components/cards/ResetAuthCard"),
  },
};
</script>