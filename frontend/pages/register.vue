<template>
  <RegisterAuthCard></RegisterAuthCard>
</template>

<script>
export default {
  layout: "auth",
  components: {
    RegisterAuthCard: () => import("@/components/cards/RegisterAuthCard"),
  },
};
</script>