<template>
  <v-layout column>
    <v-layout
      column
      v-for="(milestone, milestoneIndex) in project.milestones"
      :key="milestoneIndex"
    >
      <DefaultText>{{ `Milesone ${milestoneIndex}` }}</DefaultText>
      <v-layout column>
        <MilestoneForm></MilestoneForm>
        <v-layout column>
          <TaskForm
            v-for="(task, taskIndex) in milestone.tasks"
            :key="taskIndex"
            :task.sync="milestone.tasks[taskIndex]"
            :index="taskIndex"
          ></TaskForm>
        </v-layout>
        <ActionButton color="primary">Add Task</ActionButton>
      </v-layout>
    </v-layout>
    <ActionButton color="primary" @click.prevent="onAddMilestone"
      >Add Milestone</ActionButton
    >
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    DefaultText: () => import("@/components/texts/DefaultText"),
    MilestoneForm: () => import("@/components/forms/project/MilestoneForm"),
    TaskForm: () => import("@/components/forms/project/TaskForm"),
    ActionButton: () => import("@/components/buttons/ActionButton"),
  },
  methods: {
    onAddMilestone() {
      this.$set(this.project, "milestones", [
        ...this.project.milestones,
        {
          name: "",
        },
      ]);
    },
  },
};
</script>