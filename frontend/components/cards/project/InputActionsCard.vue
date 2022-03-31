<template>
  <v-layout column>
    <v-layout
      column
      v-for="(action, actionIndex) in project.actions"
      :key="actionIndex"
    >
      <v-layout column mb-6 class="border-wrapper pa-6">
        <ActionForm
          :actionIndex="actionIndex"
          :project="project"
          v-model="project.actions[actionIndex]"
          :readonly="readonly"
          @add:milestone="() => onAddMilestone(action)"
          @add:task="onAddTask"
          @delete:action="() => onDeleteAction(actionIndex)"
          @delete:milestone="
            (milestoneIndex) => onDeleteMilestone(action, milestoneIndex)
          "
          @delete:task="onDeleteTask"
        ></ActionForm>
        <v-layout justify-center>
          <DefaultIconButton
            v-if="!readonly"
            :config="addActionBtnConfig"
            @clicked="() => onAddAction()"
          ></DefaultIconButton>
        </v-layout>
      </v-layout>
    </v-layout>
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
  data() {
    return {
      deleteBtnConf: {
        iconOn: require("@/assets/icons/remove.svg"),
        label: "Delete",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.error,
        spacing: 2,
      },
      addTaskBtnConfig: {
        iconOn: require("@/assets/icons/add_task.svg"),
        label: "Add task",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
      addMilestoneBtnConfig: {
        iconOn: require("@/assets/icons/add_task.svg"),
        label: "Add milestone",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
      addActionBtnConfig: {
        iconOn: require("@/assets/icons/add_milestone.svg"),
        label: "Add FLR action",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    ActionForm: () => import("@/components/forms/project/ActionForm"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
  methods: {
    defaultAction() {
      return {
        name: "",
        milestones: [this.defaultMilesone()],
      };
    },
    defaultMilesone() {
      return {
        name: "",
        tasks: [this.defaultTask()],
      };
    },
    defaultTask() {
      return {
        name: "",
        instructions: "",
        batch: "0",
        reward: "0",
        count: 1,
      };
    },
    onAddAction() {
      this.$set(this.project, "actions", [
        ...(this.project.actions || []),
        this.defaultAction(),
      ]);
    },
    onAddMilestone(action) {
      this.$set(action, "milestones", [
        ...(action.milestones || []),
        this.defaultMilesone(),
      ]);
    },
    onAddTask(milestone) {
      this.$set(milestone, "tasks", [
        ...(milestone.tasks || []),
        this.defaultTask(),
      ]);
    },
    onDeleteAction(index) {
      this.project.actions.splice(index, 1);
    },
    onDeleteMilestone(action, index) {
      action.milestones.splice(index, 1);
    },
    onDeleteTask(milestone, index) {
      milestone.tasks.splice(index, 1);
    },
  },
};
</script>