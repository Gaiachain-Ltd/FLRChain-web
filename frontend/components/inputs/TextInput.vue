<template>
  <v-layout column>
    <DefaultText :size="12" :color="$vuetify.theme.themes.light.senary">{{
      label
    }}</DefaultText>
    <v-text-field
      :class="['text-field-style', readonly && 'mt-0 pt-0']"
      :placeholder="placeholder"
      :solo="!readonly"
      :readonly="readonly"
      :disabled="readonly"
      flat
      :background-color="
        readonly
          ? 'white'
          : hasError
          ? '#FBF7F7'
          : $vuetify.theme.themes.light.tertiary
      "
      height="50"
      v-model="internalText"
      :type="type"
      :required="required"
      :rules="rules"
      v-mask="mask ? `${mask}` : undefined"
      @blur="validate"
    >
      <v-layout v-if="icon" column pr-2 align-center slot="prepend-inner">
        <DefaultSVGIcon
          :class="readonly && 'readonly-icon'"
          :icon="icon"
        ></DefaultSVGIcon>
      </v-layout>
      <v-layout slot="append">
        <slot name="append"></slot>
      </v-layout>
    </v-text-field>
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
    value: {},
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
    icon: {
      type: String,
    },
    type: {
      type: String,
      default: "text",
    },
    mask: {
      type: String,
      default: undefined,
    },
    readonly: {
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
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
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
    DefaultSVGIcon: () => import("@/components/icons/DefaultSVGIcon"),
  },
};
</script>

<style scoped lang="scss">
.text-field-style {
  border-radius: 7px !important;
}
.readonly-icon {
  margin-top: 8px !important;
}
</style>

<style lang="scss">
.text-field-style .v-text-field__details {
  padding: 0 !important;
}
</style>