<template>
  <v-layout column shrink class="border-wrapper px-3 pt-3">
    <v-layout
      column
      shrink
      v-for="(milestone, milestoneIndex) in project.milestones"
      :key="milestoneIndex"
      class="mb-1"
    >
      <ProjectStructureDelegate
        :index="milestoneIndex + 1"
        :name="milestone.name"
        milestone
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
          :index="`${milestoneIndex + 1}.${taskIndex + 1}`"
          :name="task.name"
        ></ProjectStructureDelegate>
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
