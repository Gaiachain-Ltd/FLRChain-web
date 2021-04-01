<template>
  <v-layout column>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
      label
    }}</DefaultText>
    <v-text-field
      class="text-field-style"
      :placeholder="placeholder"
      solo
      flat
      :background-color="
        hasError ? '#FBF7F7' : $vuetify.theme.themes.light.tertiary
      "
      height="50"
      v-model="internalText"
      :type="password ? 'password' : 'text'"
      :required="required"
      :rules="rules"
      @blur="validate"
    ></v-text-field>
  </v-layout>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    text: {
      type: String,
    },
    password: {
      type: Boolean,
      default: false,
    },
    rules: {
      type: Array,
      default: () => [],
    },
    required: {
      type: Boolean,
      default: false,
    },
    error: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      hasError: false,
    };
  },
  watch: {
    internalText() {
      this.validate();
    },
    error() {
      this.internalError = this.error;
    },
  },
  computed: {
    internalText: {
      get() {
        return this.text;
      },
      set(value) {
        this.$emit("update:text", value);
      },
    },
    internalError: {
      get() {
        return this.hasError;
      },
      set(value) {
        this.hasError = value;
        this.$emit("update:error", value);
      },
    },
  },
  methods: {
    validate() {
      for (let index = 0; index < this.rules.length; index++) {
        const rule = this.rules[index];
        if (rule(this.internalText) !== true) {
          this.hasError = true;
          return;
        }
      }
      this.hasError = false;
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
  },
};
</script>

<style scoped lang="scss">
.text-field-style {
  border-radius: 7px !important;
}
</style>

<style lang="scss">
.text-field-style .v-text-field__details {
  padding: 0 !important;
}
</style>