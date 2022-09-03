<template>
  <div class="header" @click="onClickHeader">
    <h3>{{ title }}</h3>
    <div class="subtitle">
      <ion-icon v-if="subtitleIcon" :name="subtitleIcon"></ion-icon>
      <p v-if="subtitle">{{ subtitle }}</p>
    </div>
    <span class="expandStatusIcon">
      <ion-icon
        :name="isExpanded ? 'remove-outline' : 'add-outline'"
      ></ion-icon>
    </span>
  </div>
  <div class="contents" v-show="isExpanded">
    <slot />
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs } from "vue";

export default defineComponent({
  name: "Expandable",
  props: {
    title: {
      required: true,
      type: String,
    },
    subtitle: {
      type: String,
    },
    subtitleIcon: {
      type: String,
      default: "",
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const state = reactive({
      isExpanded: props.isExpanded,
    });

    const onClickHeader = () => {
      state.isExpanded = !state.isExpanded;
    };

    return { ...toRefs(state), onClickHeader };
  },
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--var-color-gray);
  margin-top: 26px;
  cursor: pointer;
}

.header h3,
.header p {
  margin: 0;
}

.subtitle {
  display: flex;
  align-items: center;
  color: var(--var-color-gray);
}

.subtitle ion-icon {
  font-size: 22px;
  margin-right: 4px;
}

.expandStatusIcon ion-icon {
  font-size: 36px;
  --ionicon-stroke-width: 46px;
  color: var(--var-color-green);
}
</style>
