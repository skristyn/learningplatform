<template>
  <div class="tabContainer">
    <div
      class="tab"
      :class="{ selectedTab: tab.tabTitle === $props.selectedTab }"
      v-for="(tab, index) in tabs"
      v-bind:key="index"
      @click="onSelectTab(tab.tabTitle)"
    >
      <ion-icon size="large" :name="tab.ionIconName"></ion-icon>
      <p>{{ tab.tabTitle }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Tab } from "@/types/Tab";
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: "DTabs",
  props: {
    tabs: {
      required: true,
      type: Array as PropType<Tab[]>,
    },
    selectedTab: {
      type: String,
    },
  },
  setup(props, { emit }) {
    const onSelectTab = (tabTitle: string) => {
      // emit the "onSelectTab" event with the given tab title
      emit("onSelectTab", tabTitle);
    };

    return { onSelectTab };
  },
});
</script>

<style scoped>
/* TODO: create mobile layout styles for all these */
.tabContainer {
  display: flex;
  flex-flow: row wrap;
  padding: 0 65px;
  background-color: var(--var-color-green-lighter);
  border-radius: 12px;
  color: var(--var-color-gray);
  font-weight: bold;
  font-size: 26px;
}

.tab {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  padding: 0 20px;
  border-right: 2px solid white;
  transition: 0.1s;
}

.tab:hover {
  cursor: pointer;
}

.tab:hover:not(.selectedTab) {
  background-color: var(--var-color-green-light);
}

.tab:last-child {
  border-right: none;
}

.tab p {
  margin: 16px 0;
}

ion-icon {
  margin-right: 10px;
}

.selectedTab {
  background-color: var(--var-color-green);
  color: white;
}

.selectedTab ion-icon {
  color: white;
}
</style>
