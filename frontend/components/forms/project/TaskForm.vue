<template>
  <v-form ref="form">
    <v-layout column ma-0>
      <v-layout ma-0 mb-3>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          `Task ${milestoneIndex}.${index + 1}`
        }}</DefaultText>
        <v-spacer></v-spacer>
        <DefaultIconButton
          v-if="showDeleteBtn"
          :config="deleteBtnConf"
          @clicked="$emit('delete')"
        ></DefaultIconButton>
      </v-layout>
      <v-layout column>
        <TextInput
          label="Task name*"
          v-model="task.name"
          placeholder="Please enter task name..."
          :rules="requiredRules"
          :readonly="readonly"
          required
        ></TextInput>
        <TextAreaInput
          label="Instructions for steward"
          v-model="task.instructions"
          :readonly="readonly"
        ></TextAreaInput>
        <TextInput
          label="Batch"
          v-model="task.batch"
          :rules="requiredRules"
          :icon="icon"
          :readonly="readonly"
          required
        ></TextInput>
        <TextInput
          label="How much will a steward receive upon confirmation of the task?"
          v-model="task.reward"
          :rules="[...requiredRules, ...decimalRules, ...nonZeroDecimalRules]"
          :icon="icon"
          :readonly="readonly"
          required
        ></TextInput>
        <TextInput
          label="How many times can this task be performed?"
          v-model="task.count"
          :rules="requiredRules"
          :readonly="readonly"
          required
        ></TextInput>
      </v-layout>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    value: {},
    index: {
      type: Number,
      default: 1,
    },
    milestoneIndex: {
      type: Number,
      default: 1,
    },
    showDeleteBtn: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      deleteBtnConf: {
        iconOn: require("@/assets/icons/remove.svg"),
        label: "Delete",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.error,
        spacing: 2,
      },
      icon: require("@/assets/icons/currency.svg"),
    };
  },
  computed: {
    task: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>
