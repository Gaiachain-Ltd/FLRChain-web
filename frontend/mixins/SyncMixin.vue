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
  methods: {
    refresh() {
      console.log("REFRESH");
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
      return false;
    },
  },
};
</script>