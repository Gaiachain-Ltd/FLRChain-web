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
              (t +=
                parseFloat(task.batch) +
                parseFloat(task.reward) * parseFloat(task.count))
          )
        )
      );
      t += parseFloat(this.project.fac_adm_funds);
      return parseFloat(t.toFixed(6));
    },
    totalRewards() {
      let rewards = 0;
      if (!this.project.actions) {
        return 0;
      }
      this.project.actions.forEach((action) =>
        action.milestones.forEach((milestone) => {
          milestone.tasks.forEach((task) => {
            rewards += parseFloat(task.reward) * parseInt(task.count);
          });
        })
      );
      return parseFloat(rewards.toFixed(6));
    },
    totalBatch() {
      let batches = 0;
      if (!this.project.actions) {
        return 0;
      }
      this.project.actions.forEach((action) =>
        action.milestones.forEach((milestone) => {
          milestone.tasks.forEach((task) => {
            batches += parseFloat(task.batch);
          });
        })
      );
      return parseFloat(batches.toFixed(6));
    },
    totalFacAdmFunds() {
      return this.project.fac_adm_funds ? parseFloat(this.project.fac_adm_funds) : 0;
    },
    rewardsShare() {
      if (!this.totalRewards) {
        return 0;
      }
      return ((this.totalRewards * 100) / this.total).toFixed(2);
    },
    batchesShare() {
      if (!this.totalBatch) {
        return 0;
      }
      return ((this.totalBatch * 100) / this.total).toFixed(2);
    },
    facAdmFundsShare() {
      if (!this.totalFacAdmFunds) {
        return 0;
      }
      return ((this.totalFacAdmFunds * 100) / this.total).toFixed(2);
    },
  },
};
</script>