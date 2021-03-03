<template>
  <LoginAuthCard></LoginAuthCard>
</template>

<script>
export default {
  layout: "auth",
  auth: false,
  components: {
    LoginAuthCard: () => import("@/components/cards/LoginAuthCard"),
  },
};
</script>