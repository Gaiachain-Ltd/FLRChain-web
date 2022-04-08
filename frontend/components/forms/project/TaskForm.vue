<template>
  <v-form ref="form">
    <v-layout column ma-0>
      <v-layout ma-0 align-center :class="collapsed && 'mb-3'">
        <DefaultText color="#06bcc1" bold size="18">{{
          `Task ${actionIndex}.${milestoneIndex}.${index + 1}`
        }}</DefaultText>
        <DefaultIconButton
          class="ml-6"
          v-if="showDeleteBtn && !readonly"
          :config="deleteBtnConf"
          @clicked="$emit('delete')"
        ></DefaultIconButton>
        <v-spacer></v-spacer>
        <CollapseButton v-model="collapsed"></CollapseButton>
      </v-layout>
      <DefaultText
        v-show="!collapsed"
        class="mb-2 mt-1"
        color="#06bcc1"
        size="14"
        >Task Description</DefaultText
      >
      <v-layout v-show="!collapsed" column>
        <TextInput
          label="Task name*"
          v-model="task.name"
          placeholder="Please enter task name..."
          :rules="[...requiredRules, ...maxLengthRules()]"
          :readonly="readonly"
          required
        ></TextInput>
        <DataTypeTags
          ref="dataTypeTag"
          :task.sync="task"
          :readonly="readonly"
        ></DataTypeTags>
        <DataRequiredTags
          ref="dataReqTags"
          :task.sync="task"
          :readonly="readonly"
        ></DataRequiredTags>
        <TextAreaInput
          label="Instructions for steward"
          v-model="task.instructions"
          :rules="[...maxLengthRules(2000)]"
          :readonly="readonly"
        ></TextAreaInput>
        <DefaultText class="mb-2 mt-1" color="#06bcc1" size="14"
          >Task Rewards</DefaultText
        >
        <TextInput
          label="Batch*"
          v-model="task.batch"
          :rules="[...requiredRules, ...decimalRules]"
          :icon="icon"
          :readonly="readonly"
          required
        ></TextInput>
        <TextInput
          label="How much will a steward receive upon confirmation of the task?*"
          v-model="task.reward"
          :rules="[...requiredRules, ...decimalRules, ...nonZeroDecimalRules]"
          :icon="icon"
          :readonly="readonly"
          required
        ></TextInput>
        <TextInput
          label="How many times can this task be performed?*"
          v-model="task.count"
          :rules="[...requiredRules, ...oneOrMoreInteger, ...integerRules]"
          :readonly="readonly"
          required
        ></TextInput>
        <TextInput
          label="Task total"
          v-model="total"
          :icon="icon"
          readonly
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
    actionIndex: {
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
        spacing: 1,
        iconSize: 16,
      },
      icon: require("@/assets/icons/currency.svg"),
      collapsed: false,
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
    total() {
      return parseFloat(
        (
          parseFloat(this.task.batch) +
          parseFloat(this.task.reward) * parseFloat(this.task.count)
        ).toFixed(6)
      );
    },
  },
  components: {
    CollapseButton: () => import("@/components/buttons/CollapseButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    TextAreaInput: () => import("@/components/inputs/TextAreaInput"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
    DataTypeTags: () => import("@/components/inputs/DataTypeTags"),
    DataRequiredTags: () => import("@/components/inputs/DataRequiredTags"),
  },
  methods: {
    validate() {
      const drt = this.$refs.dataReqTags.validate();
      const dtt = this.$refs.dataTypeTag.validate();
      const form = this.$refs.form.validate();
      return drt && dtt & form;
    },
  },
};
</script>
