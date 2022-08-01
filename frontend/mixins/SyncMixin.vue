<script>
export default {
  timers: {
    refresh: { time: 5000, autostart: false, repeat: false },
  },
  computed: {
    isSyncing() {
      return false;
    },
  },
  watch: {
    isSyncing() {
      this.$timer.stop("refresh");
      this.$timer.start("refresh");
    }
  },
  methods: {
    refresh() {
      this.$axios.get(this.url).then((reply) => {
        this.requestRefresh();
        this.onUpdate(reply.data);
      });
    },
    onUpdate(value) {},
    requestRefresh() {
      if (this.isSyncing) {
        this.$timer.stop("refresh");
        this.$timer.start("refresh");
        return true;
      }
      this.$timer.stop("refresh");
      return false;
    },
  },
};
</script>