<template>
  <v-layout column shrink class="border-wrapper px-3 pt-3">
    <v-layout
      column
      shrink
      v-for="(action, actionIndex) in project.actions"
      :key="actionIndex"
      class="mb-1"
    >
      <ProjectStructureDelegate
        :index="actionIndex + 1"
        :name="action.name"
        kind="action"
        class="mt-1 mb-1 mb-1"
      ></ProjectStructureDelegate>
      <v-layout
        column
        shrink
        v-for="(milestone, milestoneIndex) in action.milestones"
        :key="milestoneIndex"
        class="mb-1"
      >
        <ProjectStructureDelegate
          :index="`${actionIndex + 1}.${milestoneIndex + 1}`"
          :name="milestone.name"
          kind="milestone"
          class="mb-1"
        ></ProjectStructureDelegate>
        <v-layout
          column
          shrink
          v-for="(task, taskIndex) in milestone.tasks"
          :key="taskIndex"
          class="mb-1"
        >
          <ProjectStructureDelegate
            :index="`${actionIndex + 1}.${milestoneIndex + 1}.${taskIndex + 1}`"
            :name="task.name"
            kind="task"
          ></ProjectStructureDelegate>
        </v-layout>
      </v-layout>
    </v-layout>
  </v-layout>
</template>

<script>
export default {
  props: {
    project: {},
  },
  components: {
    ProjectStructureDelegate: () =>
      import("@/components/delegates/projects/ProjectStructureDelegate"),
  },
};
</script>
