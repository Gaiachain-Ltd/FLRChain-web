<template>
  <ForgotAuthCard></ForgotAuthCard>
</template>

<script>
export default {
  layout: "auth",
  auth: false,
  components: {
    ForgotAuthCard: () => import("@/components/cards/ForgotAuthCard"),
  },
};
</script>