<template>
  <v-layout column>
    <v-layout
      column
      v-for="(action, actionIndex) in project.actions"
      :key="actionIndex"
    >
      <v-layout column mb-6 class="border-wrapper pa-6">
        <v-layout ma-0 mb-3 justify-center>
          <DefaultText color="#02595b" size="24" bold>{{
            `FLR Action ${actionIndex + 1}`
          }}</DefaultText>
          <v-spacer></v-spacer>
          <DefaultIconButton
            v-if="project.actions.length > 1"
            :config="deleteBtnConf"
            @clicked="() => onDeleteAction(actionIndex)"
          ></DefaultIconButton>
        </v-layout>
        <ActionForm
          v-model="project.actions[actionIndex]"
          :readonly="readonly"
        ></ActionForm>
        <v-layout
          column
          v-for="(milestone, milestoneIndex) in action.milestones"
          :key="milestoneIndex"
        >
          <v-layout column mb-6 class="border-wrapper pa-6">
            <v-layout ma-0 mb-3 justify-center>
              <DefaultText color="#00868a" size="20" bold>{{
                `Milesone ${actionIndex + 1}.${milestoneIndex + 1}`
              }}</DefaultText>
              <v-spacer></v-spacer>
              <DefaultIconButton
                v-if="action.milestones.length > 1"
                :config="deleteBtnConf"
                @clicked="() => onDeleteMilestone(action, milestoneIndex)"
              ></DefaultIconButton>
            </v-layout>
            <v-layout column>
              <MilestoneForm
                v-model="action.milestones[milestoneIndex]"
                :readonly="readonly"
              ></MilestoneForm>
              <v-layout column class="border-wrapper pa-6">
                <v-layout
                  column
                  v-for="(task, taskIndex) in milestone.tasks"
                  :key="taskIndex"
                >
                  <TaskForm
                    v-model="milestone.tasks[taskIndex]"
                    :index="taskIndex"
                    :actionIndex="actionIndex + 1"
                    :milestoneIndex="milestoneIndex + 1"
                    :showDeleteBtn="milestone.tasks.length > 1"
                    :readonly="readonly || task.finished"
                    @delete="() => onDeleteTask(milestone, taskIndex)"
                  ></TaskForm>
                  <v-divider class="mb-4"></v-divider>
                </v-layout>
                <v-layout justify-center class="mt-2">
                  <DefaultIconButton
                    v-if="!readonly"
                    :config="addTaskBtnConfig"
                    @clicked="() => onAddTask(milestone)"
                  ></DefaultIconButton>
                </v-layout>
              </v-layout>
            </v-layout>
            <v-layout justify-center class="mt-6">
              <DefaultIconButton
                v-if="!readonly"
                :config="addMilestoneBtnConfig"
                @clicked="() => onAddMilestone(action)"
              ></DefaultIconButton>
            </v-layout>
          </v-layout>
        </v-layout>
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
    MilestoneForm: () => import("@/components/forms/project/MilestoneForm"),
    TaskForm: () => import("@/components/forms/project/TaskForm"),
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