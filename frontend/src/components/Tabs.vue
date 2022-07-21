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
import { ITab } from "@/types/Tab";
import { defineComponent, PropType } from "vue";

export default defineComponent({
  name: "Tabs",
  props: {
    tabs: {
      required: true,
      type: Array as PropType<ITab[]>,
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
  background-color: #d0e7d0;
  border-radius: 12px;
  color: gray;
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
  background-color: #badcbb;
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
  background-color: #8ac38c;
  color: white;
}

.selectedTab ion-icon {
  color: white;
}
</style>
