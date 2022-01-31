<template>
  <v-card v-if="project.tasks.length > 0">
    <v-layout column ma-0 pa-6>
      <v-layout column v-for="(task, index) in project.tasks" :key="task.id">
        <v-divider class="mb-6" v-if="index != 0"></v-divider>
        <TaskForm
          ref="taskForms"
          :index="index"
          :showDeleteBtn="project.tasks.length > 1"
          :task.sync="project.tasks[index]"
          @delete="deleteTask"
        ></TaskForm>
      </v-layout>
      <DefaultIconButton
        :config="addBtnConf"
        @clicked="addTask"
      ></DefaultIconButton>
    </v-layout>
  </v-card>
</template>

<script>
export default {
  props: {
    project: {},
  },
  data() {
    return {
      addBtnConf: {
        iconOn: require("@/assets/side/plus_on.svg"),
        label: "Add task",
        enabled: true,
      },
    };
  },
  components: {
    TaskForm: () => import("@/components/forms/project/TaskForm"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
  },
  methods: {
    addTask() {
      this.$set(this.project, "tasks", [
        ...this.project.tasks,
        {
          name: "",
          instructions: "",
          batch: "0",
          reward: "0",
          count: 1,
        },
      ]);
    },
    deleteTask(index) {
      this.project.tasks.splice(index, 1);
      this.$emit("update:project", this.project);
      // this.$set(this.project, "tasks", this.project.tasks);
    },
    validate() {
      for (let index = 0; index < this.$refs.taskForms.length; index++) {
        const taskForm = this.$refs.taskForms[index];
        if (!taskForm.validate()) {
          return false;
        }
      }
      return true;
    },
  },
};
</script>
