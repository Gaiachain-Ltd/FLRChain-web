<script>
import { SYNC } from "@/constants/project";

export default {
  props: {
    project: {},
  },
  timers: {
    refresh: { time: 5000, autostart: false, repeat: false },
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
    isSyncing() {
      return !this.project || this.project.sync == SYNC.TO_SYNC;
    },
  },
  methods: {
    refresh() {
      this.$axios.get(`projects/${this.project.id}/`).then((reply) => {
        this.requestRefresh();
        this.onProjectUpdate(reply.data);
      });
    },
    onProjectUpdate(project) {},
    requestRefresh() {
      if (this.isSyncing) {
        this.$timer.stop("refresh");
        this.$timer.start("refresh");
        return true;
      }
      return false;
    },
  },
};
</script>