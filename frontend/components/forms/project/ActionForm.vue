<template>
  <v-form ref="form" @submit.prevent>
    <v-layout column>
      <v-layout ma-0 mb-3 justify-center>
        <DefaultText color="#02595b" size="24" bold>{{
          `FLR Action ${actionIndex + 1}`
        }}</DefaultText>
        <DefaultIconButton
          class="ml-6"
          v-if="project.actions.length > 1"
          :config="deleteBtnConf"
          @clicked="onDeleteAction"
        ></DefaultIconButton>
        <v-spacer></v-spacer>
        <CollapseButton v-model="collapsed"></CollapseButton>
      </v-layout>
      <v-layout column v-show="!collapsed">
        <TextInput
          label="FLR action name*"
          v-model="action.name"
          :rules="[...requiredRules, ...maxLengthRules()]"
          :readonly="readonly"
          required
        ></TextInput>
      </v-layout>
      <v-layout column mb-6 class="border-wrapper pa-6" v-show="!collapsed">
        <v-layout
          column
          v-for="(milestone, milestoneIndex) in action.milestones"
          :key="milestoneIndex"
        >
          <MilestoneForm
            ref="milestoneForm"
            :actionIndex="actionIndex"
            :milestoneIndex="milestoneIndex"
            :action="action"
            v-model="action.milestones[milestoneIndex]"
            :readonly="readonly"
            @add:task="() => onAddTask(milestone)"
            @delete:milestone="() => onDeleteMilestone(milestoneIndex)"
            @delete:task="(taskIndex) => onDeleteTask(milestone, taskIndex)"
          ></MilestoneForm>
        </v-layout>
        <v-layout justify-center :class="collapsed ? 'mt-2' : 'mt-6'">
          <DefaultIconButton
            v-if="!readonly"
            :config="addMilestoneBtnConfig"
            @clicked="onAddMilestone"
          ></DefaultIconButton>
        </v-layout>
      </v-layout>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    actionIndex: {},
    project: {},
    value: {},
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      collapsed: false,
      deleteBtnConf: {
        iconOn: require("@/assets/icons/remove.svg"),
        label: "Delete",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.error,
        spacing: 2,
      },
      addMilestoneBtnConfig: {
        iconOn: require("@/assets/icons/add_task.svg"),
        label: "Add milestone",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
    };
  },
  computed: {
    action: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    onAddMilestone() {
      this.$emit("add:milestone");
    },
    onAddTask(milestone) {
      this.$emit("add:task", milestone);
    },
    onDeleteAction() {
      this.$emit("delete:action");
    },
    onDeleteMilestone(milestoneIndex) {
      this.$emit("delete:milestone", milestoneIndex);
    },
    onDeleteTask(milestone, taskIndex) {
      this.$emit("delete:task", milestone, taskIndex);
    },
    validate() {
      const f = this.$refs.form.validate();
      for (let index = 0; index < this.$refs.milestoneForm.length; index++) {
        const element = this.$refs.milestoneForm[index];
        if (!element.validate()) {
          return false;
        }
      }
      return f;
    },
  },
  components: {
    CollapseButton: () => import("@/components/buttons/CollapseButton"),
    MilestoneForm: () => import("@/components/forms/project/MilestoneForm"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
  },
};
</script>