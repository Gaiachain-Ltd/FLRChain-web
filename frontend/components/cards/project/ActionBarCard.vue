<template>
  <v-card class="card-style">
    <v-card-text>
      <v-layout row ma-0 justify-center>
        <v-flex shrink mr-3>
          <ActionButton label="Cancel" color="error"></ActionButton>
        </v-flex>
        <v-flex shrink ml-3>
          <ActionButton label="Save"></ActionButton>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
};
</script>

<style scoped>
.card-style {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    margin-bottom: -7px !important;
    margin-left: 268px !important;
    margin-right: 12px !important;
}
</style>