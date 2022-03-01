<script>
export default {
  props: {
    project: {},
  },
  computed: {
    total() {
      if (!this.project.actions) {
        return 0;
      }
      let t = 0;
      this.project.actions.forEach((action) =>
        action.milestones.forEach((milestone) =>
          milestone.tasks.forEach(
            (task) =>
              (t =
                parseFloat(task.batch) +
                parseFloat(task.reward) * parseFloat(task.count))
          )
        )
      );
      t += parseFloat(this.project.fac_adm_funds);
      return t;
    },
  },
};
</script>