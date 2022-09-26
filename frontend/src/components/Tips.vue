<template>
  <div class="tipsMain">
    <!-- Tips view -->
    <div v-if="visible === TipsView.TIPS" class="tips">
      <h3>Tips</h3>
      <div>
        <ul v-if="tips.length" class="tipsList">
          <li v-for="(tip, index) in tips" :key="index">{{ tip }}</li>
        </ul>
        <p v-else class="callToAction">
          No one has left a tip here yet! Click the "Share a new tip" button
          below to share your knowledge on this topic.
        </p>
      </div>
      <div class="callToActionButtonContainer">
        <button
          aria-label="Click to share a new tip"
          alt="Share new tip button"
          title="Share a new tip"
          @click="setVisible(TipsView.SHARE)"
        >
          Share a new tip
        </button>
      </div>
    </div>

    <!-- Share view -->
    <div v-else-if="visible === TipsView.SHARE" class="share">
      <h3>Share a tip</h3>
      <form class="form" @submit.prevent="shareTip">
        <button
          class="closeButton"
          aria-label="Close tip input"
          alt="Button to close tip input"
          title="Close"
          @click="setVisible(TipsView.TIPS)"
        >
          <ion-icon class="closeIcon" name="close-circle-outline"></ion-icon>
        </button>
        <textarea
          name="tip"
          aria-label="Tip to share"
          placeholder="Enter new tip to share"
          v-model="tip"
        ></textarea>
        <button class="shareButton" type="submit" :disabled="!tip">
          Share
        </button>
      </form>
    </div>

    <!-- Thanks view -->
    <div v-else-if="visible === TipsView.THANKS">
      <h3>Thank you!</h3>
      <p>Your tip has been shared.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

enum TipsView {
  TIPS = "tips",
  SHARE = "share",
  THANKS = "thanks",
}

export default defineComponent({
  name: "Tips",
  setup() {
    const tip = ref<string>("");
    const tips = ref<string[]>([]);
    const visible = ref<TipsView>(TipsView.TIPS);

    const setVisible = (show: TipsView) => {
      visible.value = show;
    };

    // TODO add a cancel button
    // TODO shareTip should also send the tips[] update to the database
    // TODO adding tip should end with thank-you
    // TODO tips should scroll
    // TODO sanitize input
    const shareTip = () => {
      if (tip.value.trim() !== "") {
        tips.value.push(tip.value);
      }
      tip.value = "";

      setVisible(TipsView.THANKS);
    };

    return {
      tip,
      tips,
      visible,
      setVisible,
      shareTip,
      TipsView,
    };
  },
});
</script>

<style scoped>
.tipsMain {
  color: var(--var-color-almost-black);
}

/* Tips view */

.callToAction {
  font-style: italic;
}

.callToActionButtonContainer {
  text-align: center;
  padding: 10px 0 0;
}

.callToActionButtonContainer button {
  cursor: pointer;
}

/* Share view */

.share h3 {
  margin-bottom: 10px;
}

ion-icon {
  /* hide the default pointer events and hover titles */
  pointer-events: none;
}

.closeButton {
  margin: 0 -18px -20px 0;
  /* hide the default styles for the buttons */
  background: none;
  border: none;
  cursor: pointer;
}

.closeIcon {
  font-size: 30px;
  cursor: pointer;
  background: white;
}

.shareButton {
  margin: -29px 5px 0;
  cursor: pointer;
}

.form {
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-end;
}

.form textarea {
  resize: none;
  height: 150px;
  width: 100%;
}
</style>
