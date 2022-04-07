<template>
  <v-layout column class="border-wrapper pa-3">
    <BudgetForm ref="form" :project="project" :readonly="readonly"></BudgetForm>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    BudgetForm: () => import("@/components/forms/project/BudgetForm"),
  },
  methods: {
    validate() {
      this.$refs.form.validate();
    },
  },
};
</script>