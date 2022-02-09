<template>
  <v-layout column>
    <v-layout
      column
      v-for="(milestone, milestoneIndex) in project.milestones"
      :key="milestoneIndex"
      class="border-wrapper pa-3"
    >
      <v-layout ma-0 mb-3 justify-center>
        <DefaultText :color="$vuetify.theme.themes.light.primary">{{
          `Milesone ${milestoneIndex + 1}`
        }}</DefaultText>
        <v-spacer></v-spacer>
        <DefaultIconButton
          v-if="project.milestones.length > 1"
          :config="deleteBtnConf"
          @clicked="() => onDeleteMilestone(milestoneIndex)"
        ></DefaultIconButton>
      </v-layout>
      <v-layout column>
        <MilestoneForm
          v-model="project.milestones[milestoneIndex]"
        ></MilestoneForm>
        <v-layout column class="border-wrapper pa-3">
          <v-layout
            column
            v-for="(task, taskIndex) in milestone.tasks"
            :key="taskIndex"
          >
            <TaskForm
              v-model="milestone.tasks[taskIndex]"
              :index="taskIndex"
              :milestoneIndex="milestoneIndex + 1"
              :showDeleteBtn="milestone.tasks.length > 1"
              @delete="() => onDeleteTask(milestone, taskIndex)"
            ></TaskForm>
            <v-divider class="mb-4"></v-divider>
          </v-layout>
          <v-layout justify-center class="my-3">
            <DefaultIconButton
              :config="addTaskBtnConfig"
              @clicked="() => onAddTask(milestone)"
            ></DefaultIconButton>
          </v-layout>
        </v-layout>
      </v-layout>
      <v-layout justify-center class="mb-3 mt-6">
        <DefaultIconButton
          :config="addMilestoneBtnConfig"
          @clicked="onAddMilestone"
        ></DefaultIconButton>
      </v-layout>
    </v-layout>
  </v-layout>
</template>

<script>
import _ from "lodash";

export default {
  props: {
    project: {},
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
        iconOn: require("@/assets/icons/add_milestone.svg"),
        label: "Add milestone",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
    };
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    MilestoneForm: () => import("@/components/forms/project/MilestoneForm"),
    TaskForm: () => import("@/components/forms/project/TaskForm"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
  methods: {
    onAddMilestone() {
      this.$set(this.project, "milestones", [
        ...(this.project.milestones || []),
        {
          name: "",
        },
      ]);
    },
    onAddTask(milestone) {
      this.$set(milestone, "tasks", [
        ...(milestone.tasks || []),
        {
          name: "",
          instructions: "",
          batch: "0",
          reward: "0",
          count: 1,
        },
      ]);
    },
    onDeleteTask(milestone, index) {
      milestone.tasks.splice(index, 1);
    },
    onDeleteMilestone(index) {
      this.project.milestones.splice(index, 1);
    },
  },
};
</script>

<style scoped>
</style>