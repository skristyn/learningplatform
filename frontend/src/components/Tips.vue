<template>
  <div class="container">
    <h3>Tips</h3>
    <p class="callToAction">
      No one has left a tip here yet! Click the "Share a new tip" button below
      to share your knowledge on this topic.
    </p>
    <button>Share a new tip</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
// import { ref } from "vue";

export default defineComponent({
  name: "Tips",
});
</script>

<style scoped>
.container {
  color: var(--var-color-almost-black);
  padding: 56px;
}

.callToAction {
  font-style: italic;
}
</style>
