<template>
  <RegisterAuthCard></RegisterAuthCard>
</template>

<script>
export default {
  layout: "auth",
  auth: false,
  components: {
    RegisterAuthCard: () => import("@/components/cards/RegisterAuthCard"),
  },
};
</script>