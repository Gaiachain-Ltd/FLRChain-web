<template>
  <v-layout column class="border-wrapper pa-3">
    <BudgetForm :project="project"></BudgetForm>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    BudgetForm: () => import("@/components/forms/project/BudgetForm"),
  },
};
</script>