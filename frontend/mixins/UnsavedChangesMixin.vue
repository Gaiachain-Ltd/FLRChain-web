<script>
export default {
  data() {
    return {
      isEditing: false,
      warning: "Do you want to leave without saving your recent changes?",
    };
  },
  methods: {
    preventNav(event) {
      if (!this.isEditing) return;
      event.preventDefault();
      event.returnValue = "";
    },
    postClick(event) {
      this.isEditing = false;
      this.$nextTick(() =>
        document.elementFromPoint(event.clientX, event.clientY).click()
      );
    },
    askForLeave(event, action) {
      if (this.isEditing) {
        if (!window.confirm(this.warning)) {
          return false;
        }

        this.resetEditing();

        if (action) {
          action(event);
        }

        this.$fetch();
      }
      return true;
    },
    resetEditing() {
      this.isEditing = false;
    },
  },
  beforeMount() {
    window.addEventListener("beforeunload", this.preventNav);
    this.$once("hook:beforeDestroy", () => {
      window.removeEventListener("beforeunload", this.preventNav);
    });
  },
  beforeRouteLeave(to, from, next) {
    if (this.askForLeave()) {
      next();
    }
  },
};
</script>