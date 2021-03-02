<template>
  <LoginAuthCard></LoginAuthCard>
</template>

<script>
export default {
  layout: "auth",
  components: {
    LoginAuthCard: () => import("@/components/cards/LoginAuthCard"),
  },
};
</script>