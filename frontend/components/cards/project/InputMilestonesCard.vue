<template>
  <v-layout column>
    <v-layout
      column
      v-for="(milestone, milestoneIndex) in project.milestones"
      :key="milestoneIndex"
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
        <v-layout column class="ml-4">
          <TaskForm
            v-for="(task, taskIndex) in milestone.tasks"
            v-model="milestone.tasks[taskIndex]"
            :key="taskIndex"
            :index="taskIndex"
            :milestoneIndex="milestoneIndex + 1"
            :showDeleteBtn="milestone.tasks.length > 1"
            @delete="() => onDeleteTask(milestone, taskIndex)"
          ></TaskForm>
        </v-layout>
        <v-layout justify-center>
          <DefaultIconButton
            :config="addTaskBtnConfig"
            @clicked="() => onAddTask(milestone)"
          ></DefaultIconButton>
        </v-layout>
      </v-layout>
    </v-layout>
    <v-layout justify-center>
      <DefaultIconButton
        :config="addMilestoneBtnConfig"
        @clicked="onAddMilestone"
      ></DefaultIconButton>
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
      },
      addTaskBtnConfig: {
        label: "Add task",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
      },
      addMilestoneBtnConfig: {
        label: "Add milestone",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
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
          action: "",
          reward: "0",
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