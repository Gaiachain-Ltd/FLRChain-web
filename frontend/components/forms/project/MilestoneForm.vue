<template>
  <v-form ref="form">
    <v-layout column>
      <v-layout
        ma-0
        :class="[collapsed && 'mb-3', milestoneIndex > 0 && 'mt-3']"
        justify-center
      >
        <DefaultText color="#00868a" size="20" bold>{{
          `Milesone ${actionIndex + 1}.${milestoneIndex + 1}`
        }}</DefaultText>
        <DefaultIconButton
          class="ml-6"
          v-if="action.milestones.length > 1"
          :config="deleteBtnConf"
          @clicked="onDeleteMilestone"
        ></DefaultIconButton>
        <v-spacer></v-spacer>
        <CollapseButton v-model="collapsed"></CollapseButton>
      </v-layout>
      <v-layout column v-show="!collapsed">
        <TextInput
          label="Milestone name*"
          v-model="milestone.name"
          :readonly="readonly"
          :rules="requiredRules"
          required
        ></TextInput>
      </v-layout>
      <v-layout column class="border-wrapper pa-6" v-show="!collapsed">
        <v-layout
          column
          v-for="(task, taskIndex) in milestone.tasks"
          :key="taskIndex"
        >
          <TaskForm
            ref="taskForm"
            v-model="milestone.tasks[taskIndex]"
            :index="taskIndex"
            :actionIndex="actionIndex + 1"
            :milestoneIndex="milestoneIndex + 1"
            :showDeleteBtn="milestone.tasks.length > 1"
            :readonly="readonly || task.finished"
            @delete="() => onDeleteTask(taskIndex)"
          ></TaskForm>
          <v-divider class="mb-4"></v-divider>
        </v-layout>
        <v-layout justify-center class="mt-2">
          <DefaultIconButton
            v-if="!readonly"
            :config="addTaskBtnConfig"
            @clicked="onAddTask"
          ></DefaultIconButton>
        </v-layout>
      </v-layout>
      <v-divider v-show="collapsed"></v-divider>
    </v-layout>
  </v-form>
</template>

<script>
import ValidatorMixin from "@/validators";

export default {
  mixins: [ValidatorMixin],
  props: {
    actionIndex: {},
    milestoneIndex: {},
    action: {},
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
      addTaskBtnConfig: {
        iconOn: require("@/assets/icons/add_task.svg"),
        label: "Add task",
        enabled: true,
        colorEnabled: this.$vuetify.theme.themes.light.primary,
        spacing: 2,
      },
    };
  },
  computed: {
    milestone: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
  methods: {
    onDeleteMilestone() {
      this.$emit("delete:milestone");
    },
    onDeleteTask(index) {
      this.$emit("delete:task", index);
    },
    onAddTask() {
      this.$emit("add:task");
    },
    validate() {
      const f = this.$refs.form.validate();
      for (let index = 0; index < this.$refs.taskForm.length; index++) {
        const element = this.$refs.taskForm[index];
        if (!element.validate()) {
          return false;
        }
      }
      return f;
    },
  },
  components: {
    CollapseButton: () => import("@/components/buttons/CollapseButton"),
    DefaultText: () => import("@/components/texts/DefaultText"),
    TextInput: () => import("@/components/inputs/TextInput"),
    DefaultIconButton: () => import("@/components/buttons/DefaultIconButton"),
    TaskForm: () => import("@/components/forms/project/TaskForm"),
  },
};
</script>